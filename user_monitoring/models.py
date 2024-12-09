"""
Defines the schema
"""

from pydantic import BaseModel, Field, field_validator


class UserEvent(BaseModel):
    """
    Defines the schema for the user event object.
    """

    type: str = Field(pattern=r"^(withdraw|deposit)$")
    amount: str
    user_id: int
    time: int

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: str) -> str:
        """Validates amount is of the correct convertible format"""
        try:
            float(value)
            return value
        except ValueError as e:
            raise ValueError("Amount must be in valid format") from e


class Alerts(BaseModel):
    """
    Defines the schema for the returned alerts object.
    """
    alert: bool
    alert_codes: list
    user_id: int
