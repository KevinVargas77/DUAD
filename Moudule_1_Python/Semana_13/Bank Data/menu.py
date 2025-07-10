from controllers.user_controller import handle_user_with_mixins
from controllers.account_controller import handle_savings_account, handle_withdraw
from accounts.currency_exchange import currency_exchange


def simple_log(func):
    def wrapper(*args, **kwargs):
        print(">> Running Bank App, Welcome!")  
        return func(*args, **kwargs)
    return wrapper


def show_menu():
    account = None
    print("Welcome! Let's create your user first.")
    current_user = handle_user_with_mixins()

    while True:
        print(f"\nWhat would you like to do, {current_user.name}?")
        print("1. Create savings account")
        print("2. View account balance")
        print("3. Withdraw money")
        print("4. Currency Exchange")
        print("5. Exit")

        option = input("Select an option: ")

        if option == "1":
            account = handle_savings_account(current_user)
        elif option == "2":
            if account:
                print(account)
            else:
                print("No account created yet.")
        elif option == "3":
            if account:
                handle_withdraw(account)
            else:
                print("No account found. Please create one first.")
        elif option == "4":
            currency_exchange()
        elif option == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
