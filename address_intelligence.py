"""
AAXYY AI - Address Intelligence

Provides a simple foundation for identifying the role of blockchain
addresses before interpreting whale transfers.

This module does not make trading decisions.
"""


KNOWN_ADDRESS_ROLES = {
    "exchange",
    "wallet",
    "bridge",
    "market_maker",
    "unknown",
}


def classify_address_role(address_type):
    """
    Normalize and classify an address role.

    Supported roles:
    - exchange
    - wallet
    - bridge
    - market_maker
    - unknown
    """

    if not isinstance(address_type, str):
        return "unknown"

    role = address_type.strip().lower()

    if role in KNOWN_ADDRESS_ROLES:
        return role

    return "unknown"
