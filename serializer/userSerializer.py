
def convertUser(user) -> dict:

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "created_at": user["created_at"],
        "disabled": user["disabled"]
    }


def convertUsers(users) -> list:
    return [convertUser(user) for user in users]