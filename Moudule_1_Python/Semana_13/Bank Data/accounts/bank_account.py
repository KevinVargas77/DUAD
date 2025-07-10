
def validate_positive_amount(func):  #Exercise 2
    def wrapper(self, amount, *args, **kwargs):
        if amount <= 0:
            print(f"Invalid amount: ${amount}. Please enter a positive value.")
            return
        return func(self, amount, *args, **kwargs)
    return wrapper


def validate_numeric_params(func): #Exercise 2
    def wrapper(*args, **kwargs):
        for arg in args[1:]: 
            if not isinstance(arg, (int, float)):
                raise TypeError(f"All arguments must be numeric. Invalid value: {arg}")
        return func(*args, **kwargs)
    return wrapper


class BankAccount:
    def __init__(self, balance):
        self.balance = balance


    @validate_numeric_params
    @validate_positive_amount
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposit successful. Balance: ${self.balance:.2f}")

        
    @validate_numeric_params
    @validate_positive_amount
    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Insufficient funds. Balance: ${self.balance:.2f}")
        else:
            self.balance -= amount
            print(f"Withdrawal successful. Balance: ${self.balance:.2f}")

    def get_balance(self):
        print(f"Balance: ${self.balance:.2f}")

    def __str__(self):
        return f"BankAccount balance: ${self.balance:.2f}"
