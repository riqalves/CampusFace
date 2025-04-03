
def convertUser(user) -> dict:

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "role": user["role"],
        "disabled": user["disabled"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def convertUsers(users) -> list:
    return [convertUser(user) for user in users]