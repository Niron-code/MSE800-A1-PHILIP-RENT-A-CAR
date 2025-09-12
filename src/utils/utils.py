
class Utils:
	@staticmethod
	def is_valid_password(password: str) -> bool:
		"""
		Validates a password based on the following rules:
		1. At least 8 characters long
		2. Contains both alphanumeric characters and symbols
		3. No single character repeats consecutively
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

