
import PySimpleGUI as sg
from logic.user_manager import UserManager
from logic.transactions import TransactionManager
from datetime import date
from persistence.category_handler import load_categories, save_categories
from models.category import Category

class DashboardApp:
    def __init__(self):
        self.user_manager = UserManager()
        self.transaction_manager = TransactionManager(self.user_manager)
        self.categories = load_categories()
        self.layout = self.build_layout()
        self.window = sg.Window('Personal Finance Dashboard', self.layout, resizable=True, finalize=True)

    def build_layout(self):
        today = date.today().strftime("%Y-%m-%d")
        sg.theme('DarkBlue3')

        top_banner = [[
            sg.Text('Finance Manager', font='Any 20', background_color='#1B2838'),
            sg.Push(background_color='#1B2838'),
            sg.Text(f'Date: {today}', font='Any 14', background_color='#1B2838')
        ]]

        user_block = [
            [sg.Text('First Name:'), sg.Input(key='-NAME-')],
            [sg.Text('Last Name:'), sg.Input(key='-LASTNAME-')],
            [sg.Button('Create User'), sg.Button('Load Users')],
            [sg.Text('Registered Users')],
            [sg.Table(values=[], headings=['ID', 'First', 'Last'],
                      key='-USERS_TABLE-', enable_events=True,
                      auto_size_columns=False, col_widths=[18, 18, 18],
                      justification='left', expand_x=True, num_rows=5)]
        ]

        movement_block = [
            [sg.Text('User ID:'), sg.Input(key='-USERID-')],
            [sg.Text('Title:'), sg.Input(key='-TITLE-')],
            [sg.Text('Amount:'), sg.Input(key='-AMOUNT-')],
            [sg.Text('Category:'), sg.Combo(values=[str(cat) for cat in self.categories], key='-CATEGORY-', enable_events=True)],
            [sg.Text('Date (YYYY-MM-DD):'), sg.Input(default_text=today, key='-DATE-')],
            [sg.Text('Type:'), sg.Combo(['income', 'expense'], key='-TYPE-')],
            [sg.Button('Add Movement'), sg.Button('View Movements'), sg.Button('Manage Categories'), sg.Button('Manage Budgets')],
            [sg.Text('Movements:')],
            [sg.Table(values=[], headings=['Date', 'Title', 'Amount', 'Category', 'Type'],
                      key='-MOVEMENTS_TABLE-', justification='left',
                      auto_size_columns=False, col_widths=[12, 18, 10, 18, 10],
                      expand_x=True, num_rows=6)],
            [sg.Text('Income:'), sg.Text('₡0', key='-INCOME-'),
             sg.Text('Expenses:'), sg.Text('₡0', key='-EXPENSE-'),
             sg.Text('Total:'), sg.Text('₡0', key='-TOTAL-', text_color='white')]
        ]

        layout = [
            [sg.Frame('', top_banner, background_color='#1B2838', expand_x=True, border_width=0)],
            [sg.Frame('Create User', user_block, pad=(10, 10)),
             sg.Frame('Add Movement', movement_block, pad=(10, 10))],
            [sg.Button('Exit')]
        ]
        return layout

    def update_user_table(self):
        users = self.user_manager.list_users()
        table_data = [[u.user_id, u.name, u.last_name] for u in users]
        self.window['-USERS_TABLE-'].update(values=table_data)

    def update_movement_table(self, user_id):
        movements = self.transaction_manager.get_user_movements(user_id)
        income = sum(m.amount for m in movements if m.movement_type == 'income')
        expense = sum(m.amount for m in movements if m.movement_type == 'expense')
        total = income - expense

        rows = [[m.date, m.title, m.amount, m.category, m.movement_type] for m in movements]
        self.window['-MOVEMENTS_TABLE-'].update(values=rows)
        self.window['-INCOME-'].update(f"₡{income:,.0f}")
        self.window['-EXPENSE-'].update(f"₡{expense:,.0f}")
        self.window['-TOTAL-'].update(f"₡{total:,.0f}", text_color='red' if total < 0 else 'green')

    def manage_categories_window(self):
        layout = [
            [sg.Text("Name:"), sg.Input(key='-NEW_NAME-')],
            [sg.Text("Type:"), sg.Combo(['income', 'expense'], key='-NEW_TYPE-')],
            [sg.Text("Description:"), sg.Input(key='-NEW_DESC-')],
            [sg.Button("Add"), sg.Button("Close")]
        ]
        win = sg.Window("Manage Categories", layout, modal=True)
        while True:
            event, values = win.read()
            if event in (sg.WIN_CLOSED, 'Close'):
                break
            if event == 'Add':
                name = values['-NEW_NAME-'].strip()
                type_ = values['-NEW_TYPE-']
                desc = values['-NEW_DESC-'].strip()
                if name and type_:
                    new_cat = Category(name, type_, desc)
                    self.categories.append(new_cat)
                    save_categories(self.categories)
                    self.window['-CATEGORY-'].update(values=[str(c) for c in self.categories])
                    sg.popup("Category added")
        win.close()

    def manage_budget_window(self):
        layout = [
            [sg.Text("User ID:"), sg.Input(key='-BUDGET_UID-')],
            [sg.Text("Category:"), sg.Combo(values=[str(c) for c in self.categories], key='-BUDGET_CAT-')],
            [sg.Text("Amount:"), sg.Input(key='-BUDGET_AMT-')],
            [sg.Button("Set Budget"), sg.Button("View Budget"), sg.Button("Close")]
        ]
        win = sg.Window("Manage Budgets", layout, modal=True)
        from logic.budgets import BudgetManager
        budget_manager = BudgetManager()

        while True:
            event, values = win.read()
            if event in (sg.WIN_CLOSED, 'Close'):
                break
            if event == 'Set Budget':
                user_id = values['-BUDGET_UID-'].strip()
                cat_str = values['-BUDGET_CAT-']
                amt = values['-BUDGET_AMT-'].strip()
                try:
                    amount = float(amt)
                    category = next((c.name for c in self.categories if str(c) == cat_str), None)
                    if not category:
                        raise ValueError("Invalid category")
                    budget_manager.set_budget(user_id, category, amount)
                    sg.popup("Budget set successfully")
                except Exception as e:
                    sg.popup(f"Error: {e}")

            if event == 'View Budget':
                user_id = values['-BUDGET_UID-'].strip()
                cat_str = values['-BUDGET_CAT-']
                try:
                    category = next((c.name for c in self.categories if str(c) == cat_str), None)
                    if not category:
                        raise ValueError("Invalid category")
                    remaining = budget_manager.get_remaining_budget(user_id, category, self.transaction_manager)
                    sg.popup(f"Remaining Budget for {category}: ₡{remaining:,.0f}")
                except Exception as e:
                    sg.popup(f"Error: {e}")

        win.close()

    def run(self):
        self.update_user_table()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            if event == 'Create User':
                name = values['-NAME-'].strip()
                lastname = values['-LASTNAME-'].strip()
                if name and lastname:
                    user = self.user_manager.add_user(name, lastname)
                    sg.popup(f"User created: {user.user_id}")
                    self.update_user_table()
                    self.window['-NAME-'].update('')
                    self.window['-LASTNAME-'].update('')

                else:
                    sg.popup("Please fill in both name and last name.")

            if event == 'Load Users':
                self.update_user_table()
                sg.popup("Users loaded from file")

            if event == 'Add Movement':
                if not self.categories:
                    sg.popup("No categories available. Please add one first.")
                    continue

                user_id = values['-USERID-'].strip()
                title = values['-TITLE-'].strip()
                amount = values['-AMOUNT-'].strip()
                cat_str = values['-CATEGORY-']
                date_str = values['-DATE-'].strip()
                mtype = values['-TYPE-']

                if not all([user_id, title, amount, cat_str, mtype]):
                    sg.popup("All fields are required")
                    continue

                try:
                    amount = float(amount)
                    category = next((c.name for c in self.categories if str(c) == cat_str), None)
                    if not category:
                        raise ValueError("Invalid category")
                    self.transaction_manager.add_movement(
                        user_id=user_id, title=title, amount=amount,
                        category=category, date=date_str, movement_type=mtype
                    )
                    sg.popup("Movement added successfully")
                    self.update_movement_table(user_id)

                    self.window['-TITLE-'].update('')
                    self.window['-AMOUNT-'].update('')
                    self.window['-CATEGORY-'].update('')
                    self.window['-TYPE-'].update('')

                except Exception as e:
                    sg.popup(f"Error: {e}")

            if event == 'View Movements':
                uid = values['-USERID-'].strip()
                if uid:
                    self.update_movement_table(uid)
                else:
                    sg.popup("User ID required")

            if event == '-USERS_TABLE-':
                selection = values['-USERS_TABLE-']
                if selection:
                    index = selection[0]
                    user = self.user_manager.list_users()[index]
                    self.window['-USERID-'].update(user.user_id)
                    self.update_movement_table(user.user_id)

            if event == 'Manage Categories':
                self.manage_categories_window()

            if event == 'Manage Budgets':
                self.manage_budget_window()

        self.window.close()
