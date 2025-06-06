
from datetime import datetime
import os
import random
from fastapi import APIRouter, Form, HTTPException, Depends, status, File, UploadFile
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Annotated, List, Optional
from bson import ObjectId
from pydantic import EmailStr

from models.User import User, UpdateUserCredentials

from controllers.TokenController import oauth2_scheme

from controllers.TokenController import TokenController
from controllers.UserController import UserController

from face.main import save_image_to_train_dir, train

user_router = APIRouter(tags=['User'])




@user_router.get("/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(TokenController.get_current_active_user)],):
    return current_user

    
IMAGES_DIRECTORY = "imagens"
@user_router.post("/create")
async def create_user(
    name: str = Form(...),
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    birthDate: Optional[datetime] = Form(None),
    cpf: str = Form(...),
    role: str = Form(...),
    disabled: Optional[bool] = Form(False),
    image: Optional[UploadFile] = File(None)
):
    print("=========================================================")
    print(image)
    print("=========================================================")
    # Salva a imagem no diretório de imagens

    if role in ["admin", "validator"]:
        image_filename = "default.jpg"
    if image != None:
        image_filename = f"{random.randint(373, 373773)}{random.randint(373, 373773)}{image.filename}"

        file_path = os.path.join(IMAGES_DIRECTORY, image_filename)
        with open(file_path, "wb") as file:
            file.write(await image.read())
        save_image_to_train_dir(email, image_filename)
        train("face/train")
         
    # Cria o objeto User
    user = User(
        name=name,
        username=username,
        email=email,
        password=password,
        birthDate=birthDate,
        cpf=cpf,
        role=role,
        disabled=disabled,
        imagePath=image_filename,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    # print("=========================================================")
    print(user)

    if not UserController.is_email_valid(user.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email já cadastrado")
    if not UserController.insert_user(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao cadastrar usuário")
    
    
    return JSONResponse(status_code=201, content="Usuário cadastrado com sucesso!!")
   





# @user_router.post("/create")
# async def old_create_user(user:User,file: UploadFile = File(...)):
#     if not UserController.is_email_valid(user.email):
#         raise HTTPException(status_code=500, detail="Email já cadastrado")
#     if not UserController.insert_user(user):
#         raise HTTPException(status_code=500, detail="Erro ao cadastrar usuário")
#     save_image_to_train_dir(user.email, user.imagePath )
#     train("face/train")
#     return JSONResponse(status_code=201, content="Usuário cadastrado com sucesso!!")


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
        
