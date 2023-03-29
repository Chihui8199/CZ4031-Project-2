"""
Contains code for preprocessing user inputs and data used in algorithm
"""

import json
import psycopg2
class Preprocessing:    
    def __init__(self):
        print("INITIALIZING PREPROCESSING CLASS")
       
        self.db = DBConnection()

        print("THIS IS THE DB OBJECT: ", self.db.execute(query="select * from customer limit 1;"))

class DBConnection:
    def __init__(self, db_config_path: str = 'config.json'):
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
            self.cur.execute(query)
            query_results = self.cur.fetchall()
            return query_results
        except Exception as e:
            pass
