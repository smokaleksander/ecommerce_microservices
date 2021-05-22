from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import List
from .auth_module.Token import Token, TokenData
from .auth_module.auth import authenticate
from .models import ProductModelIn, ProductModelOut, ProductModelDB
from .events_module import Publisher
router = APIRouter(prefix='/api/orders')


@router.post("/", status_code=201)
async def create_order(request: Request, product_id: str,  current_user: TokenData = Depends(authenticate)):
    pr = ProductModelDB(**product.dict(), user_id=current_user.id)
    # save to DB
    new_product = await request.app.mongodb["products"].insert_one(pr.dict())

    # check if item saved in DB and return it
    created_product = await request.app.mongodb["products"].find_one(
        {"_id": new_product.inserted_id}
    )
    # emit event
    Publisher('product:created').publish(created_product.dict())
    return ProductModelOut(**created_product)


@router.get("/", status_code=200)
async def list_orders(request: Request):
    products = []
    for doc in await request.app.mongodb["products"].find({}).to_list(length=100):
        products.append(ProductModelOut(**doc))
    return products


@router.get("/{id}", response_description="Get a single product", status_code=200)
async def show_order(id: str, request: Request):
    if (product := await request.app.mongodb["products"].find_one({"_id": ObjectId(id)})) is not None:
        return ProductModelOut(**product)

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@ router.delete("/{id}")
async def delete_orders(id: str, request: Request,  current_user: TokenData = Depends(authenticate)):
    delete_result = await request.app.mongodb["products"].delete_one({"_id": ObjectId(id), "user_id": current_user.id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Product {id} not found")
