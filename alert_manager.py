from signal_formatter import format_signal


def create_alert(signal_data):
    """
    Create an AAXYY AI alert from signal data.
    """

    message = format_signal(signal_data)

    return {
        "type": "AAXYY_SIGNAL",
        "message": message,
        "sent": False,
    }


def mark_alert_sent(alert):
    """
    Mark an alert as sent.
    """

    alert["sent"] = True

    return alert
