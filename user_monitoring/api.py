"""
Implements /event endpoint
"""

from flask import Blueprint, current_app, request


api = Blueprint("api", __name__)


@api.post("/event")
def handle_user_event() -> dict:
    "Handles user event"
    current_app.logger.info("Handling user event.")
    try:
        req = request.get_json()

        if not req:
            raise ValueError("No request provided.")

        user_id = req["user_id"]
        event_type = req["type"]
        amount = req["amount"]
        timestamp = req["time"]

        if not all(key in req for key in ["type", "amount", "user_id", "time"]):
            raise KeyError("Missing required fields")

        return {
            "event_type": event_type,
            "amount": amount,
            "user_id": user_id,
            "timestamp": timestamp,
        }
    except ValueError as e:
        current_app.logger.error(f"Value error: {e}")
        raise
