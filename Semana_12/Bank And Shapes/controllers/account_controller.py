from accounts.savings_account import SavingsAccount 


def handle_savings_account(user): 

    print ("""Welcome! Since you want to create a savings account, please note:
- The minimum balance is $50.
- A deposit of at least $50 is required to activate the account.
""")
    
    proceed = input("Do you want to proceed? (yes/no): ")
    if proceed.lower() == "yes": 
        while True: 
            try:
                deposit = int(input("Please enter the amount to deposit: "))
                if deposit >= 50:
                    break
                else: 
                    print("Please enter an amount higher than $50.00")  
            except ValueError: 
                print("Please enter a valid number")
        
        account = SavingsAccount(balance=deposit, min_balance=50)
        print(f"{user.name}, your savings account has been successfully activated.")
        return account


def handle_withdraw(account):
    if not account:
        print("No account found. Please create one first.")
        return
    
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount > 0:
            account.withdraw(amount)
        else:
            print("Please enter a positive amount.")
    except ValueError:
        print("Invalid input. Please enter a number.")

