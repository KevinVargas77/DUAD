
import pytest
from logic.user_manager import UserManager
from logic.transactions import TransactionManager
from models.movement import Movement

@pytest.fixture
def user_manager():
    return UserManager()

@pytest.fixture
def transaction_manager(user_manager):
    return TransactionManager(user_manager)

def test_create_user(user_manager):
    user = user_manager.add_user("Test", "User")
    assert user.name == "Test"
    assert user.last_name == "User"
    assert len(user.user_id) > 0

def test_create_movement(transaction_manager, user_manager):
    user = user_manager.add_user("Move", "Tester")
    movement = transaction_manager.add_movement(
        user_id=user.user_id,
        title="Test Income",
        amount=1000.0,
        category="Salary",
        date="2025-01-01",
        movement_type="income"
    )
    assert isinstance(movement, Movement)
    assert movement.title == "Test Income"
    assert movement.amount == 1000.0

def test_get_user_movements(transaction_manager, user_manager):
    user = user_manager.add_user("Calc", "Tester")
    transaction_manager.add_movement(user.user_id, "Income", 1000, "Work", "2025-01-01", "income")
    transaction_manager.add_movement(user.user_id, "Expense", 200, "Food", "2025-01-02", "expense")
    movements = transaction_manager.get_user_movements(user.user_id)
    income = sum(m.amount for m in movements if m.movement_type == "income")
    expense = sum(m.amount for m in movements if m.movement_type == "expense")
    assert income == 1000
    assert expense == 200

def test_error_invalid_user(transaction_manager):
    with pytest.raises(ValueError, match="User not found"):
        transaction_manager.add_movement(
            user_id="INVALID",
            title="Fail Case",
            amount=500,
            category="Error",
            date="2025-01-01",
            movement_type="income"
        )

import pytest
from logic.user_manager import UserManager
from logic.transactions import TransactionManager
from logic.budgets import BudgetManager
from models.category import Category
from datetime import date

@pytest.fixture
def setup_managers():
    um = UserManager()
    user = um.add_user("Test", "User")
    tm = TransactionManager(um)
    bm = BudgetManager()
    return um, tm, bm, user.user_id

def test_add_movement_and_total(setup_managers):
    um, tm, bm, uid = setup_managers
    tm.add_movement(uid, "Salary", 1000, "Job", date.today().isoformat(), "income")
    tm.add_movement(uid, "Lunch", 200, "Food", date.today().isoformat(), "expense")
    movements = tm.get_user_movements(uid)
    income = sum(m.amount for m in movements if m.movement_type == "income")
    expense = sum(m.amount for m in movements if m.movement_type == "expense")
    assert income == 1000
    assert expense == 200

def test_invalid_user_for_movement(setup_managers):
    _, tm, _, _ = setup_managers
    with pytest.raises(ValueError):
        tm.add_movement("invalid_id", "Test", 100, "Misc", date.today().isoformat(), "income")

def test_set_and_get_budget(setup_managers):
    _, tm, bm, uid = setup_managers
    category = "Food"
    bm.set_budget(uid, category, 500)
    remaining = bm.get_remaining_budget(uid, category, tm)
    assert remaining == 500

def test_budget_after_expense(setup_managers):
    um, tm, bm, uid = setup_managers
    category = "Entertainment"
    bm.set_budget(uid, category, 300)
    tm.add_movement(uid, "Movie", 50, category, date.today().isoformat(), "expense")
    remaining = bm.get_remaining_budget(uid, category, tm)
    assert remaining == 250
