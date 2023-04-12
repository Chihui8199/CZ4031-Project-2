"""
Contains code for preprocessing user inputs and data used in algorithm
"""

import json
import psycopg2
import os
from functools import wraps
from graphviz import Digraph
from mo_sql_parsing import parse
from pprint import pprint
from deepdiff import DeepDiff

class Annotation():
    def __init__(self, qep_json):
        self.qep = qep_json
        #Pre-defining the graph and node's visualization attributes
        graph_attribute = {'bgcolor': 'white'}
        node_attribute = {'style': 'filled', 'color': 'black', 'fillcolor': 'lightblue'}
        self.graph = Digraph(graph_attr=graph_attribute, node_attr=node_attribute)
        
    
    def build_dot(self, qep, parent=None, seq=1):
        node_id = str(hash(str(qep)))
        label = f"{qep['Node Type']} (Cost: {qep['Total Cost']:.2f})"
        if 'Relation Name' in qep:
            label += f"\nRelation Name: {qep['Relation Name']}"
        shape = 'box' 
        self.graph.node(node_id, label, shape=shape)
        if parent is not None:
            self.graph.edge(parent, node_id)
        if 'Plans' in qep:
            for i, plan in enumerate(qep['Plans']):
                self.build_dot(plan, node_id, i+1)

    def generate_graph(self, query_plan, format='png', view=True):
        self.build_dot(self.qep)
        self.graph.attr('node', shape='box')  # set the shape of the nodes
        self.graph.render(query_plan, format=format, view=False)
    

class Preprocessing:
    def __init__(self,configList):
        self.db = DBConnection(configList)

    def get_query_results(self, sql_query):
        output = self.validate_query(sql_query) 
        query_res, column_names = self.db.execute(sql_query)
        # print(query_res)
        return query_res, column_names
    
    
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
        print("ENTERING GET QUERY PLAN")
        is_query_valid = self.validate_query(sql_query) 
        print("QUERY VALIDATION: ", is_query_valid)
        query_plan_res = self.db.execute("EXPLAIN (FORMAT JSON) " + sql_query)
        # print(query_plan_res[0][0][0])
        
        #output = self.validate(sql_query) 
        #query_plan_res,b = self.db.execute("EXPLAIN (FORMAT JSON) " + sql_query)
        
        try:
            print("_3242354346757",query_plan_res[0][0][0][0]['Plan'])
            query_plan_res = query_plan_res[0][0][0][0]['Plan']
            
            
        except Exception as e:
            query_plan_res = {}
            pass
        print(query_plan_res)
        return query_plan_res

    def validate_query(self, query):
        """
        Checks if the given query string is valid.
        Returns:
            dict: A dictionary with the following keys:
                - error (bool): Indicates if an error occurred during validation.
                - error_message (str): The error message if an error occurred,
                otherwise an empty string.
        """
        result = {"error": False, "error_message": ""}
        # checks if there's a query to execute
        if not len(query):
            result["error_message"] = "There is no query to execute."
            result["error"] = True
            return result
        # if query exists check that the query is a valid query
        if not self.db.is_query_valid(query):
            result["error_message"] = "The query cannot be executed and is invalid"
            result["error"] = True
            return result
            
        return result

class DBConnection:
    def __init__(self, configList):
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
       
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # db_config_path = os.path.join(dir_path, "config.json")

        # with open(db_config_path, "r") as file:
        #     config_dict = json.load(file)
        # try:
        print("AHHHHHHHHH",configList)
        self.host = configList[0]
        self.port = configList[1]
        self.database = configList[2]
        self.user = configList[3]
        self.password = configList[4]
        self.conn = psycopg2.connect(host=self.host, port=self.port,database=self.database,user=self.user, password=self.password)
        self.cur = self.conn.cursor()
        # except Exception as e:
        #     print("err")
        #     # print("hello", self.conn)
        #     # print(self.cur)
        #     print("Database Connection failed!")

    def execute(self, query: str):
        """Executes a query on the database and returns the results.
        Args:
        """
        try:
            self.cur.execute(query)
            column_names = [description[0] for description in self.cur.description]
            print(column_names)
            query_results = self.cur.fetchall()
            return query_results, column_names
        except Exception as e:
            pass

    def is_query_valid(self, query: str):    
        """Fetches a single row from the database to check if the query is valid.
        Args:
            query (str): Query string that was entered by the user.
        Returns:
            boolean: true if query is valid, false otherwise.
        """
        try:
            self.cur.execute(query)
            self.cur.fetchone()
        except Exception as e:
            print ("Exception: is_query_valid:", e)
            return False
        return True

class CalculateCost:
    def __init__(self):
        print("Calculating cost------------")

        # Calculate total cost of all nodes in plan
    def calculateCost(self, plan):
        totalCost = 0
        for i in range(len(plan)):     
            initialKey = list(plan.keys())[i]
            initialValue = plan[initialKey]
            if initialKey == 'Total Cost':
                totalCost += initialValue
        return totalCost
            
    # Print cost comparison in readable format
    def printCost(self,initialPlan,newPlan):
        total_initial_cost = self.calculateCost(initialPlan)
        total_new_cost = self.calculateCost(newPlan)
        if total_new_cost < total_initial_cost:
            total_initial_cost_string = f"The total cost has reduced from {total_initial_cost} in the initial plan to {total_new_cost} in the new plan. This means that the overall cost of executing the query is lower in the new plan, which should result in faster execution times.\n"
            return str(total_initial_cost_string)
        
        else:
            total_initial_cost_string = f"The total cost has increased from {total_initial_cost} in the initial plan to {total_new_cost} in the new plan. This means that the overall cost of executing the query is higher in the new plan, which should result in slower execution times.\n"
            return str(total_initial_cost_string)

    
class Comparison:
    def __init__(self):
        print("Looking for difference------------")
    
    def comparing(self,sql_query1, sql_query2):
        
        parsed_query1 = parse(sql_query1)
        parsed_query2 = parse(sql_query2)
        ddiff = DeepDiff(parsed_query1, parsed_query2)
        difference = self.comparing_changes(ddiff, sql_query1,sql_query2,parsed_query1, parsed_query2)
        print("\n\n\n\n",difference,"\n\n\n\n")
        return difference
    
    # single dict object of token
    def token_parser(self,dict_tokens):
        lhs = ''
        rhs = ''
        operator = ''
        operator_types = {'eq': '=', 'lt': '<', 'gt': '>', 'ne': '!='}
        for key, value in dict_tokens.items():
            if key in operator_types:
                operator = operator_types.get(key)
            lhs = value[0]
            rhsDict = value[1]
            if isinstance(rhsDict, (int, float)):
                rhs = rhsDict
            else: 
                for key, value in rhsDict.items():
                    if key == 'literal':
                        rhs =  rhsDict[key]
        results = lhs + " " + operator + " " + rhs
        return results

    def cleaning_literal(self,value):
        right_value = value[1]['literal'] if 'literal' in value[1] else value[1].split('.')[-1]
        return value[0].split('.')[-1], right_value

    def convert_to_and_of_or_with_and_of(self,clause):
        and_clause = self.convert_and_clause(clause['and']) if 'and' in clause else ''
        or_clause = self.convert_or_clause(clause['or']) if 'or' in clause else ''

        if and_clause and or_clause:
            return f"({and_clause}) OR ({or_clause})"
        elif or_clause:
            return f"({or_clause})"
        else:
            return and_clause

    def convert_or_clause(self,or_clause):
        or_parts = []
        for or_cond in or_clause:
            if 'and' in or_cond:
                and_parts = []
                for and_cond in or_cond['and']:
                    and_parts.append(self.convert_and_condition(and_cond))
                or_parts.append(f"({' AND '.join(and_parts)})")
            else:
                or_parts.append(self.convert_and_condition(or_cond))
        return " OR ".join(or_parts)

    def convert_and_clause(self,and_clause):
        and_parts = []
        for and_cond in and_clause:
            and_parts.append(self.convert_and_condition(and_cond))
        return " AND ".join(and_parts)

    def convert_and_condition(self,and_cond):
        conditions = []
        for operator, operands in and_cond.items():
            left, right = map(lambda x: x.split('.')[-1] if isinstance(x, str) else x['literal'], operands)
            cleaned_right = self.cleaning_literal((left, right))[1]
            if operator == 'eq':
                conditions.append(f"{left} = {cleaned_right}")
            elif operator == 'lt':
                conditions.append(f"{left} < {cleaned_right}")
            elif operator == 'gt':
                conditions.append(f"{left} > {cleaned_right}")
            elif operator == 'le':
                conditions.append(f"{left} <= {cleaned_right}")
            elif operator == 'ge':
                conditions.append(f"{left} >= {cleaned_right}")
            elif operator == 'ne':
                conditions.append(f"{left} != {cleaned_right}")
        return ' AND '.join(conditions)
    
    def find_token_changed(self, ddiff_obj):
        results = set()
        string_ddiff  = str(ddiff_obj).lower()
        if "from" in string_ddiff.lower():
            results.add("from")
        if "where" in string_ddiff.lower():
            results.add("where")
        if "select" in string_ddiff.lower():
            results.add("select")
        if "group by" in string_ddiff.lower():
            results.add("group by")
        if "limit" in string_ddiff.lower():
            results.add("limit")
        if(len(results)>0):
            joined_string = ", ".join(results)
            return ("The tokens that are changed are in the "+ joined_string + " clause")
        else:
            return ("No clause are changed")


    def comparing_changes(self,ddiff, sql_query1, sql_query2,parsed_query1,parsed_query2):
        diffString=''
        try:
            #If no changes
            token_changed_string = self.find_token_changed(ddiff)
            if ddiff  == {}:
                print("No changes were made in Query 2")
                return None
            elif (('select' or 'from') in str(ddiff)):
                diffString += token_changed_string
            else:
                if 'values_changed' in ddiff:
                    for key, value in ddiff['values_changed'].items():
                        if key.startswith("root[") and key.endswith("]['literal']"):
                            element_parts = []
                            for part in key.split("[")[1:]:
                                index = part.split("]")[0]
                                try:
                                    index = int(index)
                                    element_parts.append(index)
                                except ValueError:
                                    element_parts.append(index.strip("'"))
                            element = sql_query1
                            
                            for part in element_parts:
                                print(part)
                                if isinstance(element, list):
                                    element = element[part]
                                elif isinstance(element, dict):
                                    element = element.get(part)
                                else:
                                    break
                        
                            if isinstance(element, dict):
                                element = element.get('literal')
                            if isinstance(element, str):
                                try:
                                    conditions = [c.strip() for c in element.split('where')[1].split('and')]
                                except:
                                    conditions = [c.strip() for c in element.split('WHERE')[1].split('and')]
                            else:
                                conditions = element
                                
                            if 'new_value' in value and 'old_value' in value:
                                old_value = value['old_value']
                                new_value = value['new_value']
                                for cond in conditions:
                                    if f"'{old_value}'" in cond and f"'{new_value}'" not in cond:
                                        column = cond.split()[0]
                                        diffString += "\nThe " + column + "changed from " + old_value + " to " + new_value
                                        print(diffString)
                        else:
                            print(f"Unexpected key format: {key}")

                if 'iterable_item_added' in ddiff:
                    iterable_values = ddiff['iterable_item_added']
                    for key, value in iterable_values.items():
                        results = self.token_parser(value)
                        diffString += "\nThere is a new statement added in the where clause" + results

                if 'iterable_item_removed' in ddiff:
                    iterable_values = ddiff['iterable_item_removed']
                    for key, value in iterable_values.items():
                        results = self.token_parser(value)
                        diffString += "\nThere is a statement removed in the where" + results

                where_clause1 = parsed_query1['where']
                where_clause2 = parsed_query2['where']
                AddToOne = False
                if len(str(where_clause1)) < len(str(where_clause2)):
                    AddToOne = True

                #Q1-> Q2 has an addition of dictionary item
                if ('dictionary_item_added' in ddiff and AddToOne == True):
                    where_clause1 = parsed_query1['where']
                    where_clause2 = parsed_query2['where']
                    
                    converted_clause1 = self.convert_to_and_of_or_with_and_of(where_clause1)
                    converted_clause2 = self.convert_to_and_of_or_with_and_of(where_clause2)

                    added_item = ddiff['dictionary_item_added'][0] # get the first dictionary in the list
                    
                    key_parts = added_item.split('[')  # split the string at '[' characters
                    key_parts = [part.strip('"]') for part in key_parts]  # remove leading/trailing '"' characters
                    where_op = key_parts[-1]  # get the last element of the list, which should be the oper

                    diffString += "\nAddition of " + where_op + " condition to query 2\nQuery 1: " + \
                                str(converted_clause1) + "\nQuery 2:" + str(converted_clause2)

                #Q1-> Q2 has a dictionary item removed
                elif  ('dictionary_item_removed' in ddiff and AddToOne==False):
                    where_clause1 = parsed_query1['where']
                    where_clause2 = parsed_query2['where']
                    removed_item = ddiff['dictionary_item_removed'][0] # get the first dictionary in the list
                    
                    key_parts = removed_item.split('[')  # split the string at '[' characters
                    key_parts = [part.strip('"]') for part in key_parts]  # remove leading/trailing '"' characters
                    where_op = key_parts[-1]  # get the last element of the list, which should be the oper

                    converted_clause1 = self.convert_to_and_of_or_with_and_of(where_clause1)
                    converted_clause2 = self.convert_to_and_of_or_with_and_of(where_clause2)

                    diffString += "\nRemoved " + where_op + " condition to query 2\nQuery 1: " + \
                                str(converted_clause1) + "\nQuery 2:" + str(converted_clause2)

        except Exception as e:
            print(e,"error5 *")
            diffString = self.find_token_changed(ddiff)

        return diffString 

        