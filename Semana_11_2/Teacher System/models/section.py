class Section:
    def __init__(self, name, students):
        self.name = name
        self.students = students

    def students(self,student):
        self.students.append(student)
    
    def global_average(self):
        total = 0
        for student in self.students:
            total += student.average()
        return total / len(self.students) if self.students else 0

    def top_3_students(self):
        sorted_list = sorted(self.students, key = lambda x : x.average() , reverse=True)
        return sorted_list[:3]
