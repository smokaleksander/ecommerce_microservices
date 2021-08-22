from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from auth_module.Token import Token, TokenData
from auth_module.auth import authenticate
from .models.Charge import ChargeModel
from .models.Order import OrderModel, OrderModelDB
from events_module.Publisher import Publisher
from events_module.EventType import EventType
from events_module.OrderStatus import OrderStatus
from .MongoDB import Mongo

router = APIRouter(prefix='/api/payments')


@router.post("/", status_code=201)
async def create_charge(request: Request, charge: ChargeModel, current_user: TokenData = Depends(authenticate)):
    print(charge)
    # check if order exists
    if (order := await Mongo.getInstance().db["orders"].find_one({"_id": ObjectId(charge.order_id)})) is None:
        raise HTTPException(status_code=404, detail=f"Order {id} not found")
    # check if order belongs to user
    order = OrderModelDB(**order)
    if order.user_id != current_user.id:
        raise HTTPException(status_code=401, detail=f"Not authorized")
    # check if order is not cancelled already
    if order.status != OrderStatus.cancelled.value:
        raise HTTPException(status_code=404, detail=f"Order cancelled")
    # pr = ProductModelDB(**product.dict(), user_id=current_user.id, version=1)
    # # save to DB
    # new_product = await Mongo.getInstance().db["products"].insert_one(pr.dict())

    # # check if item saved in DB and return it
    # created_product = await Mongo.getInstance().db["products"].find_one(
    #     {"_id": new_product.inserted_id}
    # )
    # # emit event
    # await Publisher(EventType.product_created).publish(
    #     ProductModelDB(**created_product).json(exclude={'size', 'brand', 'user_id'}))

    # return ProductModelDB(**created_product)


# @router.get("/", response_description="List all products", status_code=200)
# async def list_products(request: Request):
#     products = []
#     for doc in await Mongo.getInstance().db["products"].find({}).to_list(length=100):
#         products.append(ProductModelDB(**doc))
#     return products


# @router.get("/{id}", response_description="Get a single product", status_code=200)
# async def show_product(id: str):
#     if (product := await Mongo.getInstance().db["products"].find_one({"_id": ObjectId(id)})) is not None:
#         return ProductModelDB(**product)

#     raise HTTPException(status_code=404, detail=f"Product {id} not found")


# @router.put("/{id}", response_description="Update a product")
# async def update_product(id: str, product: ProductModel,  current_user: TokenData = Depends(authenticate)):

#     update_result = await Mongo.getInstance().db["products"].update_one(
#         {"_id": ObjectId(id), "user_id": current_user.id},
#         {"$set": product.dict(), "$inc": {"version": 1}}
#     )

#     if update_result.modified_count == 1:
#         if (
#             updated_product := await Mongo.getInstance().db["products"].find_one({"_id": ObjectId(id), "user_id": current_user.id})
#         ) is not None:
#             await Publisher(EventType.product_updated).publish(
#                 ProductModelDB(**updated_product).json(exclude={'size', 'brand', 'user_id'}))
#             return ProductModelDB(**updated_product)

#     raise HTTPException(status_code=404, detail=f"Product {id} not found")


# @ router.delete("/{id}", response_description="Delete product")
# async def delete_product(id: str, request: Request,  current_user: TokenData = Depends(authenticate)):
#     delete_result = await Mongo.getInstance().db["products"].delete_one({"id": ObjectId(id), "user_id": current_user.id})

#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Product {id} not found")

# HELPER API CALLS

@ router.get("/orders", status_code=200)
async def list_orders():
    orders = []
    for doc in await Mongo.getInstance().db["orders"].find({}).to_list(length=100):
        orders.append(OrderModelDB(**doc))
    # test
    return orders
