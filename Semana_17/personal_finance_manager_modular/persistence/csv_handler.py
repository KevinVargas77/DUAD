
import csv
import os
from models.user import User
from models.movement import Movement

USER_FILE = 'users.csv'
MOVEMENTS_FILE = 'movements.csv'

def save_users(users):
    with open(USER_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'name', 'last_name', 'budgets'])
        for user in users:
            budgets_str = ';'.join(f"{k}:{v}" for k, v in user.budgets.items())
            writer.writerow([user.user_id, user.name, user.last_name, budgets_str])

def load_users():
    users = []
    if not os.path.exists(USER_FILE):
        return users

    with open(USER_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = User(row['name'], row['last_name'], row['user_id'])
            if row['budgets']:
                for item in row['budgets'].split(';'):
                    if ':' in item:
                        category, amount = item.split(':')
                        user.budgets[category] = float(amount)
            users.append(user)
    return users

def save_movements(movements_list):
    with open(MOVEMENTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'date', 'title', 'amount', 'category', 'description', 'movement_type'])
        for mov in movements_list:
            writer.writerow([mov.user_id, mov.date, mov.title, mov.amount, mov.category, mov.description, mov.movement_type])

def load_movements():
    movements = []
    if not os.path.exists(MOVEMENTS_FILE):
        return movements
    with open(MOVEMENTS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mov = Movement(
                user_id=row['user_id'],
                title=row['title'],
                amount=float(row['amount']),
                category=row['category'],
                date=row['date'],
                movement_type=row['movement_type'],
                description=row.get('description', '')
            )
            movements.append(mov)
    return movements
