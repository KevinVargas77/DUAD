"""data: will contain all the logic for exporting and importing data."""

import csv
import os

def import_from_csv(filename="students.csv"):
    if not os.path.exists(filename):
        print("No exported file found. Please enter the data first.")
        return []

    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        students = []
        for row in reader:
            student = {
                "Full_name": row["Full_name"],
                "Section": row["Section"],
                "Spanish_grade": int(row["Spanish_grade"]),
                "English_grade": int(row["English_grade"]),
                "Social_studies_grade": int(row["Social_studies_grade"]),
                "Science_grade": int(row["Science_grade"])
            }
            students.append(student)
    print("✅ Students imported successfully.")
    return students


def export_to_csv(students, filename="students.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Full_name", "Section", "Spanish_grade", "English_grade", "Social_studies_grade", "Science_grade"
        ])
        writer.writeheader()
        writer.writerows(students)
    print("✅ Students exported to CSV successfully.")
