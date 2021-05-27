import uvicorn
import os
import json
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from events_module.Publisher import Publisher
from events_module.NatsWrapper import NatsWrapper
from events_module.Listener import Listener
from events_module.EventType import EventType
from config import settings
from src.api import router
from src.product_utils import create_product, update_product
from src.models.Product import ProductModel
from src.MongoDB import Mongo
app = FastAPI(docs_url=settings.DOCS_URL,
              openapi_url=settings.OPENAPI_URL, redoc_url=None, title=settings.APP_NAME)

app.include_router(router)


@app.on_event("startup")
async def startup_connections():
    if not settings.JWT_SECRET_KEY:
        raise ValueError('JWT_SECRET_KEY not defined')
    # connect to db
    await Mongo().connect(settings.DB_URL, settings.DB_NAME)
    # connecting to nats
    await NatsWrapper().connect()
    # start listen on events
    pr = ProductModel(id='60ad8c55eb0427d772fbd530',
                      price=400, model='dunk OG white')
    new_product = await Mongo.getInstance().db["products"].insert_one(pr.dict())
    await Listener(subject=EventType.product_created,
                   on_receive_func=create_product).listen()
    await Listener(EventType.product_updated, update_product).listen()


@app.on_event("shutdown")
async def shutdown_connections():
    app.mongodb_client.close()
    await NatsWrapper().getInstance().close()


# allow for cors requests
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc.detail)
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for err in exc.errors():
        field = err['loc'][1]
        msg = err['msg'].replace('this value', str(field))
        errors.append(
            {'msg': msg, 'field': field})
    print(errors)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"errors": errors}))

# start the server
if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.HOST,
                port=settings.PORT, reload=settings.DEBUG_MODE)
