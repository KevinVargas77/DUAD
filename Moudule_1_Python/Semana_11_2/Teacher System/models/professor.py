class Professor:
    def __init__(self, id, full_name, sections):
        self.id = id
        self.full_name = full_name
        self.sections = sections


    def add_section(self, section):
        self.sections.append(section)


    def global_average_all_sections(self):
        total = 0
        count = 0
        for section in self.sections:
            for student in section.students:
                total += student.average()
                count += 1
        return total / count if count > 0 else 0


    def top_3_global_students(self):
        all_students = []
        for section in self.sections:
            all_students.extend(section.students)

        sorted_list = sorted(all_students, key=lambda x: x.average(), reverse=True)

        for i, student in enumerate(sorted_list[:3], 1):
            print(f"Top #{i}: {student.full_name} - Avg: {student.average():.2f}")
