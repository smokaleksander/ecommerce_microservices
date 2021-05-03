from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from .auth_module.Token import Token, TokenData
from .auth_module.auth import authenticate
from .models import ProductModelIn, ProductModelOut, ProductModelDB

router = APIRouter(prefix='/api/products')


@router.post("/", response_description="Add new product", status_code=201)
async def create_product(request: Request, product: ProductModelIn,  current_user: TokenData = Depends(authenticate)):
    pr = ProductModelDB(**product.dict(), user_id=current_user.id)
    print(pr.dict())
    new_product = await request.app.mongodb["products"].insert_one(pr.dict())
    print(new_product.inserted_id)
    created_product = await request.app.mongodb["products"].find_one(
        {"_id": new_product.inserted_id}
    )

    return ProductModelOut(**created_product)


@router.get("/", response_description="List all products", status_code=200)
async def list_products(request: Request):
    products = []
    for doc in await request.app.mongodb["products"].find({}).to_list(length=100):
        products.append(ProductModelOut(**doc))
    return products


@router.get("/{id}", response_description="Get a single product", status_code=200)
async def show_product(id: str, request: Request):
    if (product := await request.app.mongodb["products"].find_one({"_id": ObjectId(id)})) is not None:
        return ProductModelOut(**product)

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.put("/{id}", response_description="Update a product")
async def update_product(id: str, request: Request, product: ProductModelIn,  current_user: TokenData = Depends(authenticate)):
    product = {k: v for k, v in product.dict().items() if v is not None}

    if len(product) >= 1:
        update_result = await request.app.mongodb["products"].update_one(
            {"_id": ObjectId(id), "user_id": current_user.id}, {
                "$set": product}
        )

        if update_result.modified_count == 1:
            if (
                updated_product := await request.app.mongodb["products"].find_one({"_id": ObjectId(id), "user_id": current_user.id})
            ) is not None:
                return ProductModelOut(**updated_product)

    if (
        existing_product := await request.app.mongodb["products"].find_one({"_id": ObjectId(id), "user_id": current_user.id})
    ) is not None:
        return ProductModelOut(**existing_product)

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@ router.delete("/{id}", response_description="Delete product")
async def delete_product(id: str, request: Request,  current_user: TokenData = Depends(authenticate)):
    delete_result = await request.app.mongodb["products"].delete_one({"_id": ObjectId(id), "user_id": current_user.id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Product {id} not found")
