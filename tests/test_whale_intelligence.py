from address_registry import AddressRegistry
from whale_intelligence import Transfer, classify_transfer


def test_large_transfer_is_whale_transfer():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xSENDER",
        receiver="0xRECEIVER",
    )

    result = classify_transfer(transfer)

    assert result.classification == "WHALE_TRANSFER"
    assert result.confidence == 75


def test_small_transfer_is_normal_transfer():
    transfer = Transfer(
        token="ETH",
        amount_usd=50_000,
        sender="0xSENDER",
        receiver="0xRECEIVER",
    )

    result = classify_transfer(transfer)

    assert result.classification == "NORMAL_TRANSFER"
    assert result.confidence == 90


def test_negative_transfer_is_invalid():
    transfer = Transfer(
        token="ETH",
        amount_usd=-1,
        sender="0xSENDER",
        receiver="0xRECEIVER",
    )

    result = classify_transfer(transfer)

    assert result.classification == "INVALID_DATA"


def test_missing_token_is_invalid():
    transfer = Transfer(
        token="",
        amount_usd=250_000,
        sender="0xSENDER",
        receiver="0xRECEIVER",
    )

    result = classify_transfer(transfer)

    assert result.classification == "INVALID_DATA"


def test_missing_address_is_invalid():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="",
        receiver="0xRECEIVER",
    )

    result = classify_transfer(transfer)

    assert result.classification == "INVALID_DATA"


def test_same_sender_and_receiver_is_normal():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xSAME",
        receiver="0xSAME",
    )

    result = classify_transfer(transfer)

    assert result.classification == "NORMAL_TRANSFER"
    assert result.confidence == 100


def test_exchange_to_wallet_is_possible_accumulation():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xEXCHANGE",
        receiver="0xWALLET",
        sender_type="exchange",
        receiver_type="wallet",
    )

    result = classify_transfer(transfer)

    assert result.classification == "POSSIBLE_ACCUMULATION"
    assert result.confidence == 65


def test_wallet_to_exchange_is_possible_distribution():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xWALLET",
        receiver="0xEXCHANGE",
        sender_type="wallet",
        receiver_type="exchange",
    )

    result = classify_transfer(transfer)

    assert result.classification == "POSSIBLE_DISTRIBUTION"
    assert result.confidence == 65


def test_unknown_direction_is_whale_transfer():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xA",
        receiver="0xB",
        sender_type="bridge",
        receiver_type="market_maker",
    )

    result = classify_transfer(transfer)

    assert result.classification == "WHALE_TRANSFER"
    assert result.confidence == 75


def test_registry_can_identify_exchange_to_wallet():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        confidence="VERIFIED",
        chain="ethereum",
    )
    registry.add_address(
        "0xWALLET",
        "wallet",
        confidence="LIKELY",
        chain="ethereum",
    )

    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xEXCHANGE",
        receiver="0xWALLET",
        chain="ethereum",
    )

    result = classify_transfer(
        transfer,
        address_registry=registry,
    )

    assert result.classification == "POSSIBLE_ACCUMULATION"
    assert result.sender_attribution_confidence == "VERIFIED"
    assert result.receiver_attribution_confidence == "LIKELY"


def test_registry_can_identify_wallet_to_exchange():
    registry = AddressRegistry()

    registry.add_address(
        "0xWALLET",
        "wallet",
        confidence="LIKELY",
        chain="ethereum",
    )
    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        confidence="VERIFIED",
        chain="ethereum",
    )

    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xWALLET",
        receiver="0xEXCHANGE",
        chain="ethereum",
    )

    result = classify_transfer(
        transfer,
        address_registry=registry,
    )

    assert result.classification == "POSSIBLE_DISTRIBUTION"
    assert result.sender_attribution_confidence == "LIKELY"
    assert result.receiver_attribution_confidence == "VERIFIED"


def test_registry_role_overrides_unknown_transfer_role():
    registry = AddressRegistry()

    registry.add_address(
        "0xEXCHANGE",
        "exchange",
        confidence="VERIFIED",
        chain="ethereum",
    )
    registry.add_address(
        "0xWALLET",
        "wallet",
        confidence="LIKELY",
        chain="ethereum",
    )

    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xEXCHANGE",
        receiver="0xWALLET",
        sender_type="unknown",
        receiver_type="unknown",
        chain="ethereum",
    )

    result = classify_transfer(
        transfer,
        address_registry=registry,
    )

    assert result.classification == "POSSIBLE_ACCUMULATION"
    assert result.sender_attribution_confidence == "VERIFIED"
    assert result.receiver_attribution_confidence == "LIKELY"
