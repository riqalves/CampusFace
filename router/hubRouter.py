
from fastapi import APIRouter, HTTPException, Depends, status

from models.Hub import Hub 

from fastapi.responses import JSONResponse

from typing import Annotated

from controllers.TokenController import TokenController
from controllers.HubController import HubController

from models.Hub import HubOut
from models.User import User

hub_router = APIRouter(tags=['Hub'])




@hub_router.post("/create")
async def create_hub(hub:Hub, current_user: Annotated[User, Depends(TokenController.get_current_user_with_role(["admin"]))]):
    hub.hubAdmin = current_user["id"]
    if not HubController.insert_hub(hub):
        raise HTTPException(status_code=500, detail="Erro ao cadastrar Hub")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Hub cadastrado com sucesso!!")

@hub_router.get("/{id}", response_model=HubOut)
async def get_hub(id: str):
    hub = await HubController.get_hub_by_id(id)
    if hub:
        return hub
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hub não encontrado")

@hub_router.get("/")
async def get_all_hubs():
    hubs = HubController.get_all_hubs()
    if not hubs:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hubs não encontrados")
    return hubs
   
    
@hub_router.put("/add-user-to-hub/")
async def add_user_to_hub(userID: str, user_role: str, current_user: Annotated[User, Depends(TokenController.get_current_user_with_role("admin"))]):
    if not HubController.add_user_to_hub(current_user["id"], userID, user_role):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao adicionar usuário ao hub")
    return JSONResponse(status_code=200, content="Usuário adicionado com sucesso ao hub")

@hub_router.get("/get-validators-from-hub/{id}")
async def get_validators_from_hub(id: str):
    validators = HubController.get_validators_from_hub(id)
    if not validators:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum validador encontrado para este hub")
    return validators



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