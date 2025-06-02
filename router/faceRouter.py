from fastapi import APIRouter, HTTPException, Depends
from controllers.TokenController import TokenController
from models.User import User
from typing import Annotated
import os
from face_recognition.main import recognize

face_router = APIRouter(tags=['Face'])

IMAGES_DIRECTORY = "imagens"

@face_router.post("/recognize-face")
async def recognize_face(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
    image_filename = current_user["imagePath"]
    image_path = os.path.join(IMAGES_DIRECTORY, image_filename)
    if not image_filename or not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Imagem de perfil não encontrada")
    name = recognize(image_path)
    if name:
        return {"recognized": True, "name": name}
    else:
        raise HTTPException(status_code=404, detail="Face não reconhecida")