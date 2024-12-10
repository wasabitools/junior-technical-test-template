from flask.testing import FlaskClient


def test_handle_user_event_success(client: FlaskClient) -> None:
    """
    Tests the successful handling of a user event.
    """
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


def test_deposits_within_window(client: FlaskClient) -> None:
    """
    Tests triggering 123 alert for total deposits within a 30-second window.
    """
    events = [
        {"type": "deposit", "amount": "100.00", "user_id": 1, "time": 1},
        {"type": "deposit", "amount": "120.00", "user_id": 1, "time": 5},
    ]

    for event in events:
        response = client.post("/event", json=event)

    response = client.post(
        "/event", json={"type": "deposit", "amount": "90.00", "user_id": 1, "time": 10}
    )
    assert response.status_code == 200
    assert response.json == {"alert": True, "alert_codes": [123], "user_id": 1}


def test_handle_user_event_no_payload(client: FlaskClient) -> None:
    """
    Tests the handling of no payload provided.
    """
    payload = {}
    response = client.post("/event", json=payload)
    assert response.json == {"Error": "No payload provided"}


def test_handle_user_event_bad_payload(client: FlaskClient) -> None:
    """
    Tests the handling of an invalid payload.
    """
    payload = {"type": 4, "amount": "100", "user_id": 1, "time": 0}
    response = client.post("/event", json=payload)
    assert response.json == {"Error": "Invalid payload"}


def test_combined_alerts(client: FlaskClient) -> None:
    """
    Tests triggering combined alerts for withdrawals and deposits.
    """
    events = [
        {"type": "withdraw", "amount": "120.00", "user_id": 1, "time": 1},
        {"type": "deposit", "amount": "100.00", "user_id": 1, "time": 2},
        {"type": "deposit", "amount": "150.00", "user_id": 1, "time": 3},
    ]

    for event in events:
        client.post("/event", json=event)

    final_response = client.post("/event", json=events[-1])
    assert final_response.status_code == 200
    assert final_response.json == {
        "alert": True,
        "alert_codes": [1100, 123],
        "user_id": 1,
    }
