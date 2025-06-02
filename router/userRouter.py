
from fastapi import APIRouter, HTTPException,FastAPI, Depends, status,File, UploadFile
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Annotated
from bson import ObjectId

from models.User import User, UpdateUserCredentials
from models.Request import Request

from controllers.TokenController import oauth2_scheme

from controllers.TokenController import TokenController
from controllers.UserController import UserController

user_router = APIRouter(tags=['User'])



@user_router.get("/teste")
async def Home():
    return "Você não deveria estar aqui!!!!!"

@user_router.get("/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(TokenController.get_current_active_user)],):
    return current_user

@user_router.post("/create")
async def create_user(user:User):
    if not UserController.is_email_valid(user.email):
        raise HTTPException(status_code=500, detail="Email já cadastrado")
    if not UserController.insert_user(user):
        raise HTTPException(status_code=500, detail="Erro ao cadastrar usuário")
    return JSONResponse(status_code=201, content="Usuário cadastrado com sucesso!!")


@user_router.put("/update-credentials/")    
async def update_user_credentials(user:UpdateUserCredentials,current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
        
        if not UserController.update_user_credentials(ObjectId(current_user["id"]),user):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao atualizar credenciais")
        return JSONResponse(status_code=200, content="Atualizado com sucesso")

@user_router.delete("/delete/")
async def delete_user(current_user: Annotated[User, Depends(TokenController.get_current_active_user)], token: str = Depends(oauth2_scheme)):
    TokenController.revoke_token(token)
    if UserController.delete_user(current_user["id"]):
        return JSONResponse(status_code=200, content="Deletado com sucesso!!!")
    raise HTTPException(status_code=500, detail="Erro ao deletar usuário!")


@user_router.get("/redirect")
async def teste(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
    if current_user["role"] == "teste":
            return RedirectResponse("/teste")
        
@user_router.post("/send-request")
async def send_request_to_hub(hubID:str,current_user: Annotated[User, Depends(TokenController.get_current_user)]):
    request = Request(
        userID=current_user["id"],
        hubID=hubID,
        created_at=None  # Será preenchido no controller
    )

    UserController.create_hub_request(Request(), current_user["id"], id)
    if "validator" in  current_user["roles"]:
        print("tem validador")
    print("testeeee")
    return current_user