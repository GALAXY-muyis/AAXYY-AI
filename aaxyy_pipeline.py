from market_regime import detect_market_regime
from trade_quality import calculate_trade_quality
from signal_conflict import detect_signal_conflict
from trade_decision import make_trade_decision
from position_sizer import calculate_position_size
from risk_targets import calculate_trade_targets
from risk_gate import check_risk_gate
from trading_guard import check_trading_guard


def run_aaxyy_pipeline(
    price,
    moving_average,
    volume,
    average_volume,
    signal,
    confidence,
    risk_reward,
    momentum,
    account_balance,
    risk_percent,
    entry_price,
    stop_loss,
    trades_today=0,
    consecutive_losses=0,
    daily_loss_percent=0,
):
    market = detect_market_regime(
        price,
        moving_average,
        momentum,
    )

    if volume > average_volume:
        volume_status = "HIGH"
    elif volume < average_volume:
        volume_status = "LOW"
    else:
        volume_status = "NORMAL"

    quality = calculate_trade_quality(
        signal=signal,
        confidence=confidence,
        risk_reward=risk_reward,
        momentum=momentum,
        volume_status=volume_status,
    )

    conflict = detect_signal_conflict(
        signal=signal,
        market_regime=market["regime"],
        momentum=momentum,
        volume_status=volume_status,
    )

    decision = make_trade_decision(
        signal=signal,
        confidence=confidence,
        trade_quality=quality["quality"],
        market_regime=market["regime"],
    )

    position_size = calculate_position_size(
        account_balance=account_balance,
        risk_percent=risk_percent,
        entry_price=entry_price,
        stop_loss=stop_loss,
    )

    targets = calculate_trade_targets(
        entry_price=entry_price,
        stop_loss=stop_loss,
        risk_reward_ratio=risk_reward,
        signal=signal,
    )

    
AAXYY-AI
Repository navigation
Code
Issues
Pull requests
Python application
fix: add take profit to risk gate #195
Annotations
1 error and 1 warning
build
failed 9 minutes ago in 15s
1s
1s
0s
8s
1s
1s
Run pytest
============================= test session starts ==============================
platform linux -- Python 3.10.21, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/runner/work/AAXYY-AI/AAXYY-AI
collected 122 items

test_data_validator.py ...                                               [  2%]
test_end_to_end_paper_trading.py F                                       [  3%]
tests/test_aaxyy_pipeline.py FFF                                         [  5%]
tests/test_end_to_end.py FFFF                                            [  9%]
tests/test_market_data.py ...                                            [ 11%]
tests/test_market_data_validator.py ......                               [ 16%]
tests/test_market_regime.py ...                                          [ 18%]
tests/test_market_scanner.py .......                                     [ 24%]
tests/test_market_scanner_analysis.py .                                  [ 25%]
tests/test_market_scanner_full_flow.py ..FFF                             [ 29%]
tests/test_market_scanner_integration.py .                               [ 30%]
tests/test_market_scanner_order.py ..                                    [ 31%]
tests/test_market_scanner_ranking.py ...                                 [ 34%]
tests/test_momentum.py ....                                              [ 37%]
tests/test_paper_trading_executor.py .............                       [ 48%]
tests/test_position_sizer.py ......                                      [ 53%]
tests/test_risk_gate.py FFFFFF                                           [ 58%]
tests/test_risk_manager.py ..                                            [ 59%]
tests/test_risk_targets.py ....                                          [ 63%]
tests/test_signal_conflict.py .....                                      [ 67%]
tests/test_signal_engine.py ........                                     [ 73%]
tests/test_trade_analyzer.py ..                                          [ 75%]
tests/test_trade_approval.py FF                                          [ 77%]
tests/test_trade_decision.py .....                                       [ 81%]
tests/test_trade_pipeline.py FF.FFFFFFFFFFFFF                            [ 94%]
tests/test_trade_quality.py ...                                          [ 96%]
tests/test_trading_guard.py ....                                         [100%]

=================================== FAILURES ===================================
______________________ test_end_to_end_paper_trading_flow ______________________

    def test_end_to_end_paper_trading_flow():
        price = 110
        moving_average = 100
        volume = 1500
        average_volume = 1000
        previous_price = 105
    
        analysis = analyze_market(
            price=price,
            moving_average=moving_average,
            volume=volume,
            average_volume=average_volume,
            previous_price=previous_price,
        )
    
>       result = run_aaxyy_pipeline(
            price=price,
            moving_average=moving_average,
            volume=volume,
            average_volume=average_volume,
            signal=analysis["signal"],
            confidence=analysis["confidence"],
            risk_reward=3,
            momentum=analysis["momentum"],
            account_balance=1000,
            risk_percent=2,
            entry_price=price,
            stop_loss=105,
        )

test_end_to_end_paper_trading.py:21: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 110, moving_average = 100, volume = 1500, average_volume = 1000
signal = 'BUY', confidence = 90, risk_reward = 3, momentum = 5
account_balance = 1000, risk_percent = 2, entry_price = 110, stop_loss = 105
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
___________________________ test_strong_buy_pipeline ___________________________

    def test_strong_buy_pipeline():
>       result = run_aaxyy_pipeline(
            price=110,
            moving_average=100,
            volume=1500,
            average_volume=1000,
            signal="BUY",
            confidence=90,
            risk_reward=3,
            momentum=10,
            account_balance=1000,
            risk_percent=2,
            entry_price=110,
            stop_loss=105,
        )

tests/test_aaxyy_pipeline.py:5: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 110, moving_average = 100, volume = 1500, average_volume = 1000
signal = 'BUY', confidence = 90, risk_reward = 3, momentum = 10
account_balance = 1000, risk_percent = 2, entry_price = 110, stop_loss = 105
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
________________________ test_conflicting_buy_pipeline _________________________

    def test_conflicting_buy_pipeline():
>       result = run_aaxyy_pipeline(
            price=90,
            moving_average=100,
            volume=1500,
            average_volume=1000,
            signal="BUY",
            confidence=90,
            risk_reward=3,
            momentum=10,
            account_balance=1000,
            risk_percent=2,
            entry_price=90,
            stop_loss=85,
        )

tests/test_aaxyy_pipeline.py:34: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 90, moving_average = 100, volume = 1500, average_volume = 1000
signal = 'BUY', confidence = 90, risk_reward = 3, momentum = 10
account_balance = 1000, risk_percent = 2, entry_price = 90, stop_loss = 85
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
______________________________ test_hold_pipeline ______________________________

    def test_hold_pipeline():
>       result = run_aaxyy_pipeline(
            price=100,
            moving_average=100,
            volume=1000,
            average_volume=1000,
            signal="HOLD",
            confidence=40,
            risk_reward=1,
            momentum=0,
            account_balance=1000,
            risk_percent=2,
            entry_price=100,
            stop_loss=95,
        )

tests/test_aaxyy_pipeline.py:57: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 100, moving_average = 100, volume = 1000, average_volume = 1000
signal = 'HOLD', confidence = 40, risk_reward = 1, momentum = 0
account_balance = 1000, risk_percent = 2, entry_price = 100, stop_loss = 95
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
__________________________ test_aaxyy_end_to_end_buy ___________________________

    def test_aaxyy_end_to_end_buy():
>       executor = run_end_to_end_test(
            signal="BUY",
            price=100,
            moving_average=99,
            volume=2000,
            average_volume=1000,
            previous_price=99,
        )

tests/test_end_to_end.py:74: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/test_end_to_end.py:29: in run_end_to_end_test
    result = run_aaxyy_pipeline(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 100, moving_average = 99, volume = 2000, average_volume = 1000
signal = 'BUY', confidence = 90, risk_reward = 3, momentum = 1
account_balance = 1000, risk_percent = 2, entry_price = 100, stop_loss = 98.0
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
__________________________ test_aaxyy_end_to_end_sell __________________________

    def test_aaxyy_end_to_end_sell():
>       executor = run_end_to_end_test(
            signal="SELL",
            price=100,
            moving_average=101,
            volume=2000,
            average_volume=1000,
            previous_price=101,
        )

tests/test_end_to_end.py:87: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/test_end_to_end.py:29: in run_end_to_end_test
    result = run_aaxyy_pipeline(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 100, moving_average = 101, volume = 2000, average_volume = 1000
signal = 'SELL', confidence = 90, risk_reward = 3, momentum = -1
account_balance = 1000, risk_percent = 2, entry_price = 100, stop_loss = 102.0
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
____________________ test_aaxyy_buy_trade_hits_take_profit _____________________

    def test_aaxyy_buy_trade_hits_take_profit():
>       executor = run_end_to_end_test(
            signal="BUY",
            price=100,
            moving_average=99,
            volume=2000,
            average_volume=1000,
            previous_price=99,
        )

tests/test_end_to_end.py:100: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/test_end_to_end.py:29: in run_end_to_end_test
    result = run_aaxyy_pipeline(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 100, moving_average = 99, volume = 2000, average_volume = 1000
signal = 'BUY', confidence = 90, risk_reward = 3, momentum = 1
account_balance = 1000, risk_percent = 2, entry_price = 100, stop_loss = 98.0
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
_____________________ test_aaxyy_sell_trade_hits_stop_loss _____________________

    def test_aaxyy_sell_trade_hits_stop_loss():
>       executor = run_end_to_end_test(
            signal="SELL",
            price=100,
            moving_average=101,
            volume=2000,
            average_volume=1000,
            previous_price=101,
        )

tests/test_end_to_end.py:122: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/test_end_to_end.py:29: in run_end_to_end_test
    result = run_aaxyy_pipeline(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 100, moving_average = 101, volume = 2000, average_volume = 1000
signal = 'SELL', confidence = 90, risk_reward = 3, momentum = -1
account_balance = 1000, risk_percent = 2, entry_price = 100, stop_loss = 102.0
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
__________________________ test_scanner_run_pipeline ___________________________

    def test_scanner_run_pipeline():
        scanner = MarketScanner(None)
    
        markets = [
            {
                "symbol": "BTC",
                "price": 110,
                "moving_average": 100,
                "volume": 2000,
                "average_volume": 1000,
                "previous_price": 105,
            }
        ]
    
        analyzed = scanner.analyze_markets(markets)
>       result = scanner.run_pipeline(analyzed)

tests/test_market_scanner_full_flow.py:68: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
market_scanner.py:105: in run_pipeline
    result = run_aaxyy_pipeline(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 110, moving_average = 100, volume = 2000, average_volume = 1000
signal = 'BUY', confidence = 90, risk_reward = 3, momentum = 5
account_balance = 1000, risk_percent = 2, entry_price = 110, stop_loss = 107.8
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
______________________ test_scanner_full_opportunity_flow ______________________

    def test_scanner_full_opportunity_flow():
        scanner = MarketScanner(None)
    
        markets = [
            {
                "symbol": "BTC",
                "price": 110,
                "moving_average": 100,
                "volume": 2000,
                "average_volume": 1000,
                "previous_price": 105,
            },
            {
                "symbol": "ETH",
                "price": 102,
                "moving_average": 100,
                "volume": 1000,
                "average_volume": 1000,
                "previous_price": 100,
            },
        ]
    
        analyzed = scanner.analyze_markets(markets)
>       pipeline_results = scanner.run_pipeline(analyzed)

tests/test_market_scanner_full_flow.py:103: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
market_scanner.py:105: in run_pipeline
    result = run_aaxyy_pipeline(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 110, moving_average = 100, volume = 2000, average_volume = 1000
signal = 'BUY', confidence = 90, risk_reward = 3, momentum = 5
account_balance = 1000, risk_percent = 2, entry_price = 110, stop_loss = 107.8
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
________________ test_scan_opportunities_returns_ranked_markets ________________

    def test_scan_opportunities_returns_ranked_markets():
        scanner = MarketScanner(None)
    
        markets = [
            {
                "symbol": "BTC",
                "price": 110,
                "moving_average": 100,
                "volume": 2000,
                "average_volume": 1000,
                "previous_price": 105,
            },
            {
                "symbol": "ETH",
                "price": 102,
                "moving_average": 100,
                "volume": 1000,
                "average_volume": 1000,
                "previous_price": 100,
            },
        ]
    
        scanner.scan = lambda symbols: markets
    
>       result = scanner.scan_opportunities(["BTC", "ETH"])

tests/test_market_scanner_full_flow.py:145: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
market_scanner.py:142: in scan_opportunities
    pipeline_results = self.run_pipeline(analyzed)
market_scanner.py:105: in run_pipeline
    result = run_aaxyy_pipeline(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

price = 110, moving_average = 100, volume = 2000, average_volume = 1000
signal = 'BUY', confidence = 90, risk_reward = 3, momentum = 5
account_balance = 1000, risk_percent = 2, entry_price = 110, stop_loss = 107.8
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def run_aaxyy_pipeline(
        price,
        moving_average,
        volume,
        average_volume,
        signal,
        confidence,
        risk_reward,
        momentum,
        account_balance,
        risk_percent,
        entry_price,
        stop_loss,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    ):
        market = detect_market_regime(
            price,
            moving_average,
            momentum,
        )
    
        if volume > average_volume:
            volume_status = "HIGH"
        elif volume < average_volume:
            volume_status = "LOW"
        else:
            volume_status = "NORMAL"
    
        quality = calculate_trade_quality(
            signal=signal,
            confidence=confidence,
            risk_reward=risk_reward,
            momentum=momentum,
            volume_status=volume_status,
        )
    
        conflict = detect_signal_conflict(
            signal=signal,
            market_regime=market["regime"],
            momentum=momentum,
            volume_status=volume_status,
        )
    
        decision = make_trade_decision(
            signal=signal,
            confidence=confidence,
            trade_quality=quality["quality"],
            market_regime=market["regime"],
        )
    
        position_size = calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
        )
    
        targets = calculate_trade_targets(
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_reward_ratio=risk_reward,
            signal=signal,
        )
    
>       risk_gate = check_risk_gate(
            signal=signal,
            risk_reward=risk_reward,
            stop_loss=stop_loss,
            entry_price=entry_price,
            position_size=position_size,
            conflict_status=conflict["status"],
            trade_quality=quality["quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

aaxyy_pipeline.py:77: TypeError
_________________________ test_strong_trade_is_allowed _________________________

    def test_strong_trade_is_allowed():
>       result = check_risk_gate(
            signal="BUY",
            risk_reward=3,
            stop_loss=95,
            entry_price=100,
            position_size=4,
            conflict_status="ALIGNED",
            trade_quality="STRONG",
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

tests/test_risk_gate.py:5: TypeError
_____________ test_trade_below_two_to_one_risk_reward_is_rejected ______________

    def test_trade_below_two_to_one_risk_reward_is_rejected():
>       result = check_risk_gate(
            signal="BUY",
            risk_reward=1.5,
            stop_loss=95,
            entry_price=100,
            position_size=4,
            conflict_status="ALIGNED",
            trade_quality="STRONG",
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

tests/test_risk_gate.py:20: TypeError
_____________________ test_zero_stop_distance_is_rejected ______________________

    def test_zero_stop_distance_is_rejected():
>       result = check_risk_gate(
            signal="BUY",
            risk_reward=3,
            stop_loss=100,
            entry_price=100,
            position_size=4,
            conflict_status="ALIGNED",
            trade_quality="STRONG",
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

tests/test_risk_gate.py:35: TypeError
_________________________ test_hold_signal_is_rejected _________________________

    def test_hold_signal_is_rejected():
>       result = check_risk_gate(
            signal="HOLD",
            risk_reward=3,
            stop_loss=95,
            entry_price=100,
            position_size=4,
            conflict_status="ALIGNED",
            trade_quality="STRONG",
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

tests/test_risk_gate.py:50: TypeError
______________________ test_conflicting_trade_is_rejected ______________________

    def test_conflicting_trade_is_rejected():
>       result = check_risk_gate(
            signal="BUY",
            risk_reward=3,
            stop_loss=95,
            entry_price=100,
            position_size=4,
            conflict_status="CONFLICT",
            trade_quality="STRONG",
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

tests/test_risk_gate.py:65: TypeError
_________________________ test_weak_trade_is_rejected __________________________

    def test_weak_trade_is_rejected():
>       result = check_risk_gate(
            signal="BUY",
            risk_reward=3,
            stop_loss=95,
            entry_price=100,
            position_size=4,
            conflict_status="ALIGNED",
            trade_quality="WEAK",
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

tests/test_risk_gate.py:80: TypeError
______________ test_trade_is_approved_when_all_safety_checks_pass ______________

    def test_trade_is_approved_when_all_safety_checks_pass():
        opportunity = {
            "signal": "BUY",
            "risk_reward": 3,
            "stop_loss": 95,
            "entry_price": 100,
            "position_size": 4,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = check_trade_approval(
            opportunity=opportunity,
            trades_today=1,
            consecutive_losses=0,
            daily_loss_percent=1,
        )

tests/test_trade_approval.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'signal': 'BUY', 'risk_reward': 3, 'stop_loss': 95, 'entry_price': 100, ...}
trades_today = 1, consecutive_losses = 0, daily_loss_percent = 1

    def check_trade_approval(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """Approve a trade only when all safety checks pass."""
    
>       risk_gate_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_approval.py:13: TypeError
_________________ test_trade_is_rejected_when_risk_gate_fails __________________

    def test_trade_is_rejected_when_risk_gate_fails():
        opportunity = {
            "signal": "BUY",
            "risk_reward": 1.5,
            "stop_loss": 95,
            "entry_price": 100,
            "position_size": 4,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = check_trade_approval(
            opportunity=opportunity,
            trades_today=1,
            consecutive_losses=0,
            daily_loss_percent=1,
        )

tests/test_trade_approval.py:36: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'signal': 'BUY', 'risk_reward': 1.5, 'stop_loss': 95, 'entry_price': 100, ...}
trades_today = 1, consecutive_losses = 0, daily_loss_percent = 1

    def check_trade_approval(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """Approve a trade only when all safety checks pass."""
    
>       risk_gate_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_approval.py:13: TypeError
_________ test_selected_opportunity_passes_risk_gate_and_trading_guard _________

    def test_selected_opportunity_passes_risk_gate_and_trading_guard():
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "position_size": 1,
            "risk_reward": 2.5,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

tests/test_trade_pipeline.py:19: TypeError
____________ test_approve_trade_opportunity_returns_safety_approved ____________

    def test_approve_trade_opportunity_returns_safety_approved():
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "position_size": 1,
            "risk_reward": 2.5,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = approve_trade_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
        )

tests/test_trade_pipeline.py:61: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
___________ test_approve_trade_opportunity_rejects_risk_gate_failure ___________

    def test_approve_trade_opportunity_rejects_risk_gate_failure():
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "position_size": 1,
            "risk_reward": 1.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = approve_trade_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
        )

tests/test_trade_pipeline.py:107: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
_________ test_approve_trade_opportunity_rejects_trading_guard_failure _________

    def test_approve_trade_opportunity_rejects_trading_guard_failure():
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "position_size": 1,
            "risk_reward": 2.5,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = approve_trade_opportunity(
            opportunity=opportunity,
            trades_today=3,
            consecutive_losses=0,
            daily_loss_percent=0,
        )

tests/test_trade_pipeline.py:130: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 3, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
____________ test_approved_opportunity_can_be_sent_to_paper_trading ____________

    def test_approved_opportunity_can_be_sent_to_paper_trading():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "take_profit": 3250,
            "position_size": 0.1,
            "risk_reward": 2.5,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:156: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
____________ test_rejected_opportunity_does_not_open_paper_position ____________

    def test_rejected_opportunity_does_not_open_paper_position():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "take_profit": 3250,
            "position_size": 0.1,
            "risk_reward": 1.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:186: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
__________ test_trading_guard_rejection_does_not_open_paper_position ___________

    def test_trading_guard_rejection_does_not_open_paper_position():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "take_profit": 3250,
            "position_size": 0.1,
            "risk_reward": 2.5,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=3,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:214: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 3, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
____________ test_paper_position_preserves_opportunity_risk_targets ____________

    def test_paper_position_preserves_opportunity_risk_targets():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "SOLUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 150,
            "stop_loss": 145,
            "take_profit": 165,
            "position_size": 0.1,
            "risk_reward": 3.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:242: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'SOLUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
_____________ test_approved_sell_opportunity_opens_paper_position ______________

    def test_approved_sell_opportunity_opens_paper_position():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "SOLUSDT",
            "valid": True,
            "signal": "SELL",
            "confidence": 95,
            "entry_price": 150,
            "stop_loss": 155,
            "take_profit": 135,
            "position_size": 0.1,
            "risk_reward": 3.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:272: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'SOLUSDT', 'valid': True, 'signal': 'SELL', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
________________ test_paper_execution_uses_risk_based_quantity _________________

    def test_paper_execution_uses_risk_based_quantity():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "BTCUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 100,
            "stop_loss": 95,
            "take_profit": 110,
            "position_size": 999,
            "risk_reward": 2.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:304: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'BTCUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
_____________ test_invalid_stop_loss_does_not_open_paper_position ______________

    def test_invalid_stop_loss_does_not_open_paper_position():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 3000,
            "take_profit": 3300,
            "position_size": 0.1,
            "risk_reward": 3.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:333: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
__________ test_invalid_starting_balance_does_not_open_paper_position __________

    def test_invalid_starting_balance_does_not_open_paper_position():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "take_profit": 3250,
            "position_size": 0.1,
            "risk_reward": 2.5,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
        try:
>           result = execute_approved_opportunity(
                opportunity=opportunity,
                trades_today=0,
                consecutive_losses=0,
                daily_loss_percent=0,
                risk_percent=1.0,
                starting_balance=0,
            )

tests/test_trade_pipeline.py:362: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
__________ test_buy_opportunity_with_wrong_side_stop_loss_is_rejected __________

    def test_buy_opportunity_with_wrong_side_stop_loss_is_rejected():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 3100,
            "take_profit": 3300,
            "position_size": 0.1,
            "risk_reward": 2.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
        try:
>           result = execute_approved_opportunity(
                opportunity=opportunity,
                trades_today=0,
                consecutive_losses=0,
                daily_loss_percent=0,
                risk_percent=1.0,
                starting_balance=1000,
            )

tests/test_trade_pipeline.py:392: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
_________ test_sell_opportunity_with_wrong_side_stop_loss_is_rejected __________

    def test_sell_opportunity_with_wrong_side_stop_loss_is_rejected():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "SELL",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "take_profit": 2700,
            "position_size": 0.1,
            "risk_reward": 2.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:421: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'SELL', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
_________ test_buy_opportunity_with_wrong_side_take_profit_is_rejected _________

    def test_buy_opportunity_with_wrong_side_take_profit_is_rejected():
        from trade_pipeline import execute_approved_opportunity
    
        opportunity = {
            "symbol": "ETHUSDT",
            "valid": True,
            "signal": "BUY",
            "confidence": 95,
            "entry_price": 3000,
            "stop_loss": 2900,
            "take_profit": 2800,
            "position_size": 0.1,
            "risk_reward": 2.0,
            "conflict_status": "ALIGNED",
            "trade_quality": "STRONG",
        }
    
>       result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )

tests/test_trade_pipeline.py:449: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
trade_pipeline.py:125: in execute_approved_opportunity
    approval = approve_trade_opportunity(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

opportunity = {'symbol': 'ETHUSDT', 'valid': True, 'signal': 'BUY', 'confidence': 95, ...}
trades_today = 0, consecutive_losses = 0, daily_loss_percent = 0

    def approve_trade_opportunity(
        opportunity,
        trades_today,
        consecutive_losses,
        daily_loss_percent,
    ):
        """
        Run a selected opportunity through AAXYY's safety gates.
    
        No exchange order is placed here.
        """
    
        if not opportunity.get("valid", False):
            return {
                "approved": False,
                "reason": "INVALID_OPPORTUNITY",
            }
    
>       risk_result = check_risk_gate(
            signal=opportunity["signal"],
            risk_reward=opportunity["risk_reward"],
            stop_loss=opportunity["stop_loss"],
            entry_price=opportunity["entry_price"],
            position_size=opportunity["position_size"],
            conflict_status=opportunity["conflict_status"],
            trade_quality=opportunity["trade_quality"],
        )
E       TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'

trade_pipeline.py:79: TypeError
=========================== short test summary info ============================
FAILED test_end_to_end_paper_trading.py::test_end_to_end_paper_trading_flow - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_aaxyy_pipeline.py::test_strong_buy_pipeline - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_aaxyy_pipeline.py::test_conflicting_buy_pipeline - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_aaxyy_pipeline.py::test_hold_pipeline - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_end_to_end.py::test_aaxyy_end_to_end_buy - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_end_to_end.py::test_aaxyy_end_to_end_sell - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_end_to_end.py::test_aaxyy_buy_trade_hits_take_profit - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_end_to_end.py::test_aaxyy_sell_trade_hits_stop_loss - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_market_scanner_full_flow.py::test_scanner_run_pipeline - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_market_scanner_full_flow.py::test_scanner_full_opportunity_flow - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_market_scanner_full_flow.py::test_scan_opportunities_returns_ranked_markets - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_risk_gate.py::test_strong_trade_is_allowed - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_risk_gate.py::test_trade_below_two_to_one_risk_reward_is_rejected - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_risk_gate.py::test_zero_stop_distance_is_rejected - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_risk_gate.py::test_hold_signal_is_rejected - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_risk_gate.py::test_conflicting_trade_is_rejected - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_risk_gate.py::test_weak_trade_is_rejected - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_approval.py::test_trade_is_approved_when_all_safety_checks_pass - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_approval.py::test_trade_is_rejected_when_risk_gate_fails - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_selected_opportunity_passes_risk_gate_and_trading_guard - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_approve_trade_opportunity_returns_safety_approved - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_approve_trade_opportunity_rejects_risk_gate_failure - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_approve_trade_opportunity_rejects_trading_guard_failure - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_approved_opportunity_can_be_sent_to_paper_trading - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_rejected_opportunity_does_not_open_paper_position - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_trading_guard_rejection_does_not_open_paper_position - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_paper_position_preserves_opportunity_risk_targets - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_approved_sell_opportunity_opens_paper_position - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_paper_execution_uses_risk_based_quantity - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_invalid_stop_loss_does_not_open_paper_position - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_invalid_starting_balance_does_not_open_paper_position - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_buy_opportunity_with_wrong_side_stop_loss_is_rejected - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_sell_opportunity_with_wrong_side_stop_loss_is_rejected - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
FAILED tests/test_trade_pipeline.py::test_buy_opportunity_with_wrong_side_take_profit_is_rejected - TypeError: check_risk_gate() missing 1 required positional argument: 'take_profit'
======================== 34 failed, 88 passed in 0.87s =========================
Error: Process completed with exit code 1.

    trading_guard = check_trading_guard(
        trades_today=trades_today,
        consecutive_losses=consecutive_losses,
        daily_loss_percent=daily_loss_percent,
    )

    if signal == "HOLD":
        final_decision = "WAIT"
    elif conflict["status"] == "CONFLICT":
        final_decision = "CAUTION"
    elif not trading_guard["allowed"]:
        final_decision = "NO TRADE"
    elif not risk_gate["allowed"]:
        final_decision = "NO TRADE"
    else:
        final_decision = decision["decision"]

    return {
        "market_regime": market["regime"],
        "volume_status": volume_status,
        "trade_quality": quality,
        "conflict": conflict,
        "decision": decision,
        "position_size": position_size,
        "targets": targets,
        "risk_gate": risk_gate,
        "trading_guard": trading_guard,
        "final_decision": final_decision,
    }
