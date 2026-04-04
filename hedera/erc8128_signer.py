"""
ERC-8128 HTTP Request Signer

Signs API requests using RFC 9421 HTTP Message Signatures + EIP-191 personal_sign.
Required for authenticated endpoints on Execution Market production API.

Usage:
    signer = ERC8128Signer(private_key="0x...", api_base_url="https://api.execution.market")
    nonce = await signer.fetch_nonce()
    headers = signer.sign_request("POST", url, body=json_body, nonce=nonce)
"""

import base64
import hashlib
import time
from typing import Optional
from urllib.parse import urlparse

from eth_account import Account
from eth_account.messages import encode_defunct
import httpx


class ERC8128Signer:
    """Sign HTTP requests with ERC-8128 (RFC 9421 + EIP-191) signatures."""

    def __init__(
        self,
        private_key: str,
        chain_id: int = 8453,
        api_base_url: str = "https://api.execution.market",
        validity_sec: int = 60,
    ):
        self.account = Account.from_key(private_key)
        self.address = self.account.address.lower()
        self.chain_id = chain_id
        self.api_base_url = api_base_url.rstrip("/")
        self.validity_sec = validity_sec

    async def fetch_nonce(self, timeout: float = 10.0) -> str:
        """Fetch a fresh nonce from the API."""
        url = f"{self.api_base_url}/api/v1/auth/erc8128/nonce"
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            return data["nonce"]

    def sign_request(
        self,
        method: str,
        url: str,
        body: Optional[str] = None,
        nonce: Optional[str] = None,
    ) -> dict:
        """
        Sign an HTTP request and return auth headers.

        Returns dict with: Signature, Signature-Input, and optionally Content-Digest.
        """
        parsed = urlparse(url)
        authority = parsed.netloc
        path = parsed.path or "/"

        now = int(time.time())
        created = now
        expires = now + self.validity_sec

        keyid = f"erc8128:{self.chain_id}:{self.address}"

        covered = ["@method", "@authority", "@path"]
        extra_headers = {}

        if body is not None:
            digest = hashlib.sha256(body.encode("utf-8")).digest()
            b64_digest = base64.b64encode(digest).decode("ascii")
            extra_headers["Content-Digest"] = f"sha-256=:{b64_digest}:"
            covered.append("content-digest")

        # Build RFC 9421 signature base
        lines = []
        for component in covered:
            if component == "@method":
                lines.append(f'"@method": {method.upper()}')
            elif component == "@authority":
                lines.append(f'"@authority": {authority}')
            elif component == "@path":
                lines.append(f'"@path": {path}')
            elif component == "content-digest":
                lines.append(f'"content-digest": {extra_headers.get("Content-Digest", "")}')

        comp_str = " ".join(f'"{c}"' for c in covered)
        sig_params = f"({comp_str});created={created};expires={expires}"
        if nonce:
            sig_params += f';nonce="{nonce}"'
        sig_params += f';keyid="{keyid}"'

        lines.append(f'"@signature-params": {sig_params}')
        sig_base = "\n".join(lines)

        # EIP-191 personal_sign
        msg = encode_defunct(text=sig_base)
        signed = self.account.sign_message(msg)
        sig_b64 = base64.b64encode(signed.signature).decode("ascii")

        extra_headers["Signature"] = f"eth=:{sig_b64}:"
        extra_headers["Signature-Input"] = f"eth={sig_params}"

        return extra_headers
