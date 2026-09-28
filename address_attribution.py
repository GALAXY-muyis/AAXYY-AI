"""
AAXYY AI - Address Attribution

Tracks how confident AAXYY is in an identified blockchain address role.

This module does not make trading decisions.
"""

from dataclasses import dataclass


VALID_CONFIDENCE_LEVELS = {
    "VERIFIED",
    "LIKELY",
    "UNKNOWN",
}


@dataclass
class AddressAttribution:
    address: str
    role: str
    confidence: str
    source: str = ""


def create_attribution(
    address,
    role,
    confidence,
    source="",
):
    """Create a validated address attribution."""

    if not isinstance(address, str) or not address.strip():
        return None

    if not isinstance(role, str) or not role.strip():
        return None

    if confidence not in VALID_CONFIDENCE_LEVELS:
        return None

    return AddressAttribution(
        address=address.strip(),
        role=role.strip().lower(),
        confidence=confidence,
        source=source.strip() if isinstance(source, str) else "",
  )
