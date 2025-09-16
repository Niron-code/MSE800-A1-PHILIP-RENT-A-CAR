# Philip Rent-A-Car

A user-friendly car rental management system for Windows, supporting both admin and customer roles. Easily manage cars, bookings, and users with a simple menu-driven interface.

## Features
- **English & Māori Language Support**: All menus, prompts, and email notifications are available in both English and Māori. Users select their preferred language at startup.
**Admin & Customer Roles**: Secure login and registration for both admins and customers.
**Car Management**: Add, update, delete, and view cars (admin only).
**Rental Booking**: Customers can book, view, update, and cancel rentals.
**Approval Workflow**: Admins approve or reject rental requests.
**Password Management**: Secure password validation and change options.
**Email Notifications**: Receive booking updates via email.
**Clear UI**: Consistent, easy-to-navigate menus with screen clearing for a clean experience.

## Project Structure

**main.py**: Entry point. Contains `PhilipRentACarApp` (singleton) to initialize DB and launch the main menu.

**Controllers**
- `car_controller.py`: `CarController` – Car management (add, view, update, delete).
- `rental_controller.py`: `RentalController` – Rental operations (booking, approval, update, cancel), email notifications.
- `user_controller.py`: `UserController` – User authentication, registration, login, password changes, menu navigation.

**Data Access Objects (DAO)**
- `car_dao.py`: `CarDAO` – CRUD for car records.
- `rental_dao.py`: `RentalDAO` – CRUD and business logic for rentals.
- `user_dao.py`: `UserDAO` – CRUD and authentication for users.

**Models**
- `car.py`: `Car` (abstract), `LuxuryCar`, etc. – Car model hierarchy and factory.
- `rental.py`: `Rental` – Rental transaction model.
- `user.py`: `User`, `AdminUser`, `CustomerUser`, `UserFactory` – User model hierarchy.

**Services**
- `car_service.py`: Business logic for car management.
- `rental_service.py`: Business logic for rental management.
- `user_service.py`: Business logic for user management.
- `email_service.py`: `EmailService` – Email notifications (approval/rejection), i18n support.

**Utilities**
- `utils.py`: `Utils` – Validation, date checks, screen clearing, i18n text loading.

**Internationalization**
- `i18n/texts_en.json`: English UI texts and email templates.
- `i18n/texts_maori.json`: Māori UI texts and email templates.

## Getting Started

### Requirements
- Windows 10/11
- Python 3.13+ (for source run) or use the provided `.exe` (no Python needed)

### Running the Executable
1. Download `PhilipRentACar.exe` from the latest release.
2. Double-click `PhilipRentACar.exe` to start the application.

### Running from Source
1. Clone this repository:
   ```
   git clone https://github.com/Niron-code/MSE800-A1-PHILIP-RENT-A-CAR
   cd yourrepo
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python src/main.py
   ```

## Usage
- **Admin Login**: Use the menu to log in as admin and manage cars or approve rentals.
- **Customer Registration/Login**: Register as a new customer or log in to book cars.
- **Menu Navigation**: Use the numbered options to navigate. Enter `0` to exit or go back as prompted.

## Versioning
- Stable releases are tagged (e.g., `v1.0.0`).
- See the [Releases](https://github.com/Niron-code/MSE800-A1-PHILIP-RENT-A-CAR/releases) page for changelogs and downloads.

## Changelog

### v1.1.0 (September 2025)
- **Māori Language Support**: The entire application now supports both English and Māori. All menus, prompts, and email notifications are fully internationalized. Users can select their preferred language at startup.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.

---

**Philip Rent-A-Car** – Simple, stable, and ready for your rental business!
