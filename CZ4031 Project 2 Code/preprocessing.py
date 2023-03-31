"""
Contains code for preprocessing user inputs and data used in algorithm
"""

import json
import psycopg2

class Preprocessing:    
    def __init__(self):
        print("INITIALIZING PREPROCESSING CLASS")
        self.db = DBConnection()
        print("THIS IS THE DB OBJECT: ", self.db.execute(query="select * from customer C, orders O where C.c_custkey = O.o_custkey"))

class DBConnection:
    def __init__(self, db_config_path: str = 'config.json'):
        import os
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

    def execute(self, query):
        try:
            # It is read from bottom to top
            # where the bottommost node represents the initial data source(s) 
            # and the topmost node represents the final output of the query.
            explain_query = "EXPLAIN " + query
            self.cur.execute(explain_query)
            query_plan = self.cur.fetchall()
            print("Query Plan Returned:", query_plan)
            # If adding results to the app
            # self.cur.execute(query)
            # query_results = self.cur.fetchall()
            # return query_results
            return
        except Exception as e:
            pass
        
