import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api
from dotenv import load_dotenv
import os
load_dotenv()

# create app instance
app = FastAPI(docs_url='/api/users/docs',
              openapi_url='/api/users/openapi.json', redoc_url=None, title='auth service')


@app.on_event("startup")
async def startup_app():
    if not os.getenv('JWT_SECRET_KEY'):
        raise ValueError('JWT_SECRET_KEY not defined')
        # connect to db
    app.mongodb_client = AsyncIOMotorClient(os.getenv('DB_URL'))
    app.mongodb = app.mongodb_client[os.getenv('DB_NAME')]


@app.on_event("shutdown")
async def shutdown_app():
    app.mongodb_client.close()


# inlude router
app.include_router(api)
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

# start the server
if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8001, reload=True)
