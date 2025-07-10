import os
import csv
from models.student import Student
from models.subject import Subject
from models.section import Section

def export_sections_for_professor(professor, folder_path="data"):
    os.makedirs(folder_path, exist_ok=True)

    for section in professor.sections:
        filename = f"{professor.id}_{section.name}.csv"
        filepath = os.path.join(folder_path, filename)

        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "Full_name", "Section", "Spanish", "English", "Science", "Social"
            ])
            writer.writeheader()

            for student in section.students:
                row = {
                    "Full_name": student.full_name,
                    "Section": student.section,
                    "Spanish": next(s.grade for s in student.subjects if s.name == "Spanish"),
                    "English": next(s.grade for s in student.subjects if s.name == "English"),
                    "Science": next(s.grade for s in student.subjects if s.name == "Science"),
                    "Social": next(s.grade for s in student.subjects if s.name == "Social")
                }
                writer.writerow(row)

    print("Sections exported correctly.")
