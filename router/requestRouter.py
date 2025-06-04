
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import Annotated
from bson import ObjectId

from models.User import User
from models.Request import Request


from controllers.TokenController import TokenController
from controllers.HubController import HubController
from controllers.RequestController import RequestController
from controllers.UserController import UserController

request_router = APIRouter(tags=['Request'])

#** USER
@request_router.post("/user/send-request")
async def send_request_to_hub(hubID:str,current_user: Annotated[User, Depends(TokenController.get_current_user_with_role("admin"))]):
    request = Request(
        userID=current_user["id"],
        hubID=hubID,
    )

    insertedRequest = UserController.create_hub_request(request)
    if not insertedRequest:
        raise HTTPException(status_code=500, detail="Erro ao enviar solicitação para o hub")

    return insertedRequest



# ** HUB
# @request_router.post("/hub/accept-request")
@request_router.get("/hub/get_all_requests/{id}")
async def get_all_requests_from_hub(id: str):
    requests = RequestController.get_all_requests_from_hub(id)
    if not requests:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Nenhum pedido encontrado para este hub")
    return requests


@request_router.put("/hub/set-request-status")
async def set_request_status(id: str ,status:str, current_user: Annotated[User, Depends(TokenController.get_current_user_with_role("admin"))]):
    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do pedido não fornecido")

    updatedRequest = RequestController.set_request_status(id, status)

    if not updatedRequest:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao aceitar o pedido")

    return JSONResponse(status_code=200, content={"message": "Pedido aceito com sucesso"})
