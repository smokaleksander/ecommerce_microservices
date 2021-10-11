from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from auth_module.Token import Token, TokenData
from auth_module.auth import authenticate
from .models.Charge import ChargeModel
from .models.Order import OrderModel, OrderModelDB
from .models.Payment import PaymentModel
from events_module.Publisher import Publisher
from events_module.EventType import EventType
from events_module.OrderStatus import OrderStatus
from .MongoDB import Mongo
from config import settings
import stripe
import json
router = APIRouter(prefix='/api/payments')

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/", status_code=201)
async def proceed_payment(request: Request, charge: ChargeModel, current_user: TokenData = Depends(authenticate)):
    # check if order exists
    if (order := await Mongo.getInstance().db["orders"].find_one({"_id": ObjectId(charge.order_id)})) is None:
        raise HTTPException(status_code=404, detail=f"Order {id} not found")
    # check if order belongs to user
    order = OrderModelDB(**order)
    if order.user_id != current_user.id:
        raise HTTPException(status_code=401, detail=f"Not authorized")
    # check if order is not cancelled already
    if (order.status == OrderStatus.cancelled or order.status == OrderStatus.complete):
        raise HTTPException(
            status_code=404, detail=f"Order cancelled or completed")
    # create charge
    stripe_charge = stripe.Charge.create(
        amount=int(order.price * 100),
        currency="usd",
        source=charge.stripe_token,
        description="Ecom",
    )
    # create payment object
    payment = PaymentModel(order_id=str(order.id), stripe_id=stripe_charge.id)
    new_payment = await Mongo.getInstance().db["payments"].insert_one(payment.dict())
    # check if payment is created successfully
    new_payment = await Mongo.getInstance().db["payments"].find_one({"_id": ObjectId(new_payment.inserted_id)})
    # emit event
    await Publisher(EventType.payment_created).publish(PaymentModel(**new_payment).json())

    return PaymentModel(**new_payment)


# @ router.get("/orders", status_code=200)
# async def list_orders():
#     orders = []
#     for doc in await Mongo.getInstance().db["orders"].find({}).to_list(length=100):
#         orders.append(OrderModelDB(**doc))
#     return orders


# @ router.get("/", status_code=200)
# async def list_payments():
#     payments = []
#     for doc in await Mongo.getInstance().db["payments"].find({}).to_list(length=100):
#         payments.append(PaymentModel(**doc))
#     return payments
