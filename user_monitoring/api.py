"""
Implements /event endpoint
"""

from flask import Blueprint, current_app, request

from user_monitoring.models import Alerts, UserEvent

api = Blueprint("api", __name__)

user_activity: dict = {}
alerts = []


@api.post("/event")
def handle_user_event() -> dict:
    "Handles user event and returns an alert response"
    current_app.logger.info("Handling user event.")
    try:
        event = UserEvent(**request.json or {})

        if not event:
            raise ValueError("No request provided.")

        if event.user_id not in user_activity:
            user_activity[event.user_id] = {"withdrawals": [], "deposits": []}

        if event.type == "withdraw" and float(event.amount) > 100:
            alerts.append(1100)

        user_activity[event.user_id]["withdrawals"].append(event)

        if event.type == "withdraw" and (
            len(user_activity[event.user_id]["withdrawals"]) == 3
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

        if (
            len(user_activity[event.user_id]["deposits"]) == 3
        ):  # again not sure as above
            three_increasing_deposits = user_activity[event.user_id]["deposits"][-3:]
            amounts = [d.amount for d in three_increasing_deposits]
            if amounts == sorted(
                amounts
            ):  # needs refactoring as it appends 300 even for the same amount * 3
                alerts.append(300)

        deposits_window = 0.0
        for deposit in user_activity[event.user_id]["deposits"]:
            if event.time - deposit.time <= 30:
                deposits_window += float(deposit.amount)
            if deposits_window > 200:
                alerts.append(123)

        response = Alerts(alert=bool(alerts), alert_codes=alerts, user_id=event.user_id)

        current_app.logger.info(
            f"Response for user {event.user_id}: {response.model_dump_json()}"
        )

        return response.model_dump()
    except ValueError as e:
        current_app.logger.error(f"Value error: {e}")
        raise


# TODO : fix persisting user_id / refactor to separate concerns / add tests / edit README
