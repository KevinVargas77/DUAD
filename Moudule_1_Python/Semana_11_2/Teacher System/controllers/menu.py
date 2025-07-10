from controllers.data_export import export_sections_for_professor

def main_menu(professor):
    while True:
        print(f"\nWelcome, {professor.full_name}. Choose an option:")
        print("1. View your sections")
        print("2. View students in a section")
        print("3. Edit grades")
        print("4. View global average")
        print("5. View global Top 3")
        print("6. Export data")
        print("7. Exit")

        choice = input("Select option: ")

        if choice == "1":
            print("\nSections:")
            for section in professor.sections:
                print(f"- {section.name}")

        elif choice == "2":
            sec_name = input("Enter section name: ").strip()
            section = next((s for s in professor.sections if s.name == sec_name), None)
            if section:
                for student in section.students:
                    print(f"{student.full_name} - Avg: {student.average():.2f}")
            else:
                print("Section not found.")

        elif choice == "3":
            sec_name = input("Enter section name to edit: ").strip()
            section = next((s for s in professor.sections if s.name == sec_name), None)
            if section:
                for student in section.students:
                    print(f"\n{student.full_name}:")
                    for subj in student.subjects:
                        try:
                            new = input(f"{subj.name} (current: {subj.grade}) → New grade or ENTER to skip: ")
                            if new.strip() != "":
                                subj.grade = int(new)
                        except ValueError:
                            print("Invalid input, grade not changed.")
                print("Grades updated.")
            else:
                print("Section not found.")

        elif choice == "4":
            total = 0
            count = 0
            for section in professor.sections:
                for student in section.students:
                    total += student.average()
                    count += 1
            avg = total / count if count else 0
            print(f"Global average of all students: {avg:.2f}")

        elif choice == "5":
            all_students = []
            for section in professor.sections:
                all_students.extend(section.students)

            sorted_students = sorted(all_students, key=lambda s: s.average(), reverse=True)
            print("\nGlobal Top 3 students:")
            for i, student in enumerate(sorted_students[:3], 1):
                print(f"Top #{i}: {student.full_name} - Avg: {student.average():.2f}")

        elif choice == "6":
            export_sections_for_professor(professor)
        
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
