from datetime import datetime

import random
import string

from bson import ObjectId

from serializer.codeSerializer import convertCodes,convertCode

from models.Code import Code

from dbconfig import requestsCollection, codesCollection

class CodeController:

    def get_codes_by_user(userID: str) -> list[Code] | bool:
        codes = codesCollection.find({"userID": ObjectId(userID)})
        if not codes:
            return False
        codes = convertCodes(codes)
        return codes
    
    def insert_code(code: Code) -> bool:
        code.created_at = datetime.utcnow()
        insert_code = codesCollection.insert_one(dict(code))
        if insert_code:
            return True
        return False

    @classmethod
    def generate_validation_code(cls,userID: str) -> bool | Code:
        """
        Gera um código de validação de 16 dígitos para o usuário.
        O código é válido por um período especificado em minutos (default: 60 minutos).
        """
        expiration = 2
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        expiration_date = datetime.utcnow().timestamp() + (expiration * 60)  # Expiração em segundos

        # Armazenar o código e a data de expiração no banco de dados
        code = Code(
            userID=userID,
            code=code,
            expirationDate=datetime.fromtimestamp(expiration_date),
            created_at=datetime.utcnow()
        )
        
        insert_code = cls.insert_code(code)
        if not insert_code:
            return False
        # Retorna o código gerado
        return code
       
    def validate_code(code: str) -> dict:
        code_data = codesCollection.find_one({"code": code})
        if not code_data:
            return {"error": "Código inválido"}

        # Verifica se o código está expirado
        if code_data["expirationDate"] < datetime.utcnow():
            # Deleta o código expirado do banco de dados
            codesCollection.delete_one({"_id": code_data["_id"]})
            return {"error": "Código expirado"}

        # Atualiza o campo "updated_at" com a data/hora atual e "verified" para True
        updatedCode = codesCollection.find_one_and_update(
            {"_id": code_data["_id"]},
            {"$set": {"updated_at": datetime.utcnow(), "verified": True}},
            return_document=True
        )
        
        if not updatedCode:
            return {"error": "Erro ao atualizar o código"}

        return convertCode(updatedCode)
