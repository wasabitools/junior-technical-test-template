# Technical Test - Junior Back End Engineer

## User Activity Tracker

an API endpoint called /event that receives a payload representing a user's action (like a deposit or withdrawal). Based on the activity in the payload, your endpoint should check against some predefined rules to determine if an alert should be raised.
Here's the expected payload format:

```json
{
"type": "deposit",
"amount": "42.00",
"user_id": 1,
"time": 10
}
```

#### Payload

• type: str The type of user action, either deposit or withdraw.

• amount: str The amount of money the user is depositing or withdrawing.

• user_id: int A unique identifier for the user.

• time: int The timestamp of the action (this value is always increasing).

The response should look like this:

```json
{
"alert": true,
"alert_codes": [30, 123],
"user_id": 1
}
```

#### Expected behaviour

You'll be checking for these conditions to trigger alerts:

• alert: Should be true if any alert codes are triggered, otherwise false.

• alert_codes: A list of alert codes that have been triggered (if any)

• user_id: The user_id of the user whose action was processed

#### Alert codes

| Action    | Code     | Description                                   |
| :-------- | :------- | :-------------------------------------------- |
| `Withdraw`| `1100`   | A withdrawal amount over 100                  |
| :-------- | :------- | :-------------------------------------------- |
| `Withdraw`| `30`     | The user makes 3 consecutive withdrawals      |
| :-------- | :------- | :-------------------------------------------- |
| `Deposit` | `300`    | The user makes 3 consecutive deposits where each one is larger than the previous deposit (withdrawals in between deposits can be ignored).      |
| `Deposit` | `123`    | The total amount deposited in a 30-second window exceeds 200      |

### Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/) for dependency management

### Install dependencies

```sh
poetry install
```

### Start API server

```sh
make run
```

### Run tests

```sh
make test
```

## Testing

```sh
curl -XPOST 'http://127.0.0.1:5000/event' -H 'Content-Type: application/json' \
-d '{"type": "deposit", "amount": "110", "user_id": 1, "time": 1}'
```

# Solution

#### File Structure

```bash
user_monitoring/
│
├── models.py      # Defines the data models and validation schemas
├── utils.py       # Contains helper functions for event processing and alert creation
└── api.py         # Implements the Flask API endpoint for handling user events
```

#### models.py

This file defines the data models used to represent user events and alerts. The UserEvent class and Alerts class are implemented using Pydantic for data validation.
Classes and Functions:

- UserEvent: Defines the schema for user events (withdrawals or deposits).
  - type: The type of event, either "withdraw" or "deposit".
  - amount: The amount of money involved in the event.
  - user_id: The unique identifier of the user.
  - time: The timestamp of when the event occurred.
  - validate_amount: A custom validator that ensures the amount is in a valid format (can be converted to a float).

- Alerts: Defines the schema for the response object containing alerts.
  - alert: A boolean indicating whether any alert was triggered.
  - alert_codes: A list of integer codes indicating specific alerts triggered by the event.
  - user_id: The unique identifier of the user associated with the alerts.

#### utils.py

This file contains helper functions for processing user events and generating alert codes based on specific criteria. It evaluates the user activity, determines the appropriate alerts, and returns them. There are individual functions that validate if their designated check is True or False (`check_three_consecutive_withdrawals`, `check_increasing_deposits`, `check_deposits_window`). The logic for processing the withdrawals and deposits has been separated so the relevant alerts are returned.

### api.py

This file defines the Flask API that handles incoming user event data, processes it using the utility functions, and returns the appropriate alert responses. The POST endpoint `/event` handles incoming user events.It reads the JSON payload from the request, validates it using the UserEvent model, and processes the event using the `process_user_event()` function from `utils.py`. If any alerts are triggered, it stores them as a set and it returns a JSON response containing the unique alert codes. If no payload is provided or if there is a validation error, an error message is returned.
