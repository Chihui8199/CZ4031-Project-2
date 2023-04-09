"""
Contains code for preprocessing user inputs and data used in algorithm
"""

import difflib
import json
import psycopg2
import os
from functools import wraps


class Preprocessing:
    def __init__(self):
        self.db = DBConnection()

    def get_query_results(self, sql_query):
        """
        Executes an SQL query and returns the query results.

        If the SQL query does not contain a `LIMIT` clause, the method automatically adds a `LIMIT 20` clause to the query to limit the number of returned rows to 20.
        Note that if the query returns a large number of rows, it may cause the application to crash due to memory constraints.
        
        Parameters:
            sql_query (str): The SQL query to execute.

        Returns:
            list: A list of rows returned by the SQL query. Each row is represented as a tuple of column values.

        Raises:
            ValueError: If the input query is empty.
        """

        # check if query has a limit clause
        if 'LIMIT' not in sql_query.upper():
            # if not, add a limit clause to limit to 20 results
            sql_query += ' LIMIT 20'
        output = self.validate(sql_query) 
        query_res = self.db.execute(sql_query)
        return query_res
    
    
    def get_query_plan(self, sql_query):
        """
        Generates a Query Execution Plan (QEP) for a given SQL query.

        Args:
            sql_query (str): The SQL query for which to generate a QEP.

        Returns:
            dict: A dictionary representation of the QEP generated by PostgreSQL.
                The dictionary is in JSON format and contains detailed information
                about the steps involved in executing the query.

        Raises:
            ValueError: If the provided SQL query is invalid.
        """
        # TODO: 
        # CALL on front end raise value error 
        
        output = self.validate(sql_query) 
        query_plan_res = self.db.execute("EXPLAIN (FORMAT JSON) " + sql_query)
        try:
            query_plan_res = query_plan_res[0][0][0]["Plan"]
        except Exception as e:
            query_plan_res = {}
            pass
        
        return query_plan_res

    def validate(self, query):
        """
        Checks if the given query string is valid.

        Args:
            query (str): The query string to be validated.

        Returns:
            dict: A dictionary with the following keys:
                - query (str): The original query string passed to the function.
                - error (bool): Indicates if an error occurred during validation.
                - error_message (str): The error message if an error occurred,
                otherwise an empty string.
        """
        output = {"query": query, "error": False, "error_message": ""}

        if not len(query):
            output["error"] = True
            output["error_message"] = "Query is empty."
            return output

        if not self.db.query_valid(query):
            print('Setting query output : invalid')
            output["error"] = True
            output["error_message"] = "Query is invalid."
            return output
            
        return output
    
    
class DBConnection:
    def __init__(self, db_config_path: str = 'config.json'):
        """Initializes a new instance of the 'Database' class
        
        The constructor reads the database connection details from the config.json file and establishes a connection to the PostgreSQL server

        Args:
        db_config_path (str, optional): The path to the configuration file containing
        the database connection details. If not provided,
            the default value is 'config.json'
        
        Raises:
            FileNotFoundException: If the config.json file is not found
            ValueError: If the config.json fi
        
        """
       
        dir_path = os.path.dirname(os.path.realpath(__file__))
        db_config_path = os.path.join(dir_path, "config.json")

        with open(db_config_path, "r") as file:
            config_dict = json.load(file)
        self.port = config_dict['port']
        self.database = config_dict['database']
        self.user = config_dict['user']
        self.host = config_dict['host']
        self.password = config_dict['password']
        self.conn = psycopg2.connect(host=self.host, port=self.port,database=self.database,user=self.user, password=self.password)
        self.cur = self.conn.cursor()

    def wrap_single_transaction(func):
        """Decorator to create cursor each time the function is called.

        Args:
            func (function): Function to be wrapped

        Returns:
            function: Wrapped function
        """
        @wraps(func)
        def inner_func(self, *args, **kwargs):
            try:
                self.cur = self.conn.cursor()
                ans = func(self, *args, **kwargs)
                self.conn.commit()
                return ans
            except Exception as error:
                print(f"Exception encountered, rolling back: {error}")
                self.conn.rollback()

        return inner_func
    
    @wrap_single_transaction
    def execute(self, query: str):
        """Executes a query on the database and returns the results.
        Args:
        """
        try:
            self.cur.execute(query)
            query_results = self.cur.fetchall()
            return query_results
        except Exception as e:
            pass

    @wrap_single_transaction
    def query_valid(self, query: str):    
        """Fetches a single row from the database to check if the query is valid.
        Args:
            query (str): Query string that was entered by the user.
        Returns:
            boolean: true if query is valid, false otherwise.
        """
        self.cur.execute(query)
        try:
            self.cur.fetchone()
        except Exception as e:
            print (e)
            return False
        return True
    
    import difflib

    