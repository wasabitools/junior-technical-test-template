"""
Implements /event endpoint
"""

import sys
from flask import Blueprint, current_app, request

# from user_monitoring.models import UserEvent

print(sys.path)

api = Blueprint("api", __name__)

user_activity: dict = {}
alerts = []


@api.post("/event")
def handle_user_event() -> dict:
    "Handles user event"
    current_app.logger.info("Handling user event.")
    try:
        req = request.get_json()
        event_type = req.get("type")
        amount = req.get("amount")
        user_id = req.get("user_id")
        timestamp = req.get("time")

        if not req:
            raise ValueError("No request provided.")

        if event_type == "withdraw" and float(amount) > 100:
            alerts.append(1100)

        return {"alert": bool(alerts), "alert_codes": alerts, "user_id": user_id}
    except ValueError as e:
        current_app.logger.error(f"Value error: {e}")
        raise
