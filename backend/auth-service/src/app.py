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
from models.User import UserSignUp, UserBase, UserDB, UserDBOut
from auth_module.Token import Token, TokenData
from auth_module.auth import authenticate

api = APIRouter(prefix='/api/users')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 180
ALGORITHM = "HS256"


async def get_user(request: Request, username: str):
    if (user := await request.app.mongodb["users"].find_one({"username": username})) is not None:
        return UserDBOut(**user)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def varify_user_credentials(request: Request, username: str, password: str):
    user = await get_user(request, username)
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
    encoded_jwt = jwt.encode(to_encode, os.getenv(
        'JWT_SECRET_KEY'), algorithm=ALGORITHM)
    return encoded_jwt


@api.get("/users", response_description="List all users")
async def list_users(request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find({}).to_list(length=100):
        users.append(User(**doc))
    return users


@api.get("/currentuser", response_description='get details about current logged user')
async def get_current_user(request: Request, current_user: TokenData = Depends(authenticate)):
    if current_user:
        user = await get_user(request, current_user.username)
        if user is None:
            return None
        return UserDBOut(**user.dict())
    return None


@ api.post('/signup', status_code=201, )
async def create_user(response: Response, request: Request, user: UserSignUp):
    existing_user = await request.app.mongodb['users'].find_one(
        {'username': user.username})
    if existing_user is not None:
        raise HTTPException(
            status_code=400, detail={'errors': [{'msg': 'User with that email exists', 'field': 'email'}]})
    user.password = get_password_hash(user.password)
    user_db = UserDB(**user.dict())
    new_user = await request.app.mongodb['users'].insert_one(user_db.dict())
    new_user = await request.app.mongodb['users'].find_one({'username': user_db.username})
    new_user = UserDBOut(**new_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": new_user.username, "id": str(new_user.id)}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=True)
    return new_user


@ api.post('/signin', response_description='login to get jwt token in cookie')
async def login(response: Response, request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await varify_user_credentials(request, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # generate new token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, 'id': str(user.id)}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=True)
    return UserBase(**user.dict())


@ api.post('/signout')
async def sign_out(response: Response):
    response.delete_cookie(key="access_token")
    return
