"""views: will contain all the logic related to the averages and student list."""

from tabulate import tabulate


def all_students(students):
    table = []
    for student in students:
        table.append([
            student['Full_name'],
            student['Section'],
            student['Spanish_grade'],
            student['English_grade'],
            student['Social_studies_grade'],
            student['Science_grade']
        ])
    headers = ["Full Name", "Section", "Spanish", "English", "Social", "Science"]
    print(tabulate(table, headers=headers, tablefmt="grid"))


def sorted_averages(students):
    averages = []
    for student in students:
        average = (
            student["Spanish_grade"]
            + student["English_grade"]
            + student["Social_studies_grade"]
            + student["Science_grade"]
        ) / 4
        entry = (average, student)
        averages.append(entry)
    sorted_list = sorted(averages, reverse=True)
    return sorted_list


def top_3_averages(sorted_averages):
    for i in range(min(3, len(sorted_averages))):
        average, student = sorted_averages[i]
        print(f"Top #{i + 1}: {student['Full_name']} - Average: {average:.2f}")


def general_average(students):
    total = 0
    for student in students:
        avg = (
            student["Spanish_grade"]
            + student["English_grade"]
            + student["Social_studies_grade"]
            + student["Science_grade"]
        ) / 4
        total += avg
    return total / len(students) if students else 0
