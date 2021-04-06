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
from OAuth2PasswordBearerWithCookie import OAuth2PasswordBearerWithCookie
from models.Token import Token, TokenData


SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

api = APIRouter(prefix='/api/users')
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="signin")
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


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(request, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(request: Request, current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@ api.get("/users", response_description="List all users")
async def list_users(request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find({}).to_list(length=100):
        users.append(User(**doc))
    return users


@ api.get("/users/me")
async def read_users_me(request: Request, current_user: User = Depends(get_current_active_user)):
    return current_user


@ api.post('/signup', response_description='Create new user', status_code=201)
async def create_user(request: Request, user: User):
    existing_user = await request.app.mongodb['users'].find_one(
        {'email': user.email})
    if existing_user is not None:
        raise HTTPException(
            status_code=400, detail='User with that email exists')
    user.password = get_password_hash(user.password)
    new_user = await request.app.mongodb['users'].insert_one(user.dict())


@ api.post('/signin')
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
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=True)
    return UserResponse(**user.dict())


@ api.post('/signout')
async def sign_out(response: Response):
    response.delete_cookie(key="access_token")
    return
