from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from events_module.OrderStatus import OrderStatus


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


class OrderModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: OrderStatus
    price: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class OrderModelDB(OrderModel):
    version: str
    user_id: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
