from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from env_variables import ACESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY
from serializer.user_serializer import convertUser, convertUsers
from serializer.post_serializer import convertPost, convertPosts
from db_config import usersCollection,codesCollection, postsCollection
from models.Token import TokenData
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


class UserController:
    
    