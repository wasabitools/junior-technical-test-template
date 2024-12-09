"""
Implements /event endpoint
"""
from flask import Blueprint, current_app, request


api = Blueprint("api", __name__)


@api.post("/event")
def handle_user_event() -> dict:
    "Handles user event"
    current_app.logger.info("Handling user event")

    req = request.get_json()

    user_id = req["user_id"]
    event_type = req["type"]
    amount = req["amount"]
    timestamp = req["time"]

    return {
        "event_type": event_type,
        "amount": amount,
        "user_id": user_id,
        "timestamp": timestamp,
    }
