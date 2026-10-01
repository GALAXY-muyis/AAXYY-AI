from whale_intelligence import Transfer, classify_transfer


def test_whale_assessment_preserves_transfer_timestamp():
    transfer = Transfer(
        token="ETH",
        amount_usd=250_000,
        sender="0xEXCHANGE",
        receiver="0xWALLET",
        timestamp="2026-09-29T11:30:00",
        sender_type="exchange",
        receiver_type="wallet",
    )

    result = classify_transfer(transfer)

    assert result.classification == "POSSIBLE_ACCUMULATION"
    assert result.timestamp == "2026-09-29T11:30:00"
