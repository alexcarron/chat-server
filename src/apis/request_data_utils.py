from flask_restful import request

def get_json_body():
	"""
	Retrieves the JSON data from the body of the current request as a dictionary.

	Returns:
		dict: The JSON data from the body of the current request.
	"""
	return request.get_json()

def get_json_body_property(property_name):
	"""
	Retrieves a specific property from the JSON data in the request body.

	Parameters:
		property_name (str): The name of the property to retrieve from the JSON data.

	Returns:
		The value of the specified property from the JSON data in the request body. None if the property does not exist.
	"""
	return get_json_body().get(property_name)

def get_query_args_dict():
	"""
	Retrieves the query arguments as a dictionary from the current request.

	Returns:
		dict: A dictionary containing the query arguments from the current request.
	"""
	return request.args.to_dict()

def get_query_value(query_arg_name):
	"""
	Retrieves the value of a specific query argument from the current request.

	Parameters:
		query_arg_name (str): The name of the query argument to retrieve.

	Returns:
		str: The value of the specified query argument, or `None` if the argument is not present in the request.
	"""
	return request.args.get(query_arg_name)