
def convertUser(user) -> dict:


    roles = user.get("roles") or []


    if user["roles"] != []:
        convertedUserList = []
        for idUser in user["roles"]:
            convertedUserList.append(idUser)
        user["roles"] = convertedUserList



    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "birthDate":user["birthDate"],
        "cpf":user["cpf"],
        "roles": user["roles"],
        "disabled": user["disabled"],
        "imagePath": user["imagePath"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def convertUsers(users) -> list:
    return [convertUser(user) for user in users]


# class User(BaseModel):
#     username: str
#     email: EmailStr
#     password: str
#     birthDate: datetime
#     cpf: str
#     role: str
#     disabled: bool | None = None
#     created_at: Optional[datetime] = None
#     updated_at: Optional[datetime] = None