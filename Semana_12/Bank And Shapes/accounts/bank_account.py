class BankAccount:
    def __init__(self,balance):
        self.balance = balance 


    def deposit(self, amount):
            if amount > 0:
                self.balance += amount
                print(f"Thank you for your deposit, your current balance is: ${self.balance:.2f}")
            else: 
                print(f"Please enter a correct amount in dollars to deposit, ${amount} is not correct")


    def withdraw(self,amount):
            if amount > self.balance:
                print(f"Insufficient funds, your current balance is: ${self.balance:.2f}") 
            elif amount > 0:
                self.balance -= amount
                print(f"Thank you for using our services, your current balance is: ${self.balance:.2f}")
            else: 
                print(f"Please enter a correct amount in dollars to withdraw, ${amount} is not correct")


    def get_balance(self):
        print(f"your correct account balance is ${self.balance:.2f} ")


    def __str__(self):
        return f"BankAccount balance: ${self.balance:.2f}"


