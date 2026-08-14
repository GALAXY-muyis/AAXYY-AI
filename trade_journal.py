import csv
import os


JOURNAL_FILE = "trade_journal.csv"


def log_trade(
    pair,
    signal,
    confidence,
    entry_price,
    stop_loss,
    take_profit,
    leverage,
    risk_percent,
    result="OPEN",
    profit_loss=0.0,
):
    """Record an AAXYY AI trade or signal."""

    file_exists = os.path.exists(JOURNAL_FILE)

    with open(JOURNAL_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                [
                    "pair",
                    "signal",
                    "confidence",
                    "entry_price",
                    "stop_loss",
                    "take_profit",
                    "leverage",
                    "risk_percent",
                    "result",
                    "profit_loss",
                ]
            )

        writer.writerow(
            [
                pair,
                signal,
                confidence,
                entry_price,
                stop_loss,
                take_profit,
                leverage,
                risk_percent,
                result,
                profit_loss,
            ]
        )


def get_journal_file():
    """Return the journal filename."""

    return JOURNAL_FILE
