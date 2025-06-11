
def convertCode(code) -> dict:

    return {
        "id": str(code["_id"]),
        "code": code["code"],
        "userID": code["userID"],
        "verified": code["verified"],
        "expirationDate": code["expirationDate"],
        "created_at": code["created_at"],
        "updated_at": code["updated_at"]
    }
   
def convertCodes(codes) -> list:
    return [convertCode(code) for code in codes]

