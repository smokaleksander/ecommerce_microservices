from pydantic import BaseModel, Field, ValidationError, validator, EmailStr
from email_validator import validate_email


class UserCredentials(BaseModel):
    email: EmailStr = Field()
    password: str = Field(min_length=4)
