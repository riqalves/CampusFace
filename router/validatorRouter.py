from datetime import timedelta
from typing import Annotated

from datetime import datetime

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from models.Token import Token
from models.User import User

from controllers.TokenController import TokenController
from controllers.CodeController import CodeController

validator_router = APIRouter(tags=['Validator'])

# TO-DO Função (get) para ler e comparar a string enviada

# @validator_router.get("/users/me/items/")
# async def read_card(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
#     return [{"item_id": "Foo", "owner": current_user["username"]}]



# TO-DO Função de gerar código. enviar uma string com código pra gerar o qr-code controlado pelo expirationDate
# ** VALIDATOR
@validator_router.post("/generate-code")
async def generate_code_for_user(userID: str):
    """
    Gera um código de validação para o usuário.
    O código é válido por um período especificado em minutos (default: 60 minutos).
    """

    code = CodeController.generate_validation_code(userID)
    
    if not code:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Erro ao gerar código")

    delta = code.expirationDate - datetime.utcnow()
    minutes = int(delta.total_seconds() // 60)
    seconds = int(delta.total_seconds() % 60)
    return {
        "code": code.code,
        "expires_in": f"{minutes} minuto(s) e {seconds} segundo(s)"
    }

@validator_router.post("/validate-code")
async def validate_code_from_user(code: str):
    """
    Valida o código enviado pelo usuário.
    """
    validatedCode = CodeController.validate_code(code)  # Exemplo de código, deve ser substituído pela lógica de recebimento do código
    if not validatedCode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Código inválido ou expirado")

    return validatedCode