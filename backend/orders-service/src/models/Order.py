from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from events_module.OrderStatus import OrderStatus
from datetime import datetime
from .Product import ProductModel


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
    product: ProductModel

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            # datetime: lambda v: v.isoformat(),
            # status: lambda v: v.value
        }
        schema_extra = {
            "example": {
                "model": "jordan 4 blue navy",

            }
        }


class OrderModelDB(OrderModel):
    user_id: str
    version: int
    status: OrderStatus
    expires_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model": "jordan 4 blue navy",
            }
        }


# class Order(Document):
#     status: OrderStatus
#     expires_at: datetime
#     user_id: PydanticObjectId
#     product: Product

#     class DocumentMeta:
#         collection_name = 'orders'

#     class Config:
#         json_encoders = {ObjectId: str}
#         arbitrary_types_allowed = True
#         allow_population_by_field_name = True
#         schema_extra = {
#             "example": {
#                 "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
#                 "status": "reserved",
#                 "expires_at": 'date',
#                 "product": {
#                     'id': "00010203-0405-0607-0809-0a0b0c0d0e0f",
#                     'model': 'model',
#                     'brand': 'brand',
#                     'price': 400
#                 }
#             }
#         }

# Order.update_forward_refs()
