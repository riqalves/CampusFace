
from fastapi import APIRouter, HTTPException,FastAPI, Depends, status,File, UploadFile
from typing import Annotated
from bson import ObjectId

from models.User import User, UpdateUserCredentials

from controllers.TokenController import oauth2_scheme

from controllers.TokenController import TokenController
from controllers.UserController import UserController

from serializer.userSerializer import convertUser
user_router = APIRouter(tags=['User'])



@user_router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(TokenController.get_current_active_user)],):
    return current_user

@user_router.post("/user/create")
async def create_user(user:User):
    if not UserController.is_email_valid(user.email):
        raise HTTPException(status_code=500, detail="Email já cadastrado")
    if not UserController.insert_user(user):
        raise HTTPException(status_code=500, detail="Erro ao cadastrar usuário")
    return HTTPException(status_code=201, detail="Usuário cadastrado com sucesso!!")


@user_router.put("/user/update-credentials/")
async def update_user_credentials(user:UpdateUserCredentials,current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
        
        if not UserController.update_user_credentials(ObjectId(current_user["id"]),user):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao atualizar credenciais")
        return HTTPException(status_code=200, detail="Atualizado com sucesso")

@user_router.delete("/user/delete/")
async def delete_user(current_user: Annotated[User, Depends(TokenController.get_current_active_user)], token: str = Depends(oauth2_scheme)):
    
    if UserController.delete_user(current_user["id"]):
        return HTTPException(status_code=200, detail="Deletado com sucesso!!!1")
    raise HTTPException(status_code=500, detail="Erro ao deletar usuário!")