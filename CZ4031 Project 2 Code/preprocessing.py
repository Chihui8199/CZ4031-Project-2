"""
Contains code for preprocessing user inputs and data used in algorithm
"""

import json
import psycopg2
import os
from graphviz import Digraph

class GraphGenerator():
    def __init__(self, qep_json):
        self.qep = qep_json
        self.graph = Digraph()

    def build_dot(self, qep, parent=None, seq=1):
        node_id = str(hash(str(qep)))
        label = qep['Node Type']
        if 'Relation Name' in qep:
            label += f"\nRelation Name: {qep['Relation Name']}"
        self.graph.node(node_id, label)
        if parent is not None:
            self.graph.edge(parent, node_id)
        if 'Plans' in qep:
            for i, plan in enumerate(qep['Plans']):
                self.build_dot(plan, node_id, i+1)

    def generate_graph(self, format='png', view=True):
        self.build_dot(self.qep)
        self.graph.render('qep_graph', format=format, view=view)

class Preprocessing:
    def __init__(self):
        self.db = DBConnection()

    def get_query_plan(self, sql_query):
        """ Generate QEP of an SQL Query """
        result = self.db.execute("EXPLAIN (FORMAT JSON) "+sql_query)
        return result[0][0][0]["Plan"]


class DBConnection:
    def __init__(self, db_config_path: str = 'config.json'):
       
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
            self.cur.execute(query)
            query_results = self.cur.fetchall()
            return query_results
        except Exception as e:
            pass
