from whale_intelligence import Transfer, classify_transfer


def test_large_transfer_is_detected_as_whale_transfer():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xAAA",
        receiver="0xBBB",
    )

    result = classify_transfer(transfer)

    assert result.classification == "WHALE_TRANSFER"
    assert result.confidence == 75


def test_small_transfer_is_normal():
    transfer = Transfer(
        token="ETH",
        amount_usd=50_000,
        sender="0xAAA",
        receiver="0xBBB",
    )

    result = classify_transfer(transfer)

    assert result.classification == "NORMAL_TRANSFER"


def test_negative_transfer_is_invalid():
    transfer = Transfer(
        token="ETH",
        amount_usd=-100,
        sender="0xAAA",
        receiver="0xBBB",
    )

    result = classify_transfer(transfer)

    assert result.classification == "INVALID_DATA"


def test_missing_token_is_invalid():
    transfer = Transfer(
        token="",
        amount_usd=250_000,
        sender="0xAAA",
        receiver="0xBBB",
    )

    result = classify_transfer(transfer)

    assert result.classification == "INVALID_DATA"


def test_missing_address_is_invalid():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="",
        receiver="0xBBB",
    )

    result = classify_transfer(transfer)

    assert result.classification == "INVALID_DATA"


def test_same_sender_and_receiver_is_normal():
    transfer = Transfer(
        token="ETH",
        amount_usd=500_000,
        sender="0xAAA",
        receiver="0xAAA",
    )

    result = classify_transfer(transfer)

    assert result.classification == "NORMAL_TRANSFER"
