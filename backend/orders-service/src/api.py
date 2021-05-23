from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from auth_module.Token import Token, TokenData
from auth_module.auth import authenticate
from .models.Order import Order, OrderIn, OrderOut
from .models.Product import Product
from events_module.Publisher import Publisher
from events_module.OrderStatus import OrderStatus
from events_module.EventType import EventType
from datetime import datetime, timedelta
from beanie import PydanticObjectId
from typing import List

EXPIRATION_CART_TIME_MINUTES = 30
router = APIRouter(prefix='/api/products')


@router.post("/", response_model=Order, status_code=201)
async def create_order(order: OrderIn,  current_user: TokenData = Depends(authenticate)):
    # look for product user is trying to add to cart
    if (product := await Product.get(order.product_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Product {order.product_id} not found")

    # check if product is not in someone elses cart already
    if (exisiting_order := await Order.find_one(Order.product == product, In(Order.status, [OrderStatus.created, OrderStatus.awaiting_status, OrderStatus.awaiting_payment, OrderStatus.complete]))) is not None:
        raise HTTPException(
            status_code=404, detail=f"Product is reserved")

    expiration = datetime.now() + timedelta(minutes=EXPIRATION_CART_TIME_MINUTES)
    expiration

    new_order = Order(user_id=current_user.id, status=OrderStatus.created,
                      expires_at=expiration, product=product)
    await new_order.insert()

    Publisher(EventType.order_created).publish(new_order.dict())
    return new_order


@router.get("/", response_model=List[Order], status_code=200)
async def list_orders(current_user: TokenData = Depends(authenticate)):
    return await Order.find(Order.user_id == current_user.id).to_list()


@router.get("/{id}", response_model=Order, status_code=200)
async def show_order(id: PydanticObjectId, current_user: TokenData = Depends(authenticate)):
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
