"""
utils.py

Utility module for the car rental system.
Provides static methods for input validation (password, email) and date checks (start/end dates).
"""

import datetime
import re


class Utils:
	"""
	Utility class providing static methods for validation and other common tasks in the car rental system.

	Includes:
	- Password and email validation
	- Date checks for rental periods
	- clear_screen(): the standard method for clearing the terminal screen before displaying menus or after logout, ensuring a consistent UI experience. Use Utils.clear_screen() instead of direct os.system calls throughout the application.
	"""
	
	@staticmethod
	def is_valid_password(password: str) -> bool:
		"""
		Validates a password based on the following rules:
		1. At least 8 characters long
		2. Contains both alphanumeric characters and symbols
		3. No single character repeats consecutively
		Returns True if valid, False otherwise.
		"""
		if len(password) < 8:
			return False
		has_alphanumeric = any(c.isalnum() for c in password)
		has_symbol = any(not c.isalnum() for c in password)
		if not (has_alphanumeric and has_symbol):
			return False
		for i in range(1, len(password)):
			if password[i] == password[i-1]:
				return False
		return True

	@staticmethod
	def is_valid_email(email: str) -> bool:
		"""
		Validates an email address using regex pattern.
		Returns True if valid, False otherwise.
		"""
		pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
		return re.match(pattern, email) is not None

	@staticmethod
	def is_start_date_today_or_future(start_date_str, date_format="%Y-%m-%d"):
		"""
		Returns True if the start_date_str is today or in the future, False otherwise.
		Expects start_date_str in 'YYYY-MM-DD' format by default.
		"""
		try:
			start_date = datetime.datetime.strptime(start_date_str, date_format).date()
			today = datetime.date.today()
			return start_date >= today
		except Exception:
			return False

	@staticmethod
	def is_end_date_valid(start_date_str, end_date_str, date_format="%Y-%m-%d"):
		"""
		Returns True if end_date_str is in the future and not before start_date_str.
		Expects date strings in 'YYYY-MM-DD' format by default.
		"""
		try:
			start_date = datetime.datetime.strptime(start_date_str, date_format).date()
			end_date = datetime.datetime.strptime(end_date_str, date_format).date()
			today = datetime.date.today()
			return end_date > today and end_date >= start_date
		except Exception:
			return False

	@staticmethod
	def clear_screen():
		"""
		Clears the terminal screen.

		This method should be used to refresh the terminal UI before displaying any main menu or after logging out,
		ensuring a clean and consistent user experience. It replaces all direct calls to os.system('cls'...) or os.system('clear')
		throughout the car rental system. Always call Utils.clear_screen() at the start of menu methods and on logout.
		"""
		import os
		os.system('cls' if os.name == 'nt' else 'clear')