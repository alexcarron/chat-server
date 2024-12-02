import requests

BASE_URL = "http://localhost:5000/"

def send_request(
	test,
	method,
	endpoint,
	body=None,
	headers=None,
	expected_code=200
):
	"""
	Sends an HTTP request (GET, POST, PUT, DELETE) to the given endpoint, tests that the response status code matches the expected status code, and retrieves the JSON body of the response.

	Parameters:
		test (unittest.TestCase): The test case to use for assertions.
		method (callable): The HTTP method function to use (e.g., requests.get, requests.post).
		endpoint (str): The endpoint to send the request to. Should not include the base URL. (e.g., "users/1", "messages")
		params (dict, optional): The data to send with the request. Defaults to None.
		headers (dict, optional): The headers to send with the request. Defaults to None.
		expected_code (int, optional): The expected response status code. Defaults to 200.

	Returns:
		dict: The JSON body of the response.
	"""
	body = body or {}
	headers = headers or {}

	url = BASE_URL + endpoint

	try:
		response = method(url, json=body, headers=headers)
		if test is not None:
			message = ""

			try:
				message = response.json()["message"]
			except Exception:
				pass
			
			test.assertEqual(
				expected_code,
				response.status_code,
				f'Response code to {endpoint} is {response.status_code}, not {expected_code}: {message}'
			)
		return response.json()
	except requests.exceptions.RequestException as error:
		test.fail(f"Request to {endpoint} failed with exception: {str(error)}")
	except ValueError as error:
		test.fail(f"Response from {endpoint} is not valid JSON: {str(error)}")

def send_get_request(
	test,
	endpoint,
	body=None,
	headers=None,
	expected_code=200
):
	"""
	Sends an HTTP GET request to the given endpoint, tests that the response status code matches the expected status code, and retrieves the JSON body of the response.

	Parameters:
		test (unittest.TestCase): The test case to use for assertions.
		endpoint (str): The endpoint to send the GET request to. Should not include the base URL. (e.g., "users/1", "messages")
		params (dict, optional): The data to send with the GET request. Defaults to None.
		headers (dict, optional): The headers to send with the GET request. Defaults to None.
		expected_code (int, optional): The expected response status code. Defaults to 200.

	Returns:
		dict: The JSON body of the response.
	"""
	return send_request(
		test,
		requests.get,
		endpoint,
		body=body,
		headers=headers,
		expected_code=expected_code
	)

def send_post_request(
	test,
	endpoint,
	body=None,
	headers=None,
	expected_code=200
):
	"""
	Sends an HTTP POST request to the given endpoint, tests that the response status code matches the expected status code, and retrieves the JSON body of the response.

	Parameters:
		test (unittest.TestCase): The test case to use for assertions.
		endpoint (str): The endpoint to send the POST request to. Should not include the base URL. (e.g., "users/1", "messages")
		params (dict, optional): The data to send with the POST request. Defaults to None.
		headers (dict, optional): The headers to send with the POST request. Defaults to None.
		expected_code (int, optional): The expected response status code. Defaults to 200.

	Returns:
		dict: The JSON body of the response.
	"""
	return send_request(
		test,
		requests.post,
		endpoint,
		body=body,
		headers=headers,
		expected_code=expected_code
	)

def send_put_request(
	test,
	endpoint,
	body=None,
	headers=None,
	expected_code=200
):
	"""
	Sends an HTTP PUT request to the given endpoint, tests that the response status code matches the expected status code, and retrieves the JSON body of the response.

	Parameters:
		test (unittest.TestCase): The test case to use for assertions.
		endpoint (str): The endpoint to send the PUT request to. Should not include the base URL. (e.g., "users/1", "messages")
		params (dict, optional): The data to send with the PUT request. Defaults to None.
		headers (dict, optional): The headers to send with the PUT request. Defaults to None.
		expected_code (int, optional): The expected response status code. Defaults to 200.

	Returns:
		dict: The JSON body of the response.
	"""
	return send_request(
		test,
		requests.put,
		endpoint,
		body=body,
		headers=headers,
		expected_code=expected_code
	)

def send_delete_request(
	test,
	endpoint,
	headers=None,
	expected_code=200
):
	"""
	Sends an HTTP DELETE request to the given endpoint, tests that the response status code matches the expected status code, and retrieves the JSON body of the response.

	Parameters:
		test (unittest.TestCase): The test case to use for assertions.
		endpoint (str): The endpoint to send the DELETE request to. Should not include the base URL. (e.g., "users/1", "messages")
		headers (dict, optional): The headers to send with the DELETE request. Defaults to None.
		expected_code (int, optional): The expected response status code. Defaults to 200.

	Returns:
		dict: The JSON body of the response.
	"""
	return send_request(
		test,
		requests.delete,
		endpoint,
		headers=headers,
		expected_code=expected_code
	)
