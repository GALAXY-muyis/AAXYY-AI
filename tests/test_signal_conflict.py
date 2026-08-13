from signal_conflict import detect_signal_conflict


def test_aligned_buy_signal():
    result = detect_signal_conflict(
        signal="BUY",
        market_regime="BULLISH",
        momentum=10,
        volume_status="HIGH",
    )

    assert result["status"] == "ALIGNED"
    assert result["conflict_count"] == 0


def test_buy_against_bearish_market():
    result = detect_signal_conflict(
        signal="BUY",
        market_regime="BEARISH",
        momentum=10,
        volume_status="HIGH",
    )

    assert result["status"] == "CONFLICT"
    assert result["conflict_count"] == 1


def test_sell_against_bullish_market():
    result = detect_signal_conflict(
        signal="SELL",
        market_regime="BULLISH",
        momentum=-10,
        volume_status="HIGH",
    )

    assert result["status"] == "CONFLICT"
    assert result["conflict_count"] == 1


def test_buy_with_negative_momentum():
    result = detect_signal_conflict(
        signal="BUY",
        market_regime="BULLISH",
        momentum=-10,
        volume_status="HIGH",
    )

    assert result["status"] == "CONFLICT"
    assert result["conflict_count"] == 1


def test_low_volume_creates_conflict():
    result = detect_signal_conflict(
        signal="BUY",
        market_regime="BULLISH",
        momentum=10,
        volume_status="LOW",
    )

    assert result["status"] == "CONFLICT"
    assert result["conflict_count"] == 1
