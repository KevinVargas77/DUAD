import re
from multiple_inheritance.user import User
from datetime import datetime


def handle_user_with_mixins():
    print("Please create your user entering your full name and email address")
    
    while True: 
        name = input("Please enter your full name: ")
        pattern = r'^[A-Za-z\s]{2,}$'
        if re.match(pattern, name):
            break
        else: 
            print("Please enter a valid name using only letters and spaces.")
    
    while True:
        email = input("Please enter your email address: ")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if re.match(pattern, email): 
            break    
        else: 
            print("Please enter a correct email like nombre@dominio.com")


    while True:
        dob_input = input("Please enter your date of birth (YYYY-MM-DD): ")
        try:
            date_of_birth = datetime.strptime(dob_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD (e.g., 1990-05-13).")

    user = User(name, email, date_of_birth)

    print(f"{user.info} | Created: {user.created_at_datetime} | Days active: {user.days_active}")
    
    return user
