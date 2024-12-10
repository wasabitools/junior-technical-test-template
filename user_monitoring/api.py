"""
Implements /event endpoint
"""

from flask import Blueprint, current_app, request

from user_monitoring.models import Alerts, UserEvent
from user_monitoring.utils import process_user_event

api = Blueprint("api", __name__)

user_activity: dict[int, dict[str, list[UserEvent]]] = {}


@api.post("/event")
def handle_user_event() -> dict:
    "Handles user event and returns an alert response"
    current_app.logger.info("Handling user event.")
    current_app.logger.info(f"User activity: {user_activity}")

    try:
        event = UserEvent(**request.json or {})

        if not event:
            raise ValueError("No request provided.")

        if event.user_id not in user_activity:
            user_activity[event.user_id] = {"withdrawals": [], "deposits": []}

        alerts = process_user_event(event, user_activity)
        current_app.logger.info(f"Alerts:{alerts}")

        response = Alerts(alert=bool(alerts), alert_codes=alerts, user_id=event.user_id)

        current_app.logger.info(
            f"Response for user {event.user_id}: {response.model_dump_json()}"
        )

        return response.model_dump()
    except ValueError as e:
        current_app.logger.error(f"Value error: {e}")
        raise


# TODO : / add tests / edit README
