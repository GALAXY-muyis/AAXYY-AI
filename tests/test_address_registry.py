from address_registry import AddressRegistry


def test_add_exchange_address():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xEXCHANGE",
        "exchange",
        "VERIFIED",
        "official_source",
    )

    assert result is True
    assert registry.get_role("0xEXCHANGE") == "exchange"


def test_add_wallet_address():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xWALLET",
        "wallet",
        "LIKELY",
        "on_chain_analysis",
    )

    assert result is True
    assert registry.get_role("0xWALLET") == "wallet"


def test_unknown_address_returns_unknown():
    registry = AddressRegistry()

    assert registry.get_role("0xUNKNOWN") == "unknown"


def test_invalid_role_is_rejected():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xADDRESS",
        "something_invalid",
        "VERIFIED",
    )

    assert result is False
    assert registry.get_role("0xADDRESS") == "unknown"


def test_empty_address_is_rejected():
    registry = AddressRegistry()

    result = registry.add_address(
        "",
        "exchange",
        "VERIFIED",
    )

    assert result is False


def test_has_address():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        "VERIFIED",
    )

    assert registry.has_address("0xEXCHANGE") is True
    assert registry.has_address("0xUNKNOWN") is False


def test_address_whitespace_is_normalized():
    registry = AddressRegistry()

    registry.add_address(
        "  0xEXCHANGE  ",
        "exchange",
        "VERIFIED",
    )

    assert registry.get_role("0xEXCHANGE") == "exchange"


def test_get_confidence():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        "VERIFIED",
    )

    assert registry.get_confidence("0xEXCHANGE") == "VERIFIED"


def test_get_source():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        "VERIFIED",
        "official_source",
    )

    assert registry.get_source("0xEXCHANGE") == "official_source"


def test_unknown_address_confidence():
    registry = AddressRegistry()

    assert registry.get_confidence("0xUNKNOWN") == "UNKNOWN"


def test_unknown_address_source():
    registry = AddressRegistry()

    assert registry.get_source("0xUNKNOWN") == ""


def test_invalid_confidence_is_rejected():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xADDRESS",
        "exchange",
        "CERTAIN",
    )

    assert result is False
    assert registry.has_address("0xADDRESS") is False
