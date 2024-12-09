"""
Implements /event endpoint
"""

import sys
from flask import Blueprint, current_app, request

from user_monitoring.models import UserEvent


print(sys.path)

api = Blueprint("api", __name__)

user_activity: dict = {}
alerts = []


@api.post("/event")
def handle_user_event() -> dict:
    "Handles user event"
    current_app.logger.info("Handling user event.")
    try:

        event = UserEvent(**request.json or {})

        if not event:
            raise ValueError("No request provided.")

        if event.type == "withdraw" and float(event.amount) > 100:
            alerts.append(1100)

        return {"alert": bool(alerts), "alert_codes": alerts, "user_id": event.user_id}
    except ValueError as e:
        current_app.logger.error(f"Value error: {e}")
        raise
