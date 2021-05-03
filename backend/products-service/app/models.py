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
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ProductModelIn(BaseModel):
    #id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    model: str
    brand: str
    size: float
    price: float

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "model": "jordan 4 blue navy",
                "brand": 'nike',
                'size': '45',
                'price': '400'
            }
        }


class ProductModelDB(ProductModelIn):
    user_id: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {"userId": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                        "model": "jordan 4 blue navy",
                        "brand": 'nike',
                        'size': '45',
                        'price': '400'
                        }
        }


class ProductModelOut(ProductModelIn):
    id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {"id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                        "model": "jordan 4 blue navy",
                        "brand": 'nike',
                        'size': '45',
                        'price': '400',
                        'user_id': 'asdfasdfadsgfsagasgafsgfsa'
                        }
        }
