from datetime import datetime, timedelta, timezone
from typing import Annotated, List

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from models.Token import TokenData
from models.User import User
from controllers.UserController import UserController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"



# Lista de tokens revogados (idealmente, use Redis ou banco de dados)
revoked_tokens = set()

class TokenController:

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.now(timezone.utc) + expires_delta
            else:
                expire = datetime.now(timezone.utc) + timedelta(minutes=15)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt

    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        if token in revoked_tokens:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as informações",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        
        except InvalidTokenError:
            raise credentials_exception
        user = UserController.get_user( username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


    def get_current_user_with_role(allowed_roles: List[str]):
        async def wrapper(user: User = Depends(TokenController.get_current_user)):
            # Considerando que user["role"] é uma string
            if user["role"] not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Você não tem permissão para acessar este recurso"
                )
            return user
        return wrapper

    async def   get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
            if current_user["disabled"]:
                raise HTTPException(status_code=400, detail="Usuário inativo!")
            return current_user

    def authenticate_user(username: str, password: str):
        if "@" in username:
            user = UserController.get_user_by_email(username)
        else:
            user = UserController.get_user(username)
        
        # Se não encontrar, tenta buscar pelo email
        if not user:
            return False
        if not UserController.verify_password(password, user["password"]):
            return False
        return user

    @staticmethod
    def revoke_token(token: str):
        """ Adiciona o token à blacklist para impedir seu uso futuro """
        revoked_tokens.add(token)
        return {"message": "Token revogado com sucesso"}
