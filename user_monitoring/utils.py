"""
Helper functions for user activity evaluation and alert creation.
"""

from typing import List
from user_monitoring.models import UserEvent


def process_user_event(event: UserEvent, user_activity: dict) -> List[int]:
    """
    Processes a user event and returns alert codes based on rules.
    """
    alerts = []

    if event.type == "withdraw":
        alerts.extend(process_withdrawal(event, user_activity))
    if event.type == "deposit":
        alerts.extend(process_deposit(event, user_activity))

    return alerts


def process_withdrawal(event: UserEvent, user_activity: dict) -> List[int]:
    """
    Processes withdrawal events and returns alert codes.

    Withdrawals:
    • Code: 1100 : A withdrawal amount over 100.
    • Code: 30 : The user makes 3 consecutive withdrawals.
    """
    withdrawals_alerts = []
    withdrawals_activity = user_activity[event.user_id]["withdrawals"]
    withdrawals_activity.append(event)

    if float(event.amount) > 100:
        withdrawals_alerts.append(1100)
    if check_three_consecutive_withdrawals(withdrawals_activity):
        withdrawals_alerts.append(30)

    return withdrawals_alerts


def process_deposit(event: UserEvent, user_activity: dict) -> List[int]:
    """
    Processes deposit events and returns alert codes.

    Deposits:
    • Code: 300 : The user makes 3 consecutive deposits where each one.
    is larger than the previous deposit (withdrawals in between deposits can be ignored).
    • Code: 123 : The total amount deposited in a 30-second window exceeds 200.
    """
    deposits_alerts = []
    deposits_activity = user_activity[event.user_id]["deposits"]
    deposits_activity.append(event)

    if check_increasing_deposits(deposits_activity):
        deposits_alerts.append(300)

    if check_deposits_window(deposits_activity, event.time):
        deposits_alerts.append(123)

    return deposits_alerts


def check_three_consecutive_withdrawals(withdrawals: List[UserEvent]) -> bool:
    "Checks for the last three consecutive withdrawals from a user event."
    if len(withdrawals) < 3:
        return False

    timestamps = [w.time for w in withdrawals[-3:]]
    return sorted(timestamps) == timestamps


def check_increasing_deposits(deposits: List[UserEvent]) -> bool:
    "Checks for the last three deposits with icnreasing amounts from a user event."
    if len(deposits) < 3:
        return False

    amounts = [float(d.amount) for d in deposits[-3:]]
    return amounts == sorted(amounts) and len(set(amounts)) == len(amounts)


def check_deposits_window(deposits: List[UserEvent], event_time: int) -> bool:
    "Checks for the total amount of deposits within a 30s window is over 200."
    total_amount = sum(
        float(deposit.amount) for deposit in deposits if event_time - deposit.time <= 30
    )
    return total_amount > 200
