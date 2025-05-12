import re
from multiple_inheritance.user import User


def handle_user_with_mixins():
    print("Please create your user entering your full name and email address")
    
    while True: 
        name = input("Please enter your full name: ")
        pattern = r'^[A-Za-z\s]{2,}$'
        if re.match(pattern,name):
            break
        else: 
            print("Please enter a valid name using only letters and spaces.")
    
    while True:
        email = input("Please enter your email address: ")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if  re.match(pattern,email): 
            break    
        else: 
            print("Please enter a correct email like nombre@dominio.com")
    
    user =  User(name, email) 
    user.log(f"User {user.name} created at {user.created_at}")
    return user 