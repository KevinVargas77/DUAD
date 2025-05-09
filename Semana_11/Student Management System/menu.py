"""menu: will contain all the logic related to the menu options."""

from controllers import data_entry, data_views, data_exp_imp
from models.subject import Subject
from models.student import Student
from exercises.exercises_runner import run_ex_1_2, run_ex_4_human


"""menu: will contain all the logic related to the menu options."""

def show_menu():
    students = []  

    while True:
        print("\n=== MENU ===")
        print("1. Add Students")
        print("2. View All Students")
        print("3. View Top 3 Students")
        print("4. View Overall Average")
        print("5. Export to CSV")
        print("6. Import from CSV")
        print("7. Run Exercises 1–2 (Circle & Bus)")
        print("8. Run Exercise 4 (Human)")
        print("9. Exit")

        choice = input("Option: ")

        if choice == "1":
            students = data_entry.students_entry()
        elif choice == "2":
            if not students:
                print("No students available. Please add or import first.")
            else:
                data_views.all_students(students)
        elif choice == "3":
            if not students:
                print("No students available. Please add or import first.")
            else:
                data_views.top_3_averages(students)
        elif choice == "4":
            if not students:
                print("No students available.")
            else:
                avg = data_views.general_average(students)
                print(f"General average of all students: {avg:.2f}")
        elif choice == "5":
            if not students:
                print("No data to export.")
            else:
                data_exp_imp.export_to_csv(students)
        elif choice == "6":
            students = data_exp_imp.import_from_csv()
        elif choice == "7":
            run_ex_1_2()
        elif choice == "8":
            run_ex_4_human()
        elif choice == "9":
            print("Exiting.")
            break
        else:
            print("Invalid option.")
