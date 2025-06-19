from interfaces.interface_main import DashboardApp

if __name__ == "__main__":
    try:
        app = DashboardApp()
        app.run()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
