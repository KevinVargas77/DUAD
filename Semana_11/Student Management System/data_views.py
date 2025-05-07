"""views: will contain all the logic related to the averages and student list."""

from tabulate import tabulate

def all_students(students):
    table = []
    for student in students:
        row = [student.full_name, student.section]

        for subject_name in ["Spanish", "English", "Social_studies", "Science"]:
            grade = next((s.grade for s in student.subjects if s.name == subject_name), None)
            row.append(grade)
        table.append(row)

    headers = ["Full Name", "Section", "Spanish", "English", "Social", "Science"]
    print(tabulate(table, headers=headers, tablefmt="grid"))

def sorted_averages(students):
    return sorted(students, key=lambda s: s.average(), reverse=True)

def top_3_averages(students):
    top_3 = sorted_averages(students)[:3]
    for i, student in enumerate(top_3, 1):
        print(f"Top #{i}: {student.full_name} - Average: {student.average():.2f}")

def general_average(students):
    if not students:
        return 0
    total = sum(student.average() for student in students)
    return total / len(students)
