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
    except Exception as e:
        print('Locking product failed')
        print(e)
    else:
        print("INFO:    Product with ID: "+order['product']['id']+" is locked")
        return True


async def unlock_product(product):
    try:
        new_product = await Mongo.getInstance().db["products"].update_one(
            {"_id": ObjectId(order["product"]["id"])},
            {"$set": {"order_id": None}}
        )
    except Exception as e:
        print('Unlocking product failed')
        print(e)
    else:
        print("INFO:    Product with ID: " +
              order['product']['id']+" is unlocked")
        return True
