
"""data: will contain all the logic for exporting and importing data."""

import csv
import os
from models.student import Student
from models.subject import Subject

def import_from_csv(filename="data/students.csv"):
    if not os.path.exists(filename):
        print("No exported file found. Please enter the data first.")
        return []

    students = []
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            subjects = [
                Subject("Spanish", int(row["Spanish_grade"])),
                Subject("English", int(row["English_grade"])),
                Subject("Social_studies", int(row["Social_studies_grade"])),
                Subject("Science", int(row["Science_grade"]))
            ]
            student = Student(row["Full_name"], row["Section"], subjects)
            students.append(student)
    print("Students imported successfully.")
    return students


def export_to_csv(students, filename="data/students.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Full_name", "Section", "Spanish_grade", "English_grade", "Social_studies_grade", "Science_grade"
        ])
        writer.writeheader()
        for student in students:
            writer.writerow(student.to_dict())
    print("Students exported to CSV successfully.")
