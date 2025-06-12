from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from fastapi.responses import JSONResponse
from controllers.TokenController import TokenController
from controllers.UserController import UserController
from models.User import User
from typing import Annotated
import os
import shutil
from face.main import recognize, train

face_router = APIRouter(tags=['Face'])

IMAGES_DIRECTORY = "imagens"
TRAIN_DIRECTORY = "face/train"

# @face_router.post("/recognize-face")
# async def recognize_face(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
#     image_filename = current_user["imagePath"]
#     image_path = os.path.join(IMAGES_DIRECTORY, image_filename)

#     if not image_filename or not os.path.isfile(image_path):
#         raise HTTPException(status_code=404, detail="Imagem de perfil não encontrada")

#     # Se a imagem não for a padrão, adiciona ao diretório de treino do usuário
#     if image_filename != "default.jpg":
#         user_train_dir = os.path.join(TRAIN_DIRECTORY, current_user["email"])
#         os.makedirs(user_train_dir, exist_ok=True)
#         dest_image_path = os.path.join(user_train_dir, image_filename)
#         # Copia a imagem apenas se ainda não existir no diretório de treino
#         if not os.path.isfile(dest_image_path):
#             shutil.copy2(image_path, dest_image_path)
#         # Treina o modelo com a nova imagem
#         train(TRAIN_DIRECTORY)

#     name = recognize(image_path)
#     if name:
#         return {"recognized": True, "name": name}
#     else:
#         raise HTTPException(status_code=404, detail="Face não reconhecida")




@face_router.post("/recognize")
async def recognize_face(image: UploadFile = File(...)):
    print("Iniciando reconhecimento facial")

    
    image_filename = image.filename

    image_path = os.path.join(IMAGES_DIRECTORY, image_filename)
    with open(image_path, "wb") as file:
        file.write(await image.read())
 
    recognized = recognize(image_path)
    user = UserController.get_user_by_id(recognized)
    
    
    if recognized:
        return {"recognized": True, "user": user}
    else:
        return {"recognized": False, "user": None}
    

@face_router.post("/train")
async def train_faces(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
    """
    Treina o modelo de reconhecimento facial com as imagens do diretório 'train'.
    Apenas usuários administradores podem treinar.
    """
    if not current_user or "admin" not in (current_user.get("role") or []):
        raise HTTPException(status_code=403, detail="Apenas administradores podem treinar o modelo.")
    if not os.path.isdir(TRAIN_DIRECTORY):
        raise HTTPException(status_code=404, detail="Diretório de treinamento não encontrado.")
    train(TRAIN_DIRECTORY)
    return {"message": "Treinamento concluído com sucesso."}