"""
AAXYY AI - Address Registry

Stores known blockchain addresses, their identified roles,
attribution confidence, source, and blockchain network.

This module provides address intelligence only.
It does not make trading decisions.
"""

from address_attribution import create_attribution
from address_intelligence import classify_address_role
from chain_intelligence import classify_chain


class AddressRegistry:
    """Registry of known blockchain addresses and their metadata."""

    def __init__(self):
        self._addresses = {}

    def add_address(
        self,
        address,
        role,
        confidence="UNKNOWN",
        source="",
        chain="unknown",
    ):
        """Add a validated address attribution."""

        if not isinstance(address, str) or not address.strip():
            return False

        normalized_role = classify_address_role(role)

        if normalized_role == "unknown":
            return False

        normalized_chain = classify_chain(chain)

        if normalized_chain == "unknown":
            return False

        attribution = create_attribution(
            address=address,
            role=normalized_role,
            confidence=confidence,
            source=source,
        )

        if attribution is None:
            return False

        key = (normalized_chain, attribution.address)

        self._addresses[key] = attribution

        return True

    def get_role(self, address, chain="unknown"):
        """Return the known role for an address on a chain."""

        normalized_chain = classify_chain(chain)

        if normalized_chain == "unknown":
            return "unknown"

        normalized_address = (
            address.strip()
            if isinstance(address, str)
            else ""
        )

        attribution = self._addresses.get(
            (normalized_chain, normalized_address)
        )

        if attribution is None:
            return "unknown"

        return attribution.role

    def get_confidence(self, address, chain="unknown"):
        """Return attribution confidence for an address on a chain."""

        normalized_chain = classify_chain(chain)

        if normalized_chain == "unknown":
            return "UNKNOWN"

        normalized_address = (
            address.strip()
            if isinstance(address, str)
            else ""
        )

        attribution = self._addresses.get(
            (normalized_chain, normalized_address)
        )

        if attribution is None:
            return "UNKNOWN"

        return attribution.confidence

    def get_source(self, address, chain="unknown"):
        """Return the attribution source for an address on a chain."""

        normalized_chain = classify_chain(chain)

        if normalized_chain == "unknown":
            return ""

        normalized_address = (
            address.strip()
            if isinstance(address, str)
            else ""
        )

        attribution = self._addresses.get(
            (normalized_chain, normalized_address)
        )

        if attribution is None:
            return ""

        return attribution.source

    def has_address(self, address, chain="unknown"):
        """Return True when an address exists on the specified chain."""

        return self.get_role(address, chain) != "unknown"
