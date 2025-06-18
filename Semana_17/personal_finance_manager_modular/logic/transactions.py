from models.movement import Movement
from persistence.csv_handler import save_movements, load_movements
from logic.user_manager import UserManager

class TransactionManager:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.movements = load_movements()

    def add_movement(self, user_id, title, amount, category, date, movement_type, description=""):
        user = self.user_manager.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if amount <= 0:
            raise ValueError("Amount must be a positive number")

        movement = Movement(user_id, title, amount, category, date, movement_type, description)
        self.movements.append(movement)
        save_movements(self.movements)

        return movement

    def get_user_movements(self, user_id, movement_type=None):
        return [
            mov for mov in self.movements
            if mov.user_id == user_id and (movement_type is None or mov.movement_type == movement_type)
        ]
