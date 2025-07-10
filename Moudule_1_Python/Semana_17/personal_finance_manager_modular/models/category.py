
class Category:
    def __init__(self, name, type_, description):
        self.name = name
        self.type_ = type_
        self.description = description

    def __str__(self):
        return f"{self.name} ({self.type_})"

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type_,
            "description": self.description
        }

    @staticmethod
    def from_dict(data):
        return Category(data["name"], data["type"], data["description"])
