"""
Helper functions for user activity evaluation and alert creation.
"""

from typing import List
from user_monitoring.models import UserEvent


def process_user_event(event: UserEvent, user_activity: dict) -> List[int]:
    """
    Processes a user event and returns alert codes based on rules:

    Withdrawals:
    • Code: 1100 : A withdrawal amount over 100.
    • Code: 30 : The user makes 3 consecutive withdrawals.

    Deposits:
    • Code: 300 : The user makes 3 consecutive deposits where each one.
    is larger than the previous deposit (withdrawals in between deposits can be ignored).
    • Code: 123 : The total amount deposited in a 30-second window exceeds 200.

    """
    alerts = []
    if event.type == "withdraw":
        user_activity[event.user_id]["withdrawals"].append(event)

        if float(event.amount) > 100:
            alerts.append(1100)

        if (
            len(user_activity[event.user_id]["withdrawals"]) >= 3
        ):  # not sure if it should stop at the first 3 or get activated at every iteration of 3
            three_consecutive_withdrawls = user_activity[event.user_id]["withdrawals"][
                -3:
            ]
            timestamps = [w.time for w in three_consecutive_withdrawls]
            if sorted(timestamps) == timestamps:
                alerts.append(30)

    if event.type == "deposit":
        float(event.amount)
        user_activity[event.user_id]["deposits"].append(event)

        if len(user_activity[event.user_id]["deposits"]) >= 3:
            three_increasing_deposits = user_activity[event.user_id]["deposits"][-3:]
            amounts = [d.amount for d in three_increasing_deposits]
            if amounts == sorted(amounts):
                alerts.append(300)

        deposits_window = 0.0
        for deposit in user_activity[event.user_id]["deposits"]:
            if event.time - deposit.time <= 30:
                deposits_window += float(deposit.amount)
            if deposits_window > 200:
                alerts.append(123)

    return alerts
