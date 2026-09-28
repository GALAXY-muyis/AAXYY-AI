from address_attribution import create_attribution


def test_verified_attribution():
    result = create_attribution(
        "0xEXCHANGE",
        "exchange",
        "VERIFIED",
        "official_source",
    )

    assert result is not None
    assert result.address == "0xEXCHANGE"
    assert result.role == "exchange"
    assert result.confidence == "VERIFIED"
    assert result.source == "official_source"


def test_likely_attribution():
    result = create_attribution(
        "0xWALLET",
        "wallet",
        "LIKELY",
        "on_chain_analysis",
    )

    assert result is not None
    assert result.confidence == "LIKELY"


def test_unknown_attribution():
    result = create_attribution(
        "0xUNKNOWN",
        "wallet",
        "UNKNOWN",
    )

    assert result is not None
    assert result.confidence == "UNKNOWN"


def test_empty_address_is_rejected():
    result = create_attribution(
        "",
        "exchange",
        "VERIFIED",
    )

    assert result is None


def test_empty_role_is_rejected():
    result = create_attribution(
        "0xADDRESS",
        "",
        "VERIFIED",
    )

    assert result is None


def test_invalid_confidence_is_rejected():
    result = create_attribution(
        "0xADDRESS",
        "exchange",
        "CERTAIN",
    )

    assert result is None


def test_role_is_normalized():
    result = create_attribution(
        "0xADDRESS",
        "EXCHANGE",
        "VERIFIED",
    )

    assert result is not None
    assert result.role == "exchange"


def test_non_string_source_is_safe():
    result = create_attribution(
        "0xADDRESS",
        "wallet",
        "LIKELY",
        None,
    )

    assert result is not None
    assert result.source == ""
