"""
Contains code for annotations
"""
from anytree import AnyNode, PreOrderIter
import interface
import copy 
import re 

class Annotation:
    """
    Helps in the generation of data structure that will be used to show annotations on the application later on.
    """
    
    def __init__(self):
        print("Init annotations")

    
    def build_tree(self, plan_list, parent=None):
        """
        Recursive function used to build tree based on plan_list retrieved from json returned by database
        """
        result_list = []
        for plan in plan_list: 
            node_type = plan['Node Type'].upper() 

            # set node 
            if parent is None: 
                node = AnyNode(id = node_type, node_type=node_type) 
            else: 
                node = AnyNode(id = node_type, node_type=node_type, parent=parent)

            # Setting the key attributes that are going to be used for searching later
            if node_type in interface.KEY_PROPERTY:
                key_properties = interface.KEY_PROPERTY[node_type]
                for key_property in key_properties:
                    if key_property in plan:
                        setattr(node, key_property, plan[key_property])

            # if "Output" in plan:
            #     setattr(node, "Output", plan["Output"])
            raw_json = copy.deepcopy(plan)
            
            if "Plans" in plan:
                self.build_tree(plan["Plans"], node)  # Build sub tree recursive call 
                raw_json.pop("Plans")  # Don't put the entire subtree in the raw json
            if "Partial Mode" in plan:
                setattr(node, "Partial Mode", plan["Partial Mode"])
            if "Index Name" in plan:
                setattr(node, "Index Name", plan["Index Name"])
            setattr(node, "raw_json", raw_json)
            print(raw_json)
            result_list.append(node)


        return result_list

    def build_invert_relation(self, query_formatted, tree):
        """
        Build relation between plan and query by iterating the tree
        Match a given node to all tokens that correlate
        """
        match_dict = {}  # Has structure {node object : [list of tuples of index]}
        tokens = self.tokenize_query(query_formatted)
        for node in PreOrderIter(tree):
            # ID is node type
            if getattr(node, 'id') not in interface.KEY_PROPERTY:
                continue
            else:
                for field in interface.KEY_PROPERTY[getattr(node, 'id')]:
                    if not hasattr(node, field):
                        continue
                    value = getattr(node, field)
                    matched_pos = self.search_query(value, tokens, query_formatted)
                    if matched_pos is not None:
                        if node in match_dict:
                            match_dict[node] = match_dict[node] + matched_pos
                        else:
                            match_dict[node] = matched_pos
        return match_dict

    def add_aqp_analysis_to_qep(self, qep_tree, aqp_tree, node_category_output_mapping_list, ref_constraint):
        """
        Add AQP analysis to qep node for nodes that have analysis returned from AQPS


        Logic:
        node_category_output_mapping_list has a datastructure of (category, node_type_from_qep, output_from_node)
        
        First we get the reference constraint from ref_constraint, then we use it to find the node_type
        Then based on the node type, we get the node category.
        Iterate through QEP and match the elements [category] and [output_from_node]] in node_category_output_mapping_list to get the equivalent node.
        
        Modify the QEP node that matches and append some analysis data
        """

        # Get join type by constraint
        print(f"Constraint in 'add_aqp_analysis_to_qep' is {ref_constraint}")
        node_type_to_match = None
        node_category_to_match = None
        node_output_to_match = None
        mapping_index_found = -1
        for n_type, constraint in interface.NODE_TYPES_CONSTRAINTS_MAPPING.items():
            if (ref_constraint == constraint):
                node_type_to_match = n_type
                break
        if (node_type_to_match is not None):
            for category, type_list in interface.NODE_TYPES_CATEGORY_MAPPING.items():
                if node_type_to_match in type_list:
                    node_category_to_match = category
                    break
        for mapping in node_category_output_mapping_list:
            mapped_category = mapping[0].upper()
            mapped_node_type = mapping[1].upper()
            mapped_output = mapping[2]
            if (node_category_to_match == mapped_category and node_type_to_match == mapped_node_type):
                node_output_to_match = mapped_output
                mapping_index_found = node_category_output_mapping_list.index(mapping)
                break

        
        if (node_category_to_match is None or node_output_to_match is None):
            return None # Nothing to update since we dont have matching category or output
        
        # Iterate through QEP and evaluate the category and outputs. If exists then that means the equivalent AQP's details can be compared
        qep_node_to_update = None

        for qep_node in PreOrderIter(qep_tree):
            if qep_node_to_update is not None:
                break # Only need to find 1 node
            # ID is node type
            if getattr(qep_node, 'id') not in interface.KEY_PROPERTY:
                continue
            else:
                qep_node_type = getattr(qep_node, 'node_type').upper()
                
                # Get QEP Output
                qep_raw_json = qep_node.raw_json
                if ('aqp_analysis_message' in qep_raw_json.keys()):
                    print("Skipping node 123")
                    continue # means that this qep has been touched already. we do not want this.
                if ('Output' in qep_raw_json.keys()):
                    qep_output = qep_raw_json['Output']
                else:
                    qep_output = None
                # Get QEP Category
                qep_node_category = None
                for category, type_list in interface.NODE_TYPES_CATEGORY_MAPPING.items():
                    if qep_node_type in type_list:
                        qep_node_category = category
                        break
                # Try to match with mapping list => node_category_output_mapping_list
                print(f"Need to match category: {qep_node_category} and output {qep_output} to {node_category_to_match} , {node_output_to_match}")
                
                if (qep_node_category == node_category_to_match and qep_output == node_output_to_match):
                        qep_node_to_update = qep_node
                        
        if (qep_node_to_update is None or mapping_index_found == -1):
            return # No node to update or invalid mapping. so no need add aqp since there is no equivalent ones.

        print("KWIWIWASD")
        print(qep_node_to_update)
        print(node_category_output_mapping_list[mapping_index_found])

        # Locate the AQP nodes
        aqp_node_to_update = None
        for aqp_node in PreOrderIter(aqp_tree):
            if aqp_node_to_update is not None:
                break # Only need to find 1 node
            # ID is node type
            if getattr(aqp_node, 'id') not in interface.KEY_PROPERTY:
                continue
            else:
                aqp_node_type = getattr(aqp_node, 'node_type').upper()
                # Get AQP Output
                aqp_raw_json = aqp_node.raw_json
                if ('Output' in aqp_raw_json.keys()):
                    aqp_output = aqp_raw_json['Output']
                else:
                    aqp_output = None
                
                # Get AQP Category
                aqp_node_category = None
                for category, type_list in interface.NODE_TYPES_CATEGORY_MAPPING.items():
                    if aqp_node_type in type_list:
                        aqp_node_category = category
                        break
                print(f"Current aqp_node => type: {aqp_node_type}, output: {aqp_output}, category: {aqp_node_category}")
                # Try to match with mapping list => node_category_output_mapping_list
                selected_mapping = node_category_output_mapping_list[mapping_index_found]
                print(f"Selected mapping {selected_mapping}")
                selected_mapped_category = selected_mapping[0].upper()
                selected_mapped_output = selected_mapping[2]
                if (aqp_node_category == selected_mapped_category and aqp_output == selected_mapped_output):
                    aqp_node_to_update = aqp_node
                    print("MATCHED!")

        if (aqp_node_to_update is None):
            return None # No aqp matching found
        

        ## ACTUAL COMPARSION BY COSTS

        # Compare the aqp just based on cost for this algorithm.
        qep_node_to_update_node_type = None
        aqp_node_to_update_node_type = None

        qep_node_total_cost = None
        aqp_node_total_cost = None
        aqp_node_to_update_raw_json = aqp_node_to_update.raw_json
        qep_node_to_update_raw_json = qep_node_to_update.raw_json
        
        qep_node_to_update_node_type = getattr(qep_node_to_update, 'node_type').upper()
        aqp_node_to_update_node_type = getattr(aqp_node_to_update, 'node_type').upper()

        if (aqp_node_to_update_node_type == qep_node_to_update_node_type):
            return None

        if ('Total Cost' in qep_node_to_update_raw_json.keys()):
            qep_node_total_cost = qep_node_to_update_raw_json['Total Cost']
        if ('Total Cost' in aqp_node_to_update_raw_json.keys()):
            aqp_node_total_cost = aqp_node_to_update_raw_json['Total Cost']

        performance_ratio = round(aqp_node_total_cost/qep_node_total_cost)
        
        # BULD ANAYLSIS TEXT
        print(f"\nCost of {qep_node_to_update_node_type}:{qep_node_total_cost}, Cost of {aqp_node_to_update_node_type}:{aqp_node_total_cost}.\n\n")
        if (qep_node_total_cost < aqp_node_total_cost):
            print(f"Performance Ratio: {performance_ratio}")
            aqp_analysis_message = f"\nCost of {qep_node_to_update_node_type}:{qep_node_total_cost}, Cost of {aqp_node_to_update_node_type}:{aqp_node_total_cost}.\n\n"
            if (performance_ratio == 1):
                aqp_analysis_message += f"{qep_node_to_update_node_type} is used because running {qep_node_to_update_node_type} costs {qep_node_total_cost} while {aqp_node_to_update_node_type} costs {aqp_node_total_cost}.\n\nHence {qep_node_to_update_node_type} runs slightly faster"
            else:
                aqp_analysis_message += f"{qep_node_to_update_node_type} is used because running {qep_node_to_update_node_type} is {performance_ratio} times faster than {aqp_node_to_update_node_type}"

            print(f"AQP INSIGHTS: {aqp_analysis_message}")
            qep_node_to_update.raw_json["aqp_analysis_message"] = aqp_analysis_message

        node_category_output_mapping_list.pop(mapping_index_found)
        return qep_tree, node_category_output_mapping_list # 1 less thing to find.
         

    def build_node_category_output_mapping(self, tree):
        """
        Iterate through tree to get node_category from node_type and output and link them together.

        Output of nodes are not dependent on the stragey used. This is used so that we can re-associated the alternative query execution plan to the current one.

        """
        node_category_output_mapping_list = []

        for node in PreOrderIter(tree):
            # ID is node type
            if getattr(node, 'id') not in interface.KEY_PROPERTY:
                continue
            else:
                node_type = getattr(node, 'node_type').upper()
                raw_json = node.raw_json
                if ('Output' in raw_json.keys()):
                    output = raw_json['Output']
                else:
                    output = None
                print(f"Node type: {node_type} , output: {output}")
                if output is not None:
                    node_category = None
                    for category, type_list in interface.NODE_TYPES_CATEGORY_MAPPING.items():
                        if node_type in type_list:
                            node_category = category
                            break
                    if (node_category is not None):
                        node_category_output_mapping_list.append([node_category, node_type, output])
        return node_category_output_mapping_list



    def search_query(self, value, tokens, query_formatted):
        """
        Do full text search on query
        Return a list of index tuple of matched query tokens or None if no token matched
        """
        matched_pos = []
        if isinstance(value, list):
            for v in value:
                regex_matches = re.finditer(v, query_formatted)
                for match in regex_matches:
                    matched_pos.append((match.start(), match.end()))
        else:
            regex_matches = re.finditer(str(value).strip('()'), query_formatted)
            for match in regex_matches:
                matched_pos.append((match.start(), match.end()))

        for token, position in tokens.items():  # position is a tuple of (start idx, end idx)
        
            # Assume value can be either a list of string or a string. Could it also be dict?
            if isinstance(value, list):  # value is a list of string
                for v in value:
                    if token in v:
                        matched_pos.append(position)
                        break
            else:  # value is string
                if token in str(value):
                    matched_pos.append(position)

        if len(matched_pos) == 0:
            return None
        else:
            return matched_pos


    def tokenize_query(self, query_formatted):
        """
        Tokenize query, return a dictionary with structure {token: (start index in query, end index..)}
        No keyword included in the result
        """
        tokens = {}
        lines = query_formatted.splitlines()  # Process query line by line
        processed_lines_len = 0
        for i in range(len(lines)):
            if i > 0:
                # +1 because of newline character has length 1
                processed_lines_len += len(lines[i - 1]) + 1

            tokenized_line = re.split('[ (),]', lines[i])
            print('tokenized line: ' + str(tokenized_line))
            for token in tokenized_line:
                token = token.strip(';')
                if token.upper() != '' and token.upper() not in interface.KEYWORDS:
                    regex_matches = re.finditer(r'([ (,])' + token + '($| |\)|,)', lines[i])
                    for matched in regex_matches:
                        tokens[token] = (matched.start() + processed_lines_len, matched.end() + processed_lines_len)
                        print('appending token: ' + token + ', pos: ' + str(tokens[token]))
                    # index_in_query = lines[i].index(token) + processed_lines_len
                    # tokens[token] = (index_in_query, index_in_query + len(token))

        print('Tokens:' + str(tokens))
        return tokens