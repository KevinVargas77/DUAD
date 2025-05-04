"""data_entry: will contain all the logic for the menu options regarding entry the students data"""

def ask_number_of_students():
    while True:
        try:
            total = int(input("Enter the total number of students you want to add: "))
            if total > 0:
                return total
            else:
                print("Number must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


def get_valid_grade(subject_name):
    while True:
        try:
            grade = int(input(f"{subject_name} grade (0–100): "))
            if 0 <= grade <= 100:
                return grade
            else:
                print("Grade must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")


def collect_student_info(index):
    print(f"\nPlease enter the information of student #{index}")

    while True:
        full_name = input("Full name: ").strip()
        if full_name.replace(" ", "").isalpha():
            break
        else:
            print("Name must contain only letters and spaces.")

    while True:
        section = input("Section (e.g., 11B): ")
        has_letter = any(char.isalpha() for char in section)
        has_digit = any(char.isdigit() for char in section)
        if has_letter and has_digit:
            break
        else:
            print("Section must contain both letters and numbers, like '11B'.")

    spanish = get_valid_grade("Spanish")
    english = get_valid_grade("English")
    social = get_valid_grade("Social studies")
    science = get_valid_grade("Science")

    return {
        "Full_name": full_name,
        "Section": section,
        "Spanish_grade": spanish,
        "English_grade": english,
        "Social_studies_grade": social,
        "Science_grade": science
    }


def students_entry():
    total = ask_number_of_students()
    students = []
    for i in range(1, total + 1):
        student = collect_student_info(i)
        students.append(student)
        print("Student added successfully!")
    return students
