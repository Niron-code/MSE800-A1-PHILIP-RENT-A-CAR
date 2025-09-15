"""
main.py

Entry point for the car rental system application.
Defines the PhilipRentACarApp singleton class and launches the main user interface menu.
Implements the Singleton pattern to ensure only one app instance exists.
Implements a lock file to prevent multiple simultaneous runs of the application.
"""
from controllers.user_controller import UserController
from database import Database


class PhilipRentACarApp:
    """
    Main application class for the Philip Rent A Car system.
    Handles database initialization and launches the main user interface menu.
    """
    def __init__(self):
        """
        Initializes the application and database.
        """
        Database.init_db()

    def run(self):
        """
        Starts the main user interface menu for the car rental system.
        This is the main entry point for user interaction.
        """
        UserController.user_main_menu()

if __name__ == "__main__":
    """
    Main entry point for the Philip Rent A Car application.
    Creates and runs the singleton application instance.
    """
    app = PhilipRentACarApp()
    app.run()

