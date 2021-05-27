from fastapi import Request
from bson import ObjectId
from .models.Product import ProductModel
from .MongoDB import Mongo


async def create_product(product):
    try:
        new_product = await Mongo.getInstance().db["products"].insert_one(
            {
                "_id": ObjectId(product["id"]),
                "model": product["model"],
                "price": product["price"],
                "version": product["version"]
            })
    except:
        print('error')
    return True
    # await product.create()
    # return product


async def update_product(product):
    print(product)
    print(type(product))
    try:
        update_result = await Mongo.getInstance().db["products"].update_one(
            {"_id": ObjectId(product["id"]),
             "version": product["version"] - 1},
            {"$set": {"model": product["model"], "price": product["price"]}, "$inc": {
                "version": 1}}
        )
    except:
        print('error')
    return True

    # product = Product.get(update_product.id)
    # await product.replace(update_product)
