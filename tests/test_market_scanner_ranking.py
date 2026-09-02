from market_scanner import calculate_scan_score


def test_strong_market_gets_high_score():
    score = calculate_scan_score(
        confidence=90,
        trade_quality="STRONG",
        risk_reward=3,
        market_regime="BULLISH",
        conflict_status="ALIGNED",
    )

    assert score == 100


def test_conflicting_market_gets_lower_score():
    score = calculate_scan_score(
        confidence=90,
        trade_quality="STRONG",
        risk_reward=3,
        market_regime="BEARISH",
        conflict_status="CONFLICT",
    )

    assert score == 70


def test_weak_market_gets_low_score():
    score = calculate_scan_score(
        confidence=40,
        trade_quality="WEAK",
        risk_reward=1,
        market_regime="SIDEWAYS",
        conflict_status="ALIGNED",
    )

    assert score == 0
