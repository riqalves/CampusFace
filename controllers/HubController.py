from datetime import datetime
from bson import ObjectId,errors
from serializer.hubSerializer import convertHub, convertHubs

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse

from models.Hub import Hub, HubOut
from models.Request import Request

from serializer.userSerializer import convertUser,  convertUsers

from dbconfig import hubsCollection
from dbconfig import usersCollection


class HubController:
    
    async def get_hub_by_id(id: str) -> HubOut | None:
        try:
            obj_id = ObjectId(id)
        except (errors.InvalidId, TypeError):
            return None

        hub = hubsCollection.find_one({"_id": obj_id})
        return HubOut(**convertHub(hub)) if hub else None
            

        
            
    # def get_employees(email: str)
        

    # def get_clients()



    def insert_hub(hub: Hub) -> bool:
        hub.created_at = datetime.utcnow()
        hub.employees = []
        hub.clients = []
        insert = hubsCollection.insert_one(dict(hub))
        if insert:
            return True
        return False


    def get_all_hubs()-> dict:
        try:
            hubs = hubsCollection.find()
            if not hubs:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Nenhum hub adicionado. Erro ao consultar hub")
            convertedHubs = convertHubs(hubs)

            if convertedHubs == []:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Nenhum hub adicionado")
                
            return convertedHubs
        except HTTPException as error:
            raise error
        
    def add_user_to_hub(hubID: str, userID: str, user_role: str) -> bool:
        """
        Adiciona o userID ao campo correto (clients ou employees) do hub, conforme a role.
        """
        user = usersCollection.find_one({"_id": ObjectId(userID)})
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        user = convertUser(user)
        print(f"Adicionando usuário {userID} ao hub {hubID} com a role {user_role}")
        if user_role == "client":
            update_field = "clients"
        elif user_role == "validator":
            update_field = "employees"
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Role de usuário inválida para associação ao hub.")

        updated_hub = hubsCollection.find_one_and_update(
            {"_id": ObjectId(hubID)},
            {"$addToSet": {update_field: user}}
        )
        if not updated_hub:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hub não encontrado")
        return True


    def remove_employee_from_hub(hubID: str, userID: str) -> bool:
        updated_hub = hubsCollection.find_one_and_update(
            {"_id": ObjectId(hubID)},
            {"$pull": {"employees": userID}}
        )
        if not updated_hub:
            return False
        return True

    def remove_client_from_hub(hubID: str, userID: str) -> bool:
            updated_hub = hubsCollection.find_one_and_update(
                {"_id": ObjectId(hubID)},
                {"$pull": {"clients": userID}}
            )
            if not updated_hub:
                return False
            return True
        

    def get_validators_from_hub(hubID: str) -> list[Request] | bool:
        """
        Retorna todos os validadores de um hub.
        """
        try:
            hub = hubsCollection.find_one({"_id": ObjectId(hubID)})
            if not hub:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hub não encontrado")
            validators = hub.get("employees", [])
            return validators
        except errors.InvalidId:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="ID do hub inválido")
    







        
    # def update_hub_credentials(id:str,userCredentials: UpdateUserCredentials) -> bool:
    #     userCredentials.password = UserController.get_password_hash(userCredentials.password)
    #     userCredentials.updated_at = datetime.utcnow()
    #     userUpdated = hubsCollection.find_one_and_update({"_id": ObjectId(id)},{"$set": dict(userCredentials)})
    #     if userUpdated:
    #         return True
    #     return False

    # def delete_hub(id:str):
    #     deletedHub = hubsCollection.find_one_and_delete({"_id": ObjectId(id)})
    #     if deletedHub:
    #         return True
    #     return False

