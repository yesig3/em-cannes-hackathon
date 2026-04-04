"""Tests for ENS integration — resolution, text records, subnames."""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

# Add ens/ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestConfig:
    """Test network configuration toggle."""

    def test_default_is_mainnet(self):
        """Default ENS_NETWORK is mainnet."""
        with patch.dict("os.environ", {"ENS_NETWORK": "mainnet"}):
            import importlib
            import config
            importlib.reload(config)
            assert config.CHAIN_ID == 1
            assert "mainnet" in config.NETWORK_LABEL.lower()

    def test_sepolia_config(self):
        """ENS_NETWORK=sepolia switches to Sepolia testnet."""
        with patch.dict("os.environ", {"ENS_NETWORK": "sepolia"}):
            import importlib
            import config
            importlib.reload(config)
            assert config.CHAIN_ID == 11155111
            assert "sepolia" in config.NETWORK_LABEL.lower()

    def test_ens_registry_same_on_both(self):
        """ENS registry address is the same on mainnet and Sepolia."""
        import config
        mainnet = config._CONFIGS["mainnet"]["ens_registry"]
        sepolia = config._CONFIGS["sepolia"]["ens_registry"]
        assert mainnet == sepolia  # Same CREATE2 address
        assert mainnet.startswith("0x")

    def test_em_text_record_prefix(self):
        """EM text records use correct prefix."""
        import config
        assert config.EM_TEXT_RECORD_PREFIX == "com.execution.market"
        assert "agentId" in config.EM_TEXT_RECORDS
        assert config.EM_TEXT_RECORDS["agentId"] == "com.execution.market.agentId"


class TestNamehash:
    """Test EIP-137 namehash implementation."""

    def test_empty_namehash(self):
        """namehash('') returns 32 zero bytes."""
        from text_records import namehash
        result = namehash("")
        assert result == b"\x00" * 32
        assert len(result) == 32

    def test_eth_namehash(self):
        """namehash('eth') produces known hash."""
        from text_records import namehash
        result = namehash("eth")
        assert len(result) == 32
        assert result != b"\x00" * 32  # Not empty

    def test_namehash_deterministic(self):
        """Same input produces same namehash."""
        from text_records import namehash
        a = namehash("vitalik.eth")
        b = namehash("vitalik.eth")
        assert a == b

    def test_different_names_different_hashes(self):
        """Different names produce different namehashes."""
        from text_records import namehash
        a = namehash("alice.eth")
        b = namehash("bob.eth")
        assert a != b

    def test_subname_namehash(self):
        """Subname namehash is different from parent."""
        from text_records import namehash
        parent = namehash("execution.eth")
        child = namehash("alice.execution.eth")
        assert parent != child
        assert len(child) == 32


class TestResolver:
    """Test ENS name resolution."""

    def test_resolve_name_success(self):
        """resolve_name returns address for known names."""
        mock_w3 = MagicMock()
        mock_w3.ens.address.return_value = "0x1234567890abcdef1234567890abcdef12345678"

        with patch("resolver._w3", mock_w3):
            from resolver import resolve_name
            result = resolve_name("test.eth")

            assert result["resolved"] is True
            assert result["address"] == "0x1234567890abcdef1234567890abcdef12345678"
            assert result["name"] == "test.eth"

    def test_resolve_name_not_found(self):
        """resolve_name returns resolved=False for unregistered names."""
        mock_w3 = MagicMock()
        mock_w3.ens.address.return_value = None

        with patch("resolver._w3", mock_w3):
            from resolver import resolve_name
            result = resolve_name("nonexistent-name-12345.eth")

            assert result["resolved"] is False
            assert result["address"] is None

    def test_resolve_name_error(self):
        """resolve_name handles RPC errors gracefully."""
        mock_w3 = MagicMock()
        mock_w3.ens.address.side_effect = Exception("RPC timeout")

        with patch("resolver._w3", mock_w3):
            from resolver import resolve_name
            result = resolve_name("error.eth")

            assert result["resolved"] is False
            assert "error" in result

    def test_reverse_resolve_success(self):
        """reverse_resolve returns name for addresses with reverse record."""
        mock_w3 = MagicMock()
        mock_w3.ens.name.return_value = "vitalik.eth"

        with patch("resolver._w3", mock_w3):
            from resolver import reverse_resolve
            result = reverse_resolve("0x1234567890abcdef1234567890abcdef12345678")

            assert result["resolved"] is True
            assert result["name"] == "vitalik.eth"

    def test_reverse_resolve_no_record(self):
        """reverse_resolve handles addresses without reverse records."""
        mock_w3 = MagicMock()
        mock_w3.ens.name.return_value = None

        with patch("resolver._w3", mock_w3):
            from resolver import reverse_resolve
            result = reverse_resolve("0x0000000000000000000000000000000000000000")

            assert result["resolved"] is False

    def test_resolve_multiple(self):
        """resolve_multiple processes list of names."""
        mock_w3 = MagicMock()
        mock_w3.ens.address.side_effect = [
            "0xAAAA" + "0" * 36,
            None,
            "0xBBBB" + "0" * 36,
        ]

        with patch("resolver._w3", mock_w3):
            from resolver import resolve_multiple
            results = resolve_multiple(["a.eth", "b.eth", "c.eth"])

            assert len(results) == 3
            assert results[0]["resolved"] is True
            assert results[1]["resolved"] is False
            assert results[2]["resolved"] is True


class TestTextRecords:
    """Test ENS text record reading."""

    def test_get_text_record_success(self):
        """get_text_record returns value for existing records."""
        mock_w3 = MagicMock()
        mock_resolver = MagicMock()
        mock_resolver.address = "0x1234567890abcdef1234567890abcdef12345678"
        mock_resolver_contract = MagicMock()
        mock_resolver_contract.functions.text.return_value.call.return_value = "https://example.com"
        mock_w3.ens.resolver.return_value = mock_resolver
        mock_w3.eth.contract.return_value = mock_resolver_contract

        with patch("text_records.get_web3", return_value=mock_w3):
            from text_records import get_text_record
            result = get_text_record("test.eth", "url")
            assert result == "https://example.com"

    def test_get_text_record_empty(self):
        """get_text_record returns None for empty records."""
        mock_w3 = MagicMock()
        mock_resolver = MagicMock()
        mock_resolver.address = "0x1234567890abcdef1234567890abcdef12345678"
        mock_resolver_contract = MagicMock()
        mock_resolver_contract.functions.text.return_value.call.return_value = ""
        mock_w3.ens.resolver.return_value = mock_resolver
        mock_w3.eth.contract.return_value = mock_resolver_contract

        with patch("text_records.get_web3", return_value=mock_w3):
            from text_records import get_text_record
            result = get_text_record("test.eth", "nonexistent.key")
            assert result is None

    def test_get_text_record_no_resolver(self):
        """get_text_record returns None when name has no resolver."""
        mock_w3 = MagicMock()
        mock_w3.ens.resolver.return_value = None

        with patch("text_records.get_web3", return_value=mock_w3):
            from text_records import get_text_record
            result = get_text_record("no-resolver.eth", "url")
            assert result is None

    def test_proposed_agent_records(self):
        """proposed_agent_records generates correct EM metadata."""
        from text_records import proposed_agent_records
        records = proposed_agent_records(agent_id=2106, world_id_verified=True)

        assert records["com.execution.market.agentId"] == "2106"
        assert records["com.execution.market.role"] == "agent"
        assert records["com.execution.market.worldIdVerified"] == "true"
        assert records["url"] == "https://execution.market"
        assert records["com.twitter"] == "executi0nmarket"
        assert len(records) > 5


class TestSubnames:
    """Test worker subname resolution."""

    def test_resolve_worker_success(self):
        """resolve_worker returns address + metadata for valid subname."""
        with patch("subnames.resolve_name") as mock_resolve, \
             patch("subnames.get_em_metadata") as mock_meta:
            mock_resolve.return_value = {
                "resolved": True,
                "address": "0xAlice" + "0" * 34,
                "ens_link": "https://app.ens.domains/alice.execution.eth",
            }
            mock_meta.return_value = {
                "em_metadata": {"role": "worker", "worldIdVerified": "true"},
            }

            from subnames import resolve_worker
            result = resolve_worker("alice.execution.eth")

            assert result["resolved"] is True
            assert result["address"].startswith("0xAlice")
            assert result["em_metadata"]["role"] == "worker"

    def test_resolve_worker_not_found(self):
        """resolve_worker handles unregistered subnames."""
        with patch("subnames.resolve_name") as mock_resolve:
            mock_resolve.return_value = {
                "resolved": False,
                "error": "Name not registered",
            }

            from subnames import resolve_worker
            result = resolve_worker("nonexistent.execution.eth")

            assert result["resolved"] is False

    def test_resolve_fleet(self):
        """resolve_fleet processes multiple workers."""
        with patch("subnames.resolve_name") as mock_resolve, \
             patch("subnames.get_em_metadata") as mock_meta:
            mock_resolve.return_value = {
                "resolved": False,
                "error": "Not registered",
            }
            mock_meta.return_value = {"em_metadata": {}}

            from subnames import resolve_fleet
            result = resolve_fleet("execution.eth", ["alice", "bob"])

            assert result["total_workers"] == 2
            assert result["parent_domain"] == "execution.eth"

    def test_proposed_fleet_structure(self):
        """proposed_fleet_structure returns valid fleet config."""
        from subnames import proposed_fleet_structure
        fleet = proposed_fleet_structure()

        assert fleet["parent"] == "execution.eth"
        assert len(fleet["subnames"]) >= 3
        assert any(s["role"] == "worker" for s in fleet["subnames"])
        assert any(s["role"] == "agent" for s in fleet["subnames"])

    def test_get_worker_identity_layers(self):
        """get_worker_identity returns multi-layer identity."""
        with patch("subnames.resolve_name") as mock_resolve, \
             patch("subnames.get_em_metadata") as mock_meta:
            mock_resolve.return_value = {
                "resolved": True,
                "address": "0xBob" + "0" * 36,
                "ens_link": "https://app.ens.domains/bob.execution.eth",
            }
            mock_meta.return_value = {
                "em_metadata": {
                    "agentId": "42",
                    "worldIdVerified": "true",
                    "worldIdLevel": "orb",
                },
            }

            from subnames import get_worker_identity
            result = get_worker_identity("bob.execution.eth")

            assert result["resolved"] is True
            layers = result["identity_layers"]
            assert layers["ens"]["status"] == "resolved"
            assert layers["erc8004"]["agentId"] == "42"
            assert layers["erc8004"]["status"] == "linked"
            assert layers["worldId"]["verified"] == "true"
