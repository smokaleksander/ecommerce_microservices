from pydantic import BaseModel, Field, ValidationError, validator, EmailStr
from typing import Optional
from bson import ObjectId
from email_validator import validate_email


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    username: str
    email: EmailStr = Field(...)
    password: str
    full_name: str
    disabled: Optional[bool] = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "jdoe@example.com",
                "password": "123456",
                "full_name": "John Doe",
                "disabled": False
            }
        }


class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    username: str
    email: EmailStr = Field(...)
    full_name: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "idasdasd",
                "username": "johndoe2",
                "email": "jdoe@example.com",
                "full_name": "John Doe",
            }
        }


class UpdateUserModel(BaseModel):
    username: str
    email: EmailStr = Field(...)
    password: str = Field(...)
    full_name: str
    disabled: bool

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "johndoe2",
                "email": "jdoe@example.com",
                "password": "123456",
                "full_name": "John Doe",
                "disabled": False

            }
        }
