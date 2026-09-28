"""
AAXYY AI - Address Registry

Stores known blockchain addresses and their identified roles.

This module provides address intelligence only.
It does not make trading decisions.
"""

from address_intelligence import classify_address_role


class AddressRegistry:
    """Registry of known blockchain addresses and their roles."""

    def __init__(self):
        self._addresses = {}

    def add_address(self, address, role):
        """Add a known address with a validated role."""

        if not isinstance(address, str) or not address.strip():
            return False

        normalized_address = address.strip()
        normalized_role = classify_address_role(role)

        if normalized_role == "unknown":
            return False

        self._addresses[normalized_address] = normalized_role
        return True

    def get_role(self, address):
        """Return the known role for an address."""

        if not isinstance(address, str):
            return "unknown"

        normalized_address = address.strip()

        return self._addresses.get(normalized_address, "unknown")

    def has_address(self, address):
        """Return True when the address exists in the registry."""

        return self.get_role(address) != "unknown"
