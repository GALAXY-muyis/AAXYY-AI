from address_registry import AddressRegistry


def test_add_exchange_address():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xEXCHANGE",
        "exchange",
        confidence="VERIFIED",
        source="official_source",
        chain="ethereum",
    )

    assert result is True
    assert registry.get_role("0xEXCHANGE", "ethereum") == "exchange"


def test_add_wallet_address():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xWALLET",
        "wallet",
        confidence="LIKELY",
        source="wallet_source",
        chain="ethereum",
    )

    assert result is True
    assert registry.get_role("0xWALLET", "ethereum") == "wallet"


def test_reject_invalid_address():
    registry = AddressRegistry()

    result = registry.add_address(
        "",
        "exchange",
        chain="ethereum",
    )

    assert result is False


def test_reject_unknown_role():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xUNKNOWN",
        "unknown",
        chain="ethereum",
    )

    assert result is False


def test_has_address():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        chain="ethereum",
    )

    assert registry.has_address("0xEXCHANGE", "ethereum") is True
    assert registry.has_address("0xMISSING", "ethereum") is False


def test_address_whitespace_is_normalized():
    registry = AddressRegistry()

    registry.add_address(
        "  0xEXCHANGE  ",
        "exchange",
        confidence="VERIFIED",
        source="official_source",
        chain="ethereum",
    )

    assert registry.get_role("0xEXCHANGE", "ethereum") == "exchange"


def test_get_confidence():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        confidence="VERIFIED",
        source="official_source",
        chain="ethereum",
    )

    assert registry.get_confidence("0xEXCHANGE", "ethereum") == "VERIFIED"


def test_get_source():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        confidence="VERIFIED",
        source="official_source",
        chain="ethereum",
    )

    assert registry.get_source("0xEXCHANGE", "ethereum") == "official_source"


def test_different_chains_are_separate():
    registry = AddressRegistry()

    registry.add_address(
        "0xSAME",
        "exchange",
        chain="ethereum",
    )

    registry.add_address(
        "0xSAME",
        "wallet",
        chain="base",
    )

    assert registry.get_role("0xSAME", "ethereum") == "exchange"
    assert registry.get_role("0xSAME", "base") == "wallet"
