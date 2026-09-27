from address_intelligence import classify_address_role


def test_exchange_role():
    assert classify_address_role("exchange") == "exchange"


def test_wallet_role():
    assert classify_address_role("wallet") == "wallet"


def test_bridge_role():
    assert classify_address_role("bridge") == "bridge"


def test_market_maker_role():
    assert classify_address_role("market_maker") == "market_maker"


def test_unknown_role():
    assert classify_address_role("something_unknown") == "unknown"


def test_empty_role_is_unknown():
    assert classify_address_role("") == "unknown"


def test_non_string_role_is_unknown():
    assert classify_address_role(None) == "unknown"


def test_role_is_case_insensitive():
    assert classify_address_role("EXCHANGE") == "exchange"
