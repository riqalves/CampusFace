
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import Annotated
from bson import ObjectId

from dbconfig import requestsCollection

from models.User import User
from models.Request import Request


from controllers.TokenController import TokenController
from controllers.HubController import HubController
from controllers.RequestController import RequestController
from controllers.UserController import UserController

request_router = APIRouter(tags=['Request'])

#** USER
@request_router.post("/user/send-request")
async def send_request_to_hub(hubID:str,current_user: Annotated[User, Depends(TokenController.get_current_active_user)]):
    request = Request(
        userID=current_user["id"],
        hubID=hubID,
        userRole=current_user["role"],
    )

    insertedRequest = RequestController.create_user_hub_request(request)
    if not insertedRequest:
        raise HTTPException(status_code=500, detail="Erro ao enviar solicitação para o hub")

    return JSONResponse(status_code=200, content={"message": "Solicitação enviada com sucesso"})





# ** HUB
# @request_router.post("/hub/accept-request")
@request_router.get("/hub/get_all_requests/{id}")
async def get_all_requests_from_hub(id: str):
    requests = RequestController.get_all_requests_from_hub(id)
    if not requests:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Nenhum pedido encontrado para este hub")
    return requests

# Aceitar ou recusar pedido do usuário ou validador
@request_router.put("/hub/set-request-status")
async def set_request_status(requestID: str ,requestStatus:str, current_user: Annotated[User, Depends(TokenController.get_current_user_with_role("admin"))]):
    if not requestID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do pedido não fornecido")

    request = RequestController.get_request_by_id(requestID)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
# ** PEGAR A ROLE DO USUÁRIO PRA ADICIONAR EM EMPLOYEE E CLIENTS DENTRO DA COLLECTION HUB

    if status == "approved":
        HubController.add_user_to_hub(current_user["id"])

    updatedRequest = RequestController.set_request_status(requestID, requestStatus)
    if not updatedRequest:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao aceitar o pedido")
    if updatedRequest == "denied":
        return JSONResponse(status_code=200, content={"message": "Pedido recusado"})
    return JSONResponse(status_code=200, content={"message": "Pedido aceito com sucesso"})
