from fastapi import Request
from bson import ObjectId
from .models.Product import ProductModel
from .MongoDB import Mongo


async def lock_product(order):
    try:
        new_product = await Mongo.getInstance().db["products"].update_one(
            {"_id": ObjectId(order["product"]["id"])},
            {"$set": {"order_id": order["id"]}}
        )
    except:
        print('err')
    return True


async def unlock_product(product):
    try:
        new_product = await Mongo.getInstance().db["products"].update_one(
            {"_id": ObjectId(order["product"]["_id"])},
            {"$set": {"order_id": null}}
        )
    except:
        print('error')
    return True
