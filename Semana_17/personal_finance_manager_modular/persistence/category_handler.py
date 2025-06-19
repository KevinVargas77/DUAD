
import csv
import os
from models.category import Category

CATEGORY_FILE = 'categories.csv'

def save_categories(categories):
    with open(CATEGORY_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'type', 'description'])
        writer.writeheader()
        for cat in categories:
            writer.writerow(cat.to_dict())

def load_categories():
    categories = []
    if not os.path.exists(CATEGORY_FILE):
        return categories

    with open(CATEGORY_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            categories.append(Category.from_dict(row))
    return categories
