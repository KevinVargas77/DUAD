class Subject:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade 

    def __repr__(self):
        return f"{self.name}: {self.grade}"

