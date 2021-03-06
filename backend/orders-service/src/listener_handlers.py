from fastapi import Request
from bson import ObjectId
from .models.Product import ProductModel
from .models.Order import OrderModelDB
from .MongoDB import Mongo
from events_module.OrderStatus import OrderStatus
from events_module.Publisher import Publisher
from events_module.EventType import EventType


async def create_product(product):
    try:
        new_product = await Mongo.getInstance().db["products"].insert_one(
            {
                "_id": ObjectId(product["id"]),
                "model": product["model"],
                "price": product["price"],
                "version": product["version"]
            })
    except Exception as e:
        print('ERROR:    Saving product failed')
        print(e)
    else:
        print("INFO:    Product ID: "+product['id']+" saved")
        return True


async def update_product(product):
    try:
        update_result = await Mongo.getInstance().db["products"].update_one(
            {"_id": ObjectId(product["id"]),
             "version": product["version"] - 1},  # check for lover version to update
            {"$set": {"model": product["model"], "price": product["price"]}, "$inc": {
                "version": 1}}
        )
    except Exception as e:
        print('ERROR:    Product updating failed')
        print(e)
    else:
        print("INFO:    Product ID: "+product['id']+" updated")
        return True


async def cancel_order(order):
    order_existing = await Mongo.getInstance().db["orders"].find_one({"_id": ObjectId(order['orderId'])})
    if order_existing['status'] == OrderStatus.complete.value:
        return True
    try:
        update_result = await Mongo.getInstance().db["orders"].update_one(
            # check for lover version to update
            {"_id": ObjectId(order['orderId'])},
            {"$set": {"status": OrderStatus.cancelled.value}, "$inc": {"version": 1}}
        )
    except Exception as e:
        print(e)
    else:
        print('INFO:    Order ID: '+order['orderId']+' is cancelled')
        try:
            order = await Mongo.getInstance().db["orders"].find_one({"_id": ObjectId(order['orderId'])})
            order = OrderModelDB(**order)
            await Publisher(EventType.order_cancelled).publish(order.json())
        except Exception as e:
            print(e)
        else:
            print('INFO:    Order ID: ' +
                  order['orderId']+' canceled event emitted')


async def complete_order(payment):
    print(payment)
    try:
        update_result = await Mongo.getInstance().db["orders"].update_one(
            # check for lover version to update
            {"_id": ObjectId(payment["order_id"])},
            {"$set": {"status": OrderStatus.complete.value}, "$inc": {"version": 1}}
        )
    except err:
        print(err)
    else:
        print('INFO:    Order ID: '+payment['order_id']+' is completed')
        try:
            order = await Mongo.getInstance().db["orders"].find_one({"_id": ObjectId(payment['order_id'])})
            order = OrderModelDB(**order)
            await Publisher(EventType.order_completed).publish(order.json())
        except Exception as e:
            print(e)
        else:
            print('INFO:    Order ID: ' +
                  payment['order_id']+' complete event emitted')
    return True
