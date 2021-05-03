from config import settings
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
import uvicorn
from fastapi import FastAPI, status
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
from app.api import router

app = FastAPI(docs_url=settings.DOCS_URL,
              openapi_url=settings.OPENAPI_URL, redoc_url=None, title=settings.APP_NAME)

app.include_router(router)


@app.on_event("startup")
async def startup_db_client():
    if not settings.JWT_SECRET_KEY:
        raise ValueError('JWT_SECRET_KEY not defined')
        # connect to db
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


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
        msg = err['msg'].replace('this value', field)
        errors.append(
            {'msg': msg, 'field': field})
    print(errors)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"errors": errors}))

# start the server
if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.HOST,
                port=settings.PORT, reload=settings.DEBUG_MODE)