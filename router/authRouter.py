from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from models.Token import Token
from models.User import User

from controllers.UserController import UserController
from controllers.TokenController import TokenController


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ROLE_PRIORITY = {
    "admin": 1,        # Mais importante
    "validator": 2,    # Intermediário
    "client": 3        # Menos importante
}


auth_router = APIRouter(tags=['Auth'])

@auth_router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

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
    user_role = user.get("role", None)
    main_role = user_role if user_role in ROLE_PRIORITY else None
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "main_role": main_role
    }



@auth_router.get("/admin-area")
async def read_admin_data(user: User = Depends(TokenController.get_current_user_with_role(["admin"]))):
    username= user['username']
    role= user['role']
    return {"msg": f"Olá, {username}! você é um {role}"}

@auth_router.get("/validator-area")
async def read_verificador_data(user: User = Depends(TokenController.get_current_user_with_role(["validator"]))):
    return {"msg": f"Olá, {user['username']}! Você é um validador."}

@auth_router.get("/client-area")
async def read_cliente_data(user: User = Depends(TokenController.get_current_user_with_role(["client"]))):
    return {"msg": f"Olá, {user['username']}! Você é um {user['role']}."}


