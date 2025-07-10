class Movement:
    def __init__(self, user_id, title, amount, category, date, movement_type, description=""):
        self.user_id = user_id
        self.title = title
        self.amount = amount
        self.category = category
        self.date = date
        self.movement_type = movement_type
        self.description = description
