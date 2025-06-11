from datetime import datetime

from fastapi import HTTPException, status

from bson import ObjectId

from serializer.requestSerializer import convertRequests, convertRequest
from serializer.userSerializer import convertUser

from controllers.HubController import HubController

from models.User import User
from models.Request import Request

from dbconfig import requestsCollection

class RequestController:

    def get_request_by_id(id: str) -> Request | bool:
        request = requestsCollection.find_one({"_id": ObjectId(id)})
        if not request:
            return False
        request = convertRequest(request)
        return request

#** FROM USERS

    def create_user_hub_request(request: Request)-> bool:
        request.created_at = datetime.utcnow()

        insert_request = requestsCollection.insert_one(dict(request))
        if insert_request:
            return True
        return False

    def get_user_requests(userID: str) -> list[Request] | bool:
        requests = requestsCollection.find({"userID": userID})
        requests = convertRequests(requests)
        if not requests:
            return False
        return requests



    # * FROM HUB

    def set_request_status(requestID: str, status: str) -> dict | bool:
        update_fields = {"status": status}
        now = datetime.utcnow()


        print("========================================================")
        print(requestID, status)
        # Busca a request para pegar userID, hubID e role
        request = requestsCollection.find_one({"_id": ObjectId(requestID)})
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitação não encontrada."
            )

        user_id = request["userID"]
        hub_id = request["hubID"]
        user_role = request["userRole"]

        if status == "approved":
            update_fields["approved_at"] = now
            # Adiciona o userID ao campo correto do hub conforme a role
            if user_id and hub_id and user_role:
                addUser = HubController.add_user_to_hub(hub_id, user_id, user_role)
                if not addUser:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Erro ao adicionar usuário ao hub."
                    )
        else:
            update_fields["updated_at"] = now

        updatedRequest = requestsCollection.find_one_and_update(
            {"_id": ObjectId(requestID)},
            {"$set": update_fields}
        )
        if updatedRequest["status"] == "approved":
            return "approved"
        return "denied"


    def get_all_requests_from_hub(hubID: str) -> list[Request] | bool:
        requests = requestsCollection.find({"hubID": hubID})

        if not requests:
            return False
        requests = convertRequests(requests)

        return requests
    






    # def set_request_status(id: str, status: str)-> bool:

    #     approved_at = None
    #     updated_at = None
        
    #     if status == "approved":
    #         approved_at = datetime.utcnow()
    #     else:
    #         updated_at = datetime.utcnow()

        
    #     status= status,
    #     updated_at=str(updated_at),
    #     approved_at=str(approved_at)

    #     updatedRequest = requestsCollection.find_one_and_update({{"_id": ObjectId(id)}, {"$set": {"status":status}}})
    #     if updatedRequest:
    #         return True
    #     return False
            

