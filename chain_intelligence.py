"""
AAXYY AI - Chain Intelligence

Provides a controlled list of supported blockchain networks.

This module is used to distinguish addresses and transfers
across different blockchain networks.

It does not make trading decisions.
"""

SUPPORTED_CHAINS = {
    "ethereum",
    "bnb_chain",
    "solana",
    "base",
    "arbitrum",
}


def classify_chain(chain):
    """Return a normalized supported chain name."""

    if not isinstance(chain, str):
        return "unknown"

    normalized_chain = chain.strip().lower()

    if normalized_chain in SUPPORTED_CHAINS:
        return normalized_chain

    return "unknown"
