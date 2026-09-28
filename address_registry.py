"""
AAXYY AI - Address Registry

Stores known blockchain addresses, their identified roles,
and the confidence of those identifications.

This module provides address intelligence only.
It does not make trading decisions.
"""

from address_attribution import create_attribution
from address_intelligence import classify_address_role


class AddressRegistry:
    """Registry of known blockchain addresses and their roles."""

    def __init__(self):
        self._addresses = {}

    def add_address(
        self,
        address,
        role,
        confidence="UNKNOWN",
        source="",
    ):
        """Add a validated address attribution."""

        if not isinstance(address, str) or not address.strip():
            return False

        normalized_role = classify_address_role(role)

        if normalized_role == "unknown":
            return False

        attribution = create_attribution(
            address=address,
            role=normalized_role,
            confidence=confidence,
            source=source,
        )

        if attribution is None:
            return False

        self._addresses[attribution.address] = attribution
        return True

    def get_role(self, address):
        """Return the known role for an address."""

        attribution = self._addresses.get(
            address.strip() if isinstance(address, str) else ""
        )

        if attribution is None:
            return "unknown"

        return attribution.role

    def get_confidence(self, address):
        """Return attribution confidence for an address."""

        attribution = self._addresses.get(
            address.strip() if isinstance(address, str) else ""
        )

        if attribution is None:
            return "UNKNOWN"

        return attribution.confidence

    def get_source(self, address):
        """Return the attribution source for an address."""

        attribution = self._addresses.get(
            address.strip() if isinstance(address, str) else ""
        )

        if attribution is None:
            return ""

        return attribution.source

    def has_address(self, address):
        """Return True when the address exists in the registry."""

        return self.get_role(address) != "unknown"
