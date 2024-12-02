import hashlib

HASHING_ALGORITHM = hashlib.sha512
ENCODING_SCHEME = 'utf-8'

def hash_string(string):
	"""
	Hashes a string using SHA-512.

	Args:
		string (str): The string to hash.

	Returns:
		str: The hash value of the string as a hexadecimal string.
	"""
	hashing_algroithm = HASHING_ALGORITHM()
	string_as_bytes = string.encode(ENCODING_SCHEME)
	hashing_algroithm.update(string_as_bytes)
	hash_value = hashing_algroithm.hexdigest()
	return hash_value

def matches_hashed_value(input_string, expected_hash_value):
	"""
	Checks if the hash value of the input string matches the expected hash value.

	Args:
		input_string (str): The string to check.
		expected_hash_value (str): The expected hash value.

	Returns:
		bool: `True` if the hash value of the input string matches the expected hash value, `False` otherwise.
	"""
	input_hash_value = hash_string(input_string)
	does_match = input_hash_value == expected_hash_value
	return does_match
