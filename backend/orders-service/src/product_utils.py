from fastapi import Request
from .models.Product import ProductModel
from .MongoDB import Mongo


async def create_product(request: Request, product):
    print('func')
    print(product)
    print(type(product))
    try:
        new_product = await Mongo.getInstance().db["products"].insert_one(product)
    except:
        print('error')
    created_product = await Mongo.getInstance().db["products"].find_one(
        {"_id": new_product.inserted_id}
    )
    print('inserted')
    print(created_product)
    return True
    # await product.create()
    # return product


async def update_product(request: Request, update_product: ProductModel):
    await Mongo.getInstance().db["products"].update_one(
        {"_id": ObjectId(product.id)}, {
            "$set": product.dict()}
    )
    print('event received; product updated')

    # product = Product.get(update_product.id)
    # await product.replace(update_product)
