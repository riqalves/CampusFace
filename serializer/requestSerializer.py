
def convertRequest(request) -> dict:

    return {
        "id": str(request["_id"]),
        "userID": request["userID"],
        "hubID": request["hubID"],
        "userRole": request["userRole"],
        "status": request["status"],
        "approved_at": request["approved_at"],
        "created_at": request["created_at"],
        "updated_at": request["updated_at"]
    }
   
def convertRequests(requests) -> list:
    return [convertRequest(request) for request in requests]

