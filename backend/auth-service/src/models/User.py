from pydantic import BaseModel, Field, validator, EmailStr
from fastapi import HTTPException
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


class UserBase(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    username: str = Field(min_length=4)
    email: EmailStr = Field(...)
    password: str = Field(min_length=6)
    fullname: str

    @validator('fullname')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError(
                'Fullname must contain a space')

        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "jdoe@example.com",
                "password": "123456",
                "fullname": "John Doe",
            }
        }


class UserDB(UserBase):
    disabled: Optional[bool] = False

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "jdoe@example.com",
                "password": "123456",
                "fullname": "John Doe",
                "disabled": False
            }
        }


class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    username: str
    email: EmailStr = Field(...)
    full_name: str

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "idasdasd",
                "username": "johndoe2",
                "email": "jdoe@example.com",
                "fullname": "John Doe",
            }
        }


class UserSignUp(UserBase):
    password_repeat: Optional[str]

    @validator('password_repeat')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError(
                'Passwords do not match')
        return v

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe2",
                "fullname": "John Doe",
                "email": "jdoe@example.com",
                "password": "123456",
                "password_repeat": "123456",
            }
        }
