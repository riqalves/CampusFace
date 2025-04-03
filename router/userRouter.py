
from fastapi import APIRouter, HTTPException,FastAPI, Depends, status,File, UploadFile
from typing import Annotated

from models.User import User, UpdateUserCredentials


from controllers.TokenController import TokenController
from controllers.UserController import UserController

from serializer.userSerializer import convertUser
user_router = APIRouter(tags=['User'])

@user_router.get("/")
def home():
    return {"bomdia": "gente"}


@user_router.post("/user/create")
def create_user(user:User):
    print(user.email)
    if not UserController.is_email_valid(user.email):
        raise HTTPException(status_code=404, detail="Email já cadastrado")
    if not UserController.insert_user(user):
        raise HTTPException(status_code=404, detail="Erro ao cadastrar usuário")
    return HTTPException(status_code=201, detail="Usuário cadastrado com sucesso!!")


@user_router.put("/user/update-credentials/{id}")
def update_user_credentials(id: str,user:UpdateUserCredentials,current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
        userUpdated = usersCollection.find_one_and_update({"_id": ObjectId(id)}, {"$set" : dict(user)})
        
        if not userUpdated:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao atualizar credenciais")
        return HTTPException(status_code=200, detail="Atualizado com sucesso")