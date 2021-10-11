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
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserBase(BaseModel):

    fullname: str
    username: EmailStr = Field(...)

    @validator('fullname')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError(
                'Fullname must contain a space')

        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                'id': 'asdfasdfadsfasfasdf',
                "username": "jdoe@example.com",
                "password": "123456",
                "fullname": "John Doe",
            }
        }


class UserDB(UserBase):
    disabled: Optional[bool] = False
    password: str = Field(min_length=6)

    class Config:
        #json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "password": "123456",
                "fullname": "John Doe",
                "disabled": False
            }
        }


class UserDBOut(UserBase):
    id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    disabled: Optional[bool] = False
    password: str = Field(min_length=6)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "password": "hashed",
                "fullname": "John Doe",
                "disabled": False
            }
        }


class UserSignUp(UserBase):
    password: str = Field(min_length=6)
    password_repeat: Optional[str]

    @ validator('password_repeat')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError(
                'Passwords do not match')
        return v

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "username": "jdoe@example.com",
                "password": "123456",
                "password_repeat": "123456",
            }
        }


class UserSignIn(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "username": "jdoe@example.com",
                "password": "123456",
                "password_repeat": "123456",
            }
        }
