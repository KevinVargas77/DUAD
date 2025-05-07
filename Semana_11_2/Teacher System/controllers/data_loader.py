import os
import csv
from models.student import Student
from models.subject import Subject
from models.section import Section

def read_csv(filename):
    students = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            subjects = [
                Subject("Spanish", int(row["Spanish"])),
                Subject("English", int(row["English"])),
                Subject("Science", int(row["Science"])),
                Subject("Social", int(row["Social"]))
            ]
            student = Student(
                full_name=row["Full_name"],
                section=row["Section"],
                subjects=subjects
            )
            students.append(student)
    return students


def load_sections_for_professor(professor_id, folder_path="data"):
    sections = []
    for file in os.listdir(folder_path):
        if file.startswith(professor_id) and file.endswith(".csv"):
            path = os.path.join(folder_path, file)
            students = read_csv(path)
            section_name = students[0].section if students else "??"
            section = Section(name=section_name, students=students)
            sections.append(section)
    return sections


def get_professor_name(professor_id, filename="professors.csv"):
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == professor_id:
                return row["Full_name"]
    return None


