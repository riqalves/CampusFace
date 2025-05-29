from datetime import datetime
from bson import ObjectId,errors
from serializer.hubSerializer import convertHub, convertHubs

from fastapi import status, HTTPException

from models.Hub import Hub, HubOut

from dbconfig import hubsCollection


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


    # def aprove_request

    # def aprove_client_request

    # def aprove_employee_request