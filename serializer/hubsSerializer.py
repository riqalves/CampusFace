
def convertHub(hub) -> dict:

    if hub["employees"] != None:
        convertedHubList = []
        for idHub in hub["employees"]:
            convertedHubList.append(idHub)
        hub["employees"] = convertedHubList


    return {
        "id": str(hub["_id"]),
        "name": hub["name"],
        "employees": hub["employees"],
        "clients": hub["employees"],
        "created_at": hub["created_at"],
        "updated_at": hub["updated_at"]
    }


def convertHubs(hubs) -> list:
    return [convertHub(hub) for hub in hubs]


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