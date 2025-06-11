from serializer.userSerializer import convertUser, convertUsers

def convertHub(hub) -> dict:

    employees = hub.get("employees") or []
    clients = hub.get("clients") or []
    # hub["employees"] = convertUsers(hub["employees"]) if employees else []
    # hub["clients"] = convertUsers(hub["clients"]) if clients else []


  

    if hub["employees"] != []:
        convertedHubList = []
        for idHub in hub["employees"]:
            convertedHubList.append(idHub)
        hub["employees"] = convertedHubList


    if hub["clients"] != None:
        convertedHubList = []
        for idHub in hub["clients"]:
            convertedHubList.append(idHub)
        hub["clients"] = convertedHubList

   

    return {
        "id": str(hub["_id"]),
        "hubAdmin": hub["hubAdmin"],
        "name": hub["name"],
        "employees": hub["employees"],
        "clients": hub["clients"],
        "created_at": hub["created_at"],
        "updated_at": hub["updated_at"]
    }


def convertHubs(hubs) -> list:
    return [convertHub(hub) for hub in hubs]


