from address_registry import AddressRegistry


def test_add_exchange_address():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xEXCHANGE",
        "exchange",
    )

    assert result is True
    assert registry.get_role("0xEXCHANGE") == "exchange"


def test_add_wallet_address():
    registry = AddressRegistry()

    result = registry.add_address(
        "0xWALLET",
        "wallet",
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
    )

    assert result is False
    assert registry.get_role("0xADDRESS") == "unknown"


def test_empty_address_is_rejected():
    registry = AddressRegistry()

    result = registry.add_address(
        "",
        "exchange",
    )

    assert result is False


def test_has_address():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
    )

    assert registry.has_address("0xEXCHANGE") is True
    assert registry.has_address("0xUNKNOWN") is False


def test_address_whitespace_is_normalized():
    registry = AddressRegistry()

    registry.add_address(
        "  0xEXCHANGE  ",
        "exchange",
    )

    assert registry.get_role("0xEXCHANGE") == "exchange"
