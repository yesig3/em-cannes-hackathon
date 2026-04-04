"""Tests for Hedera ERC-8004 integration."""

import os
import sys
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Add hedera/ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

pytestmark = pytest.mark.asyncio


class TestConfig:
    """Test network configuration toggle."""

    def test_default_is_testnet(self):
        """Default HEDERA_8004_NETWORK is testnet."""
        with patch.dict("os.environ", {"HEDERA_8004_NETWORK": "testnet"}):
            import importlib
            import config
            importlib.reload(config)
            assert config.CHAIN_ID == 296
            assert config.FACILITATOR_NETWORK == "hedera-testnet"
            assert "testnet" in config.RPC_URL

    def test_mainnet_config(self):
        """HEDERA_8004_NETWORK=mainnet switches to mainnet."""
        with patch.dict("os.environ", {"HEDERA_8004_NETWORK": "mainnet"}):
            import importlib
            import config
            importlib.reload(config)
            assert config.CHAIN_ID == 295
            assert config.FACILITATOR_NETWORK == "hedera"
            assert "mainnet" in config.RPC_URL

    def test_identity_registry_addresses_differ(self):
        """Testnet and mainnet use different registry addresses."""
        import config
        testnet = config._CONFIGS["testnet"]["identity_registry"]
        mainnet = config._CONFIGS["mainnet"]["identity_registry"]
        assert testnet != mainnet
        assert testnet.startswith("0x8004")
        assert mainnet.startswith("0x8004")


class TestIdentity:
    """Test ERC-8004 identity operations."""

    async def test_get_identity_success(self):
        """get_identity returns agent data when found."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "agentId": 1,
            "owner": "0x350427992DC5cE57fAbAe5B12251e2354f64e976",
        }

        with patch("identity.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_resp
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_cls.return_value = mock_client

            from identity import get_identity
            result = await get_identity(1)

            assert result["found"] is True
            assert result["agentId"] == 1

    async def test_get_identity_not_found(self):
        """get_identity returns found=False for missing agents."""
        mock_resp = MagicMock()
        mock_resp.status_code = 404

        with patch("identity.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_resp
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_cls.return_value = mock_client

            from identity import get_identity
            result = await get_identity(9999)

            assert result["found"] is False

    async def test_register_agent_sends_correct_payload(self):
        """register_agent sends correct network and params."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"agentId": 42, "txHash": "0xabc"}

        with patch("identity.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_resp
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_cls.return_value = mock_client

            from identity import register_agent
            result = await register_agent(
                recipient="0x1234567890abcdef" * 2 + "abcdef01",
            )

            assert result["status_code"] == 200
            assert result["agentId"] == 42

            # Verify payload includes correct network
            call_args = mock_client.post.call_args
            payload = call_args[1]["json"]
            assert "hedera" in payload["network"]


class TestReputation:
    """Test reputation/feedback operations."""

    async def test_submit_feedback_success(self):
        """submit_feedback sends correct payload to Facilitator."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"txHash": "0xfeedback123"}

        with patch("reputation.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_resp
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_cls.return_value = mock_client

            from reputation import submit_feedback
            result = await submit_feedback(agent_id=1, value=95)

            assert result["status_code"] == 200
            assert "txHash" in result

    async def test_get_reputation(self):
        """get_reputation returns score data."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "agentId": 1,
            "averageValue": 92,
            "totalFeedback": 5,
        }

        with patch("reputation.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_resp
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_cls.return_value = mock_client

            from reputation import get_reputation
            result = await get_reputation(1)

            assert result["agentId"] == 1
            assert result["averageValue"] == 92


class TestPayment:
    """Test Hedera payment/balance operations."""

    async def test_get_balance(self):
        """get_balance converts wei to HBAR."""
        # 100 HBAR = 100 * 10^18 wei
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "result": hex(100 * 10**18),
        }

        with patch("payment.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_resp
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_cls.return_value = mock_client

            from payment import get_balance
            result = await get_balance("0x1234")

            assert result["balance_hbar"] == 100.0
            assert "hashscan" in result["explorer"]

    async def test_get_chain_id(self):
        """get_chain_id returns correct chain ID."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"result": hex(296)}

        with patch("payment.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_resp
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_cls.return_value = mock_client

            from payment import get_chain_id
            result = await get_chain_id()

            assert result == 296
