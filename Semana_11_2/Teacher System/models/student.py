class Student:
    def __init__(self, full_name, section, subjects):
        self.full_name = full_name
        self.section = section
        self.subjects = subjects

    def average(self):
        total = sum(subject.grade for subject in self.subjects)
        return total / len(self.subjects)

    def __repr__(self):
        return f"{self.full_name} - Avg: {self.average():.2f}"
