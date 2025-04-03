from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from models.Token import Token, TokenData
from models.User import User

from controllers.UserController import UserController
from controllers.TokenController import TokenController


ACCESS_TOKEN_EXPIRE_MINUTES = 30



auth_router = APIRouter(tags=['Auth'])


@auth_router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    
    if "@" in form_data.username:
        userInDB = UserController.get_user_by_email(form_data.username)
        form_data.username = userInDB["username"]

    
    user = TokenController.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenController.create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")




@auth_router.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user["username"]}]



