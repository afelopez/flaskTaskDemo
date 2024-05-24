from flask_login import UserMixin

from .firestore_service import get_user

class UserDTO:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserModel(UserMixin):
    def __init__(self, userdto):
        self.id = userdto.username
        self.password = userdto.password
    
    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        userdto = UserDTO(
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )
        
        return UserModel(userdto)