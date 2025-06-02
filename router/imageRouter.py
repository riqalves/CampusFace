
from fastapi import APIRouter,status, HTTPException,FastAPI, File, UploadFile, Depends

from dbconfig import usersCollection
from controllers.UserController import UserController
from controllers.TokenController import TokenController

import random
from fastapi.responses import FileResponse, JSONResponse
import os


image_router = APIRouter(tags=['Image'])
# ** Rota para upload de imagem de perfil
IMAGES_DIRECTORY = "imagens"
@image_router.put("/update")
async def upload_image(file: UploadFile = File(...), current_user: str = Depends(TokenController.get_current_user)):
    if not os.path.exists(IMAGES_DIRECTORY):
        os.makedirs(IMAGES_DIRECTORY)
    
    filename = f"{random.randint(373, 373773)}{random.randint(373, 373773)}{file.filename}"

    file_path = os.path.join(IMAGES_DIRECTORY, filename)
    with open(file_path, "wb") as image:
        image.write(await file.read())


    insert = usersCollection.find_one_and_update({'email': current_user['email']},{"$set": {'imagePath':filename}})

    if not insert:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao atualizar imagem de perfil")
    return filename

@image_router.delete("/")
async def delete_image_from_user(current_user: str = Depends(TokenController.get_current_user)):
    filename = current_user["imagePath"]

    if filename == "default.png":
        raise HTTPException(status_code=400, detail="Insira uma imagem de perfil antes de excluir")
    
    file_path = os.path.join(IMAGES_DIRECTORY, filename)

    if os.path.exists(file_path):
        updatedImage = UserController.set_image_default(current_user["id"])
        if updatedImage:
            os.remove(file_path)
            return JSONResponse(status_code=200, content={"mensagem": "Imagem excluída com sucesso."})
    else:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
@image_router.get("/user")
async def get_image_path(current_user: str = Depends(TokenController.get_current_user)):
    if "imagePath" not in current_user or not current_user["imagePath"]:
        raise HTTPException(status_code=404, detail="Imagem de perfil não encontrada")    
    return JSONResponse(status_code=200, content={"imagePath": current_user["imagePath"]})  


# ** Comentado por enquanto, pois não é necessário buscar imagens de outros usuários
# @image_router.get("/get-image/{filename}")
# async def get_image_by_filename(filename: str,current_user: str = Depends(TokenController.get_current_user)):
    
#     file_path = os.path.join(IMAGES_DIRECTORY, filename)

#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     else:
#         raise HTTPException(status_code=404, detail="Diretório de imagens não encontrado")

#** Comentado por enquanto, pois não é necessário excluir imagens de outros usuários
# @image_router.delete("/{filename}")
# async def delete_image(filename: str):
#     file_path = os.path.join(IMAGES_DIRECTORY, filename)
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         return {"mensagem": f"Imagem {filename} excluída com sucesso."}
#     else:
#         raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
