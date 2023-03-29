"""
Contains code for preprocessing user inputs and data used in algorithm
"""
from anytree import PreOrderIter
import interface

class Preprocessing:
    
    
    def __init__(self):
        print("Init preprocessing")


    def get_json(self, query_explain_result):
        """
        Get json of sql output
        
        Based on postgres return format
        """        
        json_portion = query_explain_result[0][0][0] 
        return json_portion


    def prepare_highlighting_sql_query_character_map(self, query):
        """
        Preprocess query to prepare for highlighting during annotation phase.

        Look into python tkinter text tagging for more information.       

        During tagging we need to specify the specific line number and character (column) 
        """
        index_map = {}
        line = 1
        column = 0
        index = 0
        while index <= len(query):
            index_map[index] = f'{line}.{column}'
            if index < len(query) and query[index] == '\n':
                line += 1
                column = 0
            else:
                column += 1
            index += 1
        return index_map;


    def get_planner_method_configuration_constraints(self, tree):
        """
        Iterate through the tree and get the constraints to apply
        """
        constraints = []

        for node in PreOrderIter(tree):
            # ID is node type
            if getattr(node, 'id') not in interface.KEY_PROPERTY:
                continue
            else:
                node_type = getattr(node, 'node_type').upper()
                if (node_type in interface.NODE_TYPES_CONSTRAINTS_MAPPING.keys()):
                    constraint = interface.NODE_TYPES_CONSTRAINTS_MAPPING[node_type]
                    constraints.append(constraint)
                    
        return set(constraints) # get unique constraints