import uvicorn
import os
import json
from fastapi import FastAPI, status
from config import settings
from fastapi.exceptions import RequestValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.api import router
from events_module.Publisher import Publisher
from events_module.NatsWrapper import NatsWrapper
from events_module.Listener import Listener
from events_module.EventType import EventType
from app.MongoDB import Mongo
from app.listeners_handlers import save_order, cancel_order

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
    await Listener(EventType.order_created, save_order).listen()
    await Listener(EventType.order_cancelled, cancel_order).listen()


@ app.on_event("shutdown")
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


@ app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc.detail)
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@ app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for err in exc.errors():
        field = err['loc'][1]
        msg = err['msg'].replace('this value', str(field))
        errors.append(
            {'msg': msg, 'field': field})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"errors": errors}))

# start the server
if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.HOST,
                port=settings.PORT, reload=settings.DEBUG_MODE)
