from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from serializer.userSerializer import convertUser

from models.Token import Token, TokenData
from models.User import User

from dbconfig import usersCollection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserController:
    
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(password)->str:
        return pwd_context.hash(password)

    def get_user(username: str)->dict:
        user_data = usersCollection.find_one({"username": username})
        if user_data:
            return convertUser(user_data)
            
    
    def is_email_valid(email: str)-> bool:
        user = usersCollection.find_one({'email': email})
        # Se o usuário de mesmo email não for encontrado, logo é possível cadastrar
        if not user:
            return True
        return False

    def insert_user(user: User) -> bool:
        user.created_at = datetime.now()
        user.password =  UserController.get_password_hash(user.password)
        insert = usersCollection.insert_one(dict(user))
        if not insert:
            return False
        return True


    


    


    

    