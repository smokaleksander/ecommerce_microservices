from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import date


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


class OrderModelDB(BaseModel):
    user_id: str
    status: str
    expiresAt: date
    product: Product

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "status": 'nike',
                'expiresAt': '45',
                'product': '400'
            }
        }


class OrderModelOut(ProductModelIn):
    id: ObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {"id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                        "user_id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                        "status": 'nike',
                        'expiresAt': '45',
                        'product': '400'
                        }
        }
