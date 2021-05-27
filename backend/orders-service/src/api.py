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
from beanie import PydanticObjectId
from typing import List
from .MongoDB import Mongo
EXPIRATION_CART_TIME_MINUTES = 30

router = APIRouter(prefix='/api/orders')


@router.post("/", response_model=OrderModelDB, status_code=201)
async def create_order(order: OrderModel,  current_user: TokenData = Depends(authenticate)):
    # look for product user is trying to add to cart
    if (product := await Mongo.getInstance().db["products"].find_one({"_id": ObjectId(order.id)})) is None:
        raise HTTPException(
            status_code=404, detail=f"Product {order.product_id} not found")

    # check if product is not in someone elses cart already
    if (exisiting_order := await Mongo.getInstance().db["orders"].find_one({Order.product == product, In(Order.status, [OrderStatus.created, OrderStatus.awaiting_status, OrderStatus.awaiting_payment, OrderStatus.complete])})) is not None:
        raise HTTPException(
            status_code=404, detail=f"Product is reserved")

    expiration = datetime.now() + timedelta(minutes=EXPIRATION_CART_TIME_MINUTES)
    expiration

    new_order = Order(user_id=current_user.id, status=OrderStatus.created,
                      expires_at=expiration, product=product)
    await new_order.insert()

    Publisher(EventType.order_created).publish(new_order.dict())
    return new_order


@router.get("/", response_model=List[OrderModelDB], status_code=200)
async def list_orders(request: Request, current_user: TokenData = Depends(authenticate)):
    orders = []
    for doc in await Mongo.getInstance().db["orders"].find({}).to_list(length=100):
        orders.append(OrderModelDB(**doc))
    return orders


@router.get("/products", response_description="List all products", status_code=200)
async def list_products(request: Request):
    products = []
    for doc in await Mongo.getInstance().db["products"].find({}).to_list(length=100):
        products.append(ProductModel(**doc))
    return products


@router.get("/{id}", response_model=OrderModelDB, status_code=200)
async def show_order(id: str, current_user: TokenData = Depends(authenticate)):
    if (order := await Order.find(Order.user_id == current_user.id, _id=PydanticObjectId(id))) is not None:
        return order
    raise HTTPException(status_code=404, detail=f"Order {id} not found")


@ router.delete("/{id}", response_description="Delete product", status_code=204)
async def delete_order(id: PydanticObjectId, current_user: TokenData = Depends(authenticate)):
    if (order := await Order.find(Order.user_id == current_user.id, _id=PydanticObjectId(id))) is not None:
        await order.delete()
        Publisher(EventType.order_cancelled).publish(order.dict())
        return
    raise HTTPException(status_code=404, detail=f"Order {id} not found")
