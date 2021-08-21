from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from auth_module.Token import Token, TokenData
from auth_module.auth import authenticate
from .models.Order import OrderModel, OrderModelDB
from .models.Product import ProductModel
from events_module.Publisher import Publisher
from events_module.OrderStatus import OrderStatus
from events_module.EventType import EventType
from datetime import datetime, timedelta
from typing import List
from .MongoDB import Mongo
from .listener_handlers import update_product
import json

EXPIRATION_CART_TIME_MINUTES = 15

router = APIRouter(prefix='/api/orders')


@router.post("/{product_id}", response_model=OrderModelDB, status_code=201)
async def create_order(product_id: str,  current_user: TokenData = Depends(authenticate)):
    # look for product user is trying to add to cart
    product = await Mongo.getInstance().db["products"].find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(
            status_code=404, detail=f"Product {order.product.id} not found")
    product = ProductModel(**product)
    # check if product is not in someone elses cart already
    existing_order = await Mongo.getInstance().db["orders"].find_one(
        {"product": product.dict()},
        {"status": {"$in": [["created", "awaiting_payment"],  # why two arrays - i have no idea pymongo throws error if not
                            ["complete"]]}}
    )

    if existing_order is not None:
        raise HTTPException(
            status_code=404, detail=f"Order this product is impossible right now")

    expiration = datetime.now() + timedelta(seconds=EXPIRATION_CART_TIME_MINUTES)
    new_order = OrderModelDB(user_id=current_user.id, status=OrderStatus.created,
                             expires_at=expiration, product=product, version=1)
    inserted_order = await Mongo.getInstance().db["orders"].insert_one(new_order.dict())
    # check if new order in db and return in
    inserted_order = await Mongo.getInstance().db["orders"].find_one(
        {"_id": inserted_order.inserted_id}
    )
    inserted_order = OrderModelDB(**inserted_order)
    try:
        await Publisher(EventType.order_created).publish(inserted_order.json(exclude={'size', 'brand', 'user_id'}))
    except Exception as e:
        print(e)
    return inserted_order


@ router.get("/", status_code=200)
async def list_orders(request: Request, current_user: TokenData = Depends(authenticate)):
    orders = []
    for doc in await Mongo.getInstance().db["orders"].find({"user_id": current_user.id}).to_list(length=100):
        orders.append(OrderModelDB(**doc))
    return orders


@ router.get("/products", response_description="List all products", status_code=200)
async def list_products(request: Request):
    products = []
    for doc in await Mongo.getInstance().db["products"].find({}).to_list(length=100):
        products.append(str(doc))
    return products


@ router.get("/products/{id}", response_description="Get a single product", status_code=200)
async def show_product(id: str, request: Request):
    product = await Mongo.getInstance().db["products"].find_one({"_id": ObjectId(id)})
    if product is not None:
        return str(product)

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@ router.get("/{id}", response_model=OrderModelDB, status_code=200)
async def show_order(id: str, current_user: TokenData = Depends(authenticate)):
    order = await Mongo.getInstance().db["orders"].find_one({"_id": ObjectId(id), "user_id": current_user.id})
    if order is not None:
        return OrderModelDB(**order)
    raise HTTPException(status_code=404, detail=f"Order {id} not found")


@ router.delete("/{id}", response_description="Order deleted", status_code=204)
async def delete_order(id: str, current_user: TokenData = Depends(authenticate)):
    delete_result = await Mongo.getInstance().db["order"].delete_one({"id": ObjectId(id), "user_id": current_user.id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Order {id} not found")
