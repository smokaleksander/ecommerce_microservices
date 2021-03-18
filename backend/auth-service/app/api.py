from typing import List
from fastapi import Header, APIRouter, HTTPException
from pydantic import BaseModel, Field
from models.UserCredentials import UserCredentials
api = APIRouter(prefix='/api/users')


@api.post('/signup')
async def sign_up(credentials: UserCredentials):
    return


@api.get('/currentuser')
async def get_current_user():
    return 'k8ss'


@api.post('/signin')
async def sign_in():
    return 'signin'


@api.post('/signout')
async def sign_out():
    return 'signin'
