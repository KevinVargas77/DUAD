
from subject import Subject

class Student: 
    def __init__(self, full_name, section, subjects):
        self.full_name = full_name
        self.section = section 
        self.subjects = subjects  # lista de objetos Subject
    
    def average(self):
        total = sum(subject.grade for subject in self.subjects)
        return total / len(self.subjects)

    def to_dict(self):
        return {
            "Full_name": self.full_name,
            "Section": self.section,
            **{s.name + "_grade": s.grade for s in self.subjects}
        }

    def __repr__(self):
        return f"{self.full_name} - {self.section} - Avg: {self.average():.2f}"
