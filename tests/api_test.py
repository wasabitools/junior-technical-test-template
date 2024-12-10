from flask.testing import FlaskClient


def test_handle_user_event_success(client: FlaskClient) -> None:
    """
    Tests the successful handling of a user event.
    """
    payload = {"type": "deposit", "amount": "100", "user_id": 1, "time": 0}
    payload = {"type": "deposit", "amount": "100", "user_id": 1, "time": 0}
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert response.json == {"alert": False, "alert_codes": [], "user_id": 1}


def test_handle_large_withdrawal(client: FlaskClient) -> None:
    """
    Tests triggering the 1100 alert for a withdrawal over 100.
    """
    payload = {"type": "withdraw", "amount": "120.00", "user_id": 1, "time": 10}
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert response.json == {"alert": True, "alert_codes": [1100], "user_id": 1}


def test_three_consecutive_withdrawals(client: FlaskClient) -> None:
    """
    Tests triggering 30 alert for three consecutive withdrawals.
    """
    events = [
        {"type": "withdraw", "amount": "50.00", "user_id": 1, "time": 1},
        {"type": "withdraw", "amount": "30.00", "user_id": 1, "time": 2},
        {"type": "withdraw", "amount": "20.00", "user_id": 1, "time": 3},
    ]

    for event in events:
        response = client.post("/event", json=event)

    response = client.post("/event", json=events[-1])
    assert response.status_code == 200
    assert response.json == {"alert": True, "alert_codes": [30], "user_id": 1}


def test_consecutive_increasing_deposits(client: FlaskClient) -> None:
    """
    Tests triggering 300 alert for consecutive increasing deposits.
    """
    events = [
        {"type": "deposit", "amount": "10", "user_id": 1, "time": 1},
        {"type": "deposit", "amount": "11", "user_id": 1, "time": 1},
    ]

    for event in events:
        response = client.post("/event", json=event)

    response = client.post(
        "/event", json={"type": "deposit", "amount": "13", "user_id": 1, "time": 1}
    )
    assert response.status_code == 200
    assert response.json == {"alert": True, "alert_codes": [300], "user_id": 1}
