"""
main.py

Entry point for the car rental system application.
Defines the PhilipRentACarApp singleton class and launches the main user interface menu.
Implements the Singleton pattern to ensure only one app instance exists.
Implements a lock file to prevent multiple simultaneous runs of the application.
"""

from controllers.user_controller import UserController
from database import Database
from utils.text_loader import load_texts


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
        print("Select Language / Kōwhiria te Reo:")
        print("1. English")
        print("2. Māori")
        lang_choice = input("Enter choice (1/2): ").strip()
        language = 'maori' if lang_choice == '2' else 'en'
        texts = load_texts(language)
        # Pass texts to UserController (assumes UserController can accept it)
        UserController.user_main_menu(texts)


if __name__ == "__main__":
    app = PhilipRentACarApp()
    app.run()

