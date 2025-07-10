from accounts.bank_account import BankAccount

class SavingsAccount(BankAccount):
    def __init__(self,balance,min_balance):
        if balance < min_balance:
            raise ValueError("Initial balance cannot be lower than the minimum balance.")
        super().__init__(balance)
        self.min_balance = min_balance

    def withdraw(self,amount):
        if self.balance - amount >= self.min_balance:
            super().withdraw(amount)
        else: 
            print(f"Cannot withdraw, balance would go below minimum allowed: ${self.min_balance:.2f}")
    

    def withdraw(self, amount):
        if self.balance - amount >= self.min_balance:
            super().withdraw(amount)
        else: 
            print(f"Cannot withdraw, balance would go below minimum allowed: ${self.min_balance:.2f}")


    def __str__(self):
        return f"SavingsAccount | Balance: ${self.balance:.2f} | Minimum balance: ${self.min_balance:.2f}"
