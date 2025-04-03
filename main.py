from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from models.Token import Token, TokenData
from models.User import User

from router.userRouter import user_router
from router.authRouter import auth_router
# to get a string like this run:
# openssl rand -hex 32







app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)









