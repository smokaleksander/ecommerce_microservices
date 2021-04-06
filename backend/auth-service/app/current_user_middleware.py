import os
from fastapi import Depends, Request, HTTPException, status, Depends
from models.Token import Token, TokenData
from OAuth2PasswordBearerWithCookie import OAuth2PasswordBearerWithCookie
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="signin")
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        id: str = payload.get("id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, id=id)
    except JWTError:
        raise credentials_exception
    return token_data
