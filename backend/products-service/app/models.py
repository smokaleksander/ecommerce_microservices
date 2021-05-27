from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


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


class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model: str
    brand: str
    size: float
    price: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "model": "jordan 4 blue navy",
                "brand": 'nike',
                'size': '45',
                'price': '400'
            }
        }


class ProductModelDB(ProductModel):
    user_id: str
    version: int

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {"userId": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                        "model": "jordan 4 blue navy",
                        "brand": 'nike',
                        'size': '45',
                        'price': '400',
                        'version': '1'
                        }
        }
