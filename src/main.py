"""
main.py

Entry point for the car rental system application.
Initializes the database and launches the main user interface menu.
"""


from controllers.user_controller import UserController
from database import Database

class PhilipRentACarApp:
    """
    Main application class for Philip Rent A Car system.
    Handles initialization and launching the main menu.
    """
    def __init__(self):
        # Initialize the database
        Database.init_db()

    def run(self):
        """
        Starts the main user interface menu for the car rental system.
        """
        UserController.user_main_menu()

if __name__ == "__main__":
    app = PhilipRentACarApp()
    app.run()
