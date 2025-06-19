# user.py
class User:
    def __init__(self, name, last_name, user_id):
        self.name = name
        self.last_name = last_name
        self.user_id = user_id
        self.incomes = []
        self.expenses = []
        self.budgets = {}
