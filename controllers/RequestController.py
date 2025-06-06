from datetime import datetime

from bson import ObjectId

from serializer.requestSerializer import convertRequests
from serializer.userSerializer import convertUser

from models.User import User
from models.Request import Request

from dbconfig import requestsCollection

class RequestController:

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

    def set_request_status(id: str, status: str) -> bool:
        update_fields = {"status": status}
        now = datetime.utcnow()

        if status == "approved":
            update_fields["approved_at"] = now
        else:
            update_fields["updated_at"] = now

        updatedRequest = requestsCollection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_fields}
        )
        if updatedRequest:
            return True
        return False


    def get_all_requests_from_hub(hubID: str) -> list[Request] | bool:
        print("========================================================")
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
            

