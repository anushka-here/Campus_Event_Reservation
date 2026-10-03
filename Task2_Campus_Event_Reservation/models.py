from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr, field_validator

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    venue: str
    capacity: int
    organizer: str
    status: str = "Open"

    @field_validator("title", "venue", "organizer")
    @classmethod
    def non_empty(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("This field must not be empty.")
        return value

    @field_validator("capacity")
    @classmethod
    def positive_capacity(cls, value: int):
        if value <= 0:
            raise ValueError("Capacity must be greater than 0.")
        return value

    @field_validator("status")
    @classmethod
    def valid_status(cls, value: str):
        value = value.strip().title()
        if value not in {"Open", "Closed"}:
            raise ValueError("Status must be Open or Closed.")
        return value

class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(index=True)
    student_name: str
    roll_number: str
    email: str

    @field_validator("student_name", "roll_number")
    @classmethod
    def non_empty(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("This field must not be empty.")
        return value

    @field_validator("email")
    @classmethod
    def valid_email(cls, value: str):
        value = value.strip()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Enter a valid email address.")
        return value
