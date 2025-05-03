"""menu: will contain all the logic related to the menu options."""

import data_entry, data_views, data_exp_imp

students = []


def show_menu():
    global students
    while True:
        print("\n=== MENU ===")
        print("1. Add Students")
        print("2. View All Students")
        print("3. View Top 3 Students")
        print("4. View Overall Average")
        print("5. Export to CSV")
        print("6. Import from CSV")
        print("7. Exit")


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
                sorted_list = data_views.sorted_averages(students)
                data_views.top_3_averages(sorted_list)
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
            print("Exiting.")
            break
        else:
            print("Invalid option.")
