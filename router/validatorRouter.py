from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from models.Token import Token
from models.User import User

from controllers.UserController import UserController
from controllers.TokenController import TokenController



# TO-DO Função (get) para ler e comparar a string enviada

@validator_router.get("/users/me/items/")
async def read_card(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user["username"]}]



# TO-DO Função de gerar código. enviar uma string com código pra gerar o qr-code controlado pelo expirationDate