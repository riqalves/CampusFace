
def convertUser(user) -> dict:

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "birthDate":user["birthDate"],
        "cpf":user["cpf"],
        "role": user["role"],
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