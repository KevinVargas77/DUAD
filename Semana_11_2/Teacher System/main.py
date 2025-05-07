from controllers.menu import main_menu
from controllers.data_entry import login_professor

def main():
    print("🎓 Welcome to the Grade Management System\n")
    professor = login_professor()

    if professor:
        main_menu(professor)
    else:
        print("Login failed. Exiting program.")

if __name__ == "__main__":
    main()
