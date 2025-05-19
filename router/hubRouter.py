
from fastapi import APIRouter, HTTPException,FastAPI, Depends, status,File, UploadFile

from models.Hub import Hub 

from fastapi.responses import JSONResponse

from controllers.HubController import HubController

from models.Hub import HubOut

hub_router = APIRouter(tags=['Hub'])




@hub_router.post("/create")
async def create_hub(hub:Hub):
    if not HubController.insert_hub(hub):
        raise HTTPException(status_code=500, detail="Erro ao cadastrar Hub")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Hub cadastrado com sucesso!!")

@hub_router.get("/{id}", response_model=HubOut)
async def get_hub(id: str):
    hub = await HubController.get_hub_by_id(id)
    if hub:
        return hub
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hub não encontrado")

# @hub_router.put("/user/update-credentials/")
# async def update_user_credentials(user:UpdateUserCredentials,current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
        
#         if not UserController.update_user_credentials(ObjectId(current_user["id"]),user):
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao atualizar credenciais")
#         return HTTPException(status_code=200, detail="Atualizado com sucesso")

# @hub_router.delete("/user/delete/")
# async def delete_user(current_user: Annotated[User, Depends(TokenController.get_current_active_user)], token: str = Depends(oauth2_scheme)):
#     TokenController.revoke_token(token)
#     if UserController.delete_user(current_user["id"]):
#         return HTTPException(status_code=200, detail="Deletado com sucesso!!!")
#     raise HTTPException(status_code=500, detail="Erro ao deletar usuário!")


# @hub_router.get("/user/redirect")
# async def teste(current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
#     if current_user["role"] == "teste":
#             return RedirectResponse("/teste")