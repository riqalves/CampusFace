from datetime import datetime

from bson import ObjectId
import jwt
from passlib.context import CryptContext

from serializer.userSerializer import convertUser

from models.User import User, UpdateUserCredentials

from dbconfig import usersCollection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserController:
    
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(password)->str:
        return pwd_context.hash(password)

    def get_user(username: str)->dict:
        user_data = usersCollection.find_one({"username": username})
        if user_data:
            return convertUser(user_data)
            
    def get_user_by_email(email: str)-> User:
        user = usersCollection.find_one({'email': email})
        if not user:
            return print("Usuário não encontrado")
        return convertUser(user)


    def is_email_valid(email: str)-> bool:
        user = usersCollection.find_one({'email': email})
        # Se o usuário de mesmo email não for encontrado, logo é possível cadastrar
        if not user:
            return True
        return False

    def insert_user(user: User) -> bool:
        user.created_at = datetime.utcnow()
        user.password =  UserController.get_password_hash(user.password)
        user.disabled = False
        insert = usersCollection.insert_one(dict(user))
        if insert:
            return True
        return False

    def update_user_credentials(id:str,userCredentials: UpdateUserCredentials) -> bool:
        userCredentials.password = UserController.get_password_hash(userCredentials.password)
        userCredentials.updated_at = datetime.utcnow()
        userUpdated = usersCollection.find_one_and_update({"_id": ObjectId(id)},{"$set": dict(userCredentials)})
        if userUpdated:
            return True
        return False

    def delete_user(id:str):
        deletedUser = usersCollection.find_one_and_delete({"_id": ObjectId(id)})
        if deletedUser:
            return True
        return False

    


    


    

    