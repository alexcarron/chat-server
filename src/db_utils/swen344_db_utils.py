# Utility file for interacting with the PostgreSQL database

import psycopg2
import psycopg2.extras
import psycopg2.sql
import yaml
import os

def connect():
	"""
	Connect to the PostgreSQL database using the configuration in `../config/db.yml`.

	Returns a connection object.
	"""
	config = {}
	yml_path = os.path.join(os.path.dirname(__file__), '../../config/db.yml')

	with open(yml_path, 'r') as file:
		config = yaml.load(file, Loader=yaml.FullLoader)

	return psycopg2.connect(
		dbname=config['database'],
		user=config['user'],
		password=config['password'],
		host=config['host'],
		port=config['port']
	)

def get_cursor(connection):
	"""
	Returns a cursor object for the given connection.
	"""
	dictionary_cursor_factory = psycopg2.extras.RealDictCursor
	return connection.cursor(cursor_factory=dictionary_cursor_factory)

def exec_sql_file(sql_file_path):
	"""
	Execute a SQL file specified by `sql_file_path` against the database.

	`sql_file_path` is the path to the SQL file, relative to the root of the project.
	"""
	current_dir = os.path.dirname(__file__)
	root_dir = os.path.join(current_dir, '..', 'sql_files')

	full_path = os.path.abspath(os.path.join(root_dir, sql_file_path))
	connection = connect()
	cursor = get_cursor(connection)

	with open(full_path , 'r') as file:
		cursor.execute(file.read())

	connection.commit()
	connection.close()

def exec_get_first_row(sql_query, args={}):
	"""
	Execute a SQL query against the database and return the first row.

	`args` is a tuple of arguments to pass to the query.

	Returns the first row of the query result as a tuple, or `None` if the query did not return any rows.
	"""
	connection = connect()
	cursor = get_cursor(connection)
	cursor.execute(sql_query, args)
	first_row = cursor.fetchone()
	connection.close()

	return first_row

def exec_get_first_value(sql_query, args={}):
	"""
	Execute a SQL query against the database and return the first value of the first row.

	`args` is a tuple of arguments to pass to the query.

	Returns the first value of the query result as a string, or `None` if the query did not return any rows.
	"""
	first_row = exec_get_first_row(sql_query, args)

	if first_row is None:
		return None

	first_row_values = list(first_row.values())

	return first_row_values[0]

def exec_get_all_rows(sql_query, args={}):
	"""
	Execute a SQL query against the database and return all rows.

	`args` is a tuple of arguments to pass to the query.

	Returns a list of all the rows of the query result as tuples, or an empty list if the query did not return any rows.
	"""
	connection = connect()
	cursor = get_cursor(connection)
	cursor.execute(sql_query, args)
	# https://www.psycopg.org/docs/cursor.html#cursor.fetchall

	list_of_all_rows = cursor.fetchall()
	connection.close()

	return list_of_all_rows

def exec_many(sql_query, args=[]):
	"""
	Executes a SQL query against the database for each tuple in `args` and commit the changes.

	`args` is a list of tuples of arguments to pass to the query.
	"""

	connection = connect()
	cursor = get_cursor(connection)
	cursor.executemany(sql_query, args)
	connection.commit()
	connection.close()

def exec_commit(sql_query, args={}):
	"""
	Executes a SQL query against the database and commit the changes.

	`args` is a tuple of arguments to pass to the query.
	"""

	connection = connect()
	cursor = get_cursor(connection)
	cursor.execute(sql_query, args)
	connection.commit()
	connection.close()

def exec_commit_return_value(sql_query, args={}):
	"""
	Executes a SQL query against the database, commits the changes, and returns the first value of the first row of the returned rows.

	`args` is a tuple of arguments to pass to the query.

	Returns the first value of the query result, or `None` if the query did not return any rows.
	"""
	first_row = exec_commit_return_row(sql_query, args)

	if not first_row:
		return None

	first_row_values = list(first_row.values())

	return first_row_values[0]

def exec_commit_return_row(sql_query, args={}):
	"""
	Executes a SQL query against the database, commits the changes, and returns the first row of the returned rows.

	`args` is a tuple of arguments to pass to the query.

	Returns the first row of the query result as a tuple, or `None` if the query did not return any rows.
	"""
	connection = connect()
	cursor = get_cursor(connection)
	cursor.execute(sql_query, args)
	result = cursor.fetchone()
	connection.commit()
	connection.close()
	return result