from models.user import User
from random import randint
from persistence.csv_handler import save_users, load_users

class UserManager:
    def __init__(self):

        self.users = load_users()

    def list_users(self):
        return self.users

    def generate_unique_user_id(self, name, last_name):
        initials = (name[0] + last_name[0]).upper()
        while True:
            user_id = f"{initials}{randint(100,999)}"
            if all(user.user_id != user_id for user in self.users):
                return user_id

    def add_user(self, name, last_name):
        user_id = self.generate_unique_user_id(name, last_name)
        new_user = User(name, last_name, user_id)
        self.users.append(new_user)
        save_users(self.users) 
        return new_user

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
