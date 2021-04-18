import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
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

# override 422 error


@auth_service.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for err in exc.errors():
        errors.append(
            {'msg': err['msg'], 'field': err['loc'][1]})
    print(errors)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"errors": errors}))
    """
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={'detail': {'msg': exc.errors()[0].get('msg'), 'field': exc.errors()[
                            0].get('loc')[1]}}
                        )
    """
# start the server
if __name__ == "__main__":
    uvicorn.run('main:auth_service', host="0.0.0.0", port=8001, reload=True)
