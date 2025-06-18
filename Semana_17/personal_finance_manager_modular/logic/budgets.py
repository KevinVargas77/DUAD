
import csv
import os

BUDGETS_FILE = 'budgets.csv'

class BudgetManager:
    def __init__(self):
        self.budgets = self.load_budgets()

    def set_budget(self, user_id, category, amount):
        if amount <= 0:
            raise ValueError("Budget amount must be a positive number")

        if user_id not in self.budgets:
            self.budgets[user_id] = {}
        self.budgets[user_id][category] = amount
        self.save_budgets()

    def get_budget(self, user_id, category):
        return self.budgets.get(user_id, {}).get(category, 0)

    def get_remaining_budget(self, user_id, category, transaction_manager):
        budget = self.get_budget(user_id, category)
        total_spent = sum(
            m.amount for m in transaction_manager.get_user_movements(user_id)
            if m.category == category and m.movement_type == "expense"
        )
        return budget - total_spent

    def load_budgets(self):
        if not os.path.exists(BUDGETS_FILE):
            return {}
        budgets = {}
        with open(BUDGETS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                uid = row['user_id']
                cat = row['category']
                amt = float(row['amount'])
                if uid not in budgets:
                    budgets[uid] = {}
                budgets[uid][cat] = amt
        return budgets

    def save_budgets(self):
        with open(BUDGETS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['user_id', 'category', 'amount'])
            writer.writeheader()
            for uid, cats in self.budgets.items():
                for cat, amt in cats.items():
                    writer.writerow({'user_id': uid, 'category': cat, 'amount': amt})
