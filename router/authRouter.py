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
    # ...existing code...
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
    user_roles = user.get("roles", [])
    # Ordena as roles do usuário pela prioridade
    main_role = sorted(user_roles, key=lambda r: ROLE_PRIORITY.get(r, 99))[0] if user_roles else None
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "main_role": main_role
    }




@auth_router.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user["username"]}]

@auth_router.get("/admin-area")
async def read_admin_data(user: User = Depends(TokenController.get_current_user_with_role(["admin"]))):
    username= user['username']
    roles= user['roles']
    return {"msg": f"Olá, {username}! você é um {roles}"}

@auth_router.get("/validator-area")
async def read_verificador_data(user: User = Depends(TokenController.get_current_user_with_role(["validator"]))):
    return {"msg": f"Olá, {user['username']}! Você é um validador."}

@auth_router.get("/client-area")
async def read_cliente_data(user: User = Depends(TokenController.get_current_user_with_role(["client"]))):
    return {"msg": f"Olá, {user['username']}! Você é um {user['role']}."}


