import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app import api
from dotenv import load_dotenv
import os

load_dotenv()

# create app instance
auth_service = FastAPI(docs_url='/api/users/docs',
                       openapi_url='/api/users/openapi.json', redoc_url=None, title='auth service')

# inlude router
auth_service.include_router(api)


@auth_service.on_event("startup")
async def startup_app():
    if not os.getenv('JWT_SECRET_KEY'):
        raise ValueError('JWT_SECRET_KEY not defined')
        # connect to db
    auth_service.mongodb_client = AsyncIOMotorClient(os.getenv('DB_URL'))
    auth_service.mongodb = auth_service.mongodb_client[os.getenv('DB_NAME')]


@auth_service.on_event("shutdown")
async def shutdown_app():
    auth_service.mongodb_client.close()


# allow for cors requests
origins = [
    "http://localhost",
    "http://localhost:3000",
]

auth_service.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@auth_service.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc.detail)
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@auth_service.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for err in exc.errors():
        field = err['loc'][1]
        msg = err['msg'].replace('this value', field)
        errors.append(
            {'msg': msg, 'field': field})
    print(errors)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"errors": errors}))


# start the server
if __name__ == "__main__":
    uvicorn.run('main:auth_service', host="0.0.0.0", port=8001, reload=True)
