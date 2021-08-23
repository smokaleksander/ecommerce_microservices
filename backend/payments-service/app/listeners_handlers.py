from fastapi import Request
from bson import ObjectId
from .models.Order import OrderModel, OrderModelDB
from events_module.OrderStatus import OrderStatus
from .MongoDB import Mongo


async def save_order(order):
    try:
        # save to DB
        new_order = await Mongo.getInstance().db["orders"].insert_one(
            {
                "_id": ObjectId(order['id']),
                "price": order['product']['price'],
                "status": order['status'],
                "user_id": order['user_id'],
                "version": order['version']
            })
    except Exception as e:
        print('ERROR:    Saving order failed')
        print(e)
    else:
        print("INFO:    Order ID: "+order['id']+" saved")
        return True


async def cancel_order(order):
    print(order)
    try:
        new_product = await Mongo.getInstance().db["orders"].update_one(
            {"_id": ObjectId(order["id"]), "version": order["version"] - 1},
            {"$set": {"status": OrderStatus.cancelled.value}, "$inc": {"version": 1}}
        )
    except Exception as e:
        print('ERROR:    Cancelling order failed')
        print(e)
    else:
        print("INFO:    Order with ID: " +
              order['id']+" is cancelled")
        return True


async def complete_order(order):
    try:
        new_product = await Mongo.getInstance().db["orders"].update_one(
            {"_id": ObjectId(order["id"]), "version": order["version"] - 1},
            {"$set": {"status": OrderStatus.complete.value}, "$inc": {"version": 1}}
        )
    except Exception as e:
        print('ERROR:    Completing order failed')
        print(e)
    else:
        print("INFO:    Order with ID: " +
              order['id']+" is completed")
        return True
