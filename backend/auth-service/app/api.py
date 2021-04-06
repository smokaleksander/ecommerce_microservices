import os
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import Header, APIRouter, HTTPException, Request, Body, status, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.User import User, UserResponse
#from OAuth2PasswordBearerWithCookie import OAuth2PasswordBearerWithCookie
from models.Token import Token, TokenData
from current_user_middleware import get_current_user

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

api = APIRouter(prefix='/api/users')
#oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="signin")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(request: Request, username: str):
    if (user := await request.app.mongodb["users"].find_one({"username": username})) is not None:
        return User(**user)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(request: Request, username: str, password: str):
    user = await get_user(request, username)
    print(user)
    if not user:
        return False
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@ api.get("/users", response_description="List all users")
async def list_users(request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find({}).to_list(length=100):
        users.append(User(**doc))
    return users


@ api.get("/users/me", response_description='get details about current logged user')
async def read_users_me(request: Request, current_user: TokenData = Depends(get_current_user)):
    return await get_user(request, current_user.username)


@ api.post('/signup', response_description='Create new user', status_code=201)
async def create_user(request: Request, user: User):
    existing_user = await request.app.mongodb['users'].find_one(
        {'email': user.email})
    if existing_user is not None:
        raise HTTPException(
            status_code=400, detail='User with that email exists')
    existing_user = await request.app.mongodb['users'].find_one(
        {'username': user.username})
    if existing_user is not None:
        raise HTTPException(
            status_code=400, detail='User with that username exists')
    user.password = get_password_hash(user.password)
    new_user = await request.app.mongodb['users'].insert_one(user.dict())


@ api.post('/signin', response_description='login to get jwt token in cookie')
async def login(response: Response, request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(request, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "id": str(user.id)}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=True)
    return UserResponse(**user.dict())


@ api.post('/signout')
async def sign_out(response: Response):
    response.delete_cookie(key="access_token")
    return
