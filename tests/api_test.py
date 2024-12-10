from flask.testing import FlaskClient


def test_handle_user_event_success(client: FlaskClient) -> None:
    """
    Tests the successful handling of a user event.
    """
    payload = {
        "type": "deposit",
        "amount": "10.00",
        "user_id": 1,
        "time": 0
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert response.json == {"alert": False, "alert_codes": [], "user_id": 1}
