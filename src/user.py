import bcrypt
import json
import os
from database import Database

USERS_FILE = "users.json"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

class UserManager:
    def __init__(self):
        self.db = Database()

    def register_user(self, username, password, email="", full_name=""):
        if not username or not password:
            return False, "Kullanıcı adı ve şifre boş olamaz"
        
        if len(password) < 6:
            return False, "Şifre en az 6 karakter olmalıdır"
        
        if self.db.register_user(username, password, email, full_name):
            return True, "Kayıt başarılı!"
        return False, "Bu kullanıcı adı zaten kullanılıyor"

    def login_user(self, username, password):
        if not username or not password:
            return False, "Kullanıcı adı ve şifre boş olamaz"
        
        if self.db.verify_user(username, password):
            user_id = self.db.get_user_id(username)
            return True, user_id
        return False, "Kullanıcı adı veya şifre hatalı"

    def get_user_info(self, user_id):
        return self.db.get_user_info(user_id)

    def update_user_info(self, user_id, email="", full_name=""):
        return self.db.update_user_info(user_id, email, full_name)
