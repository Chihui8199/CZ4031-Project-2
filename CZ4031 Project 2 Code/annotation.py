import json

import networkx as nx
import matplotlib.pyplot as plt

class Annotation():
    def __init__(self):
        # Example usage
        query_plan_file = 'query_plan.json'
        self.load_plan(query_plan_file)
        pass
    
    def load_plan(self, query_plan_file):
        # Load query plan from JSON file
        with open(query_plan_file) as f:
            query_plan = json.load(f)

        # Parse the query plan into a list of dictionaries
        parsed_plan = []
        for node in query_plan:
            if isinstance(node, str):
                # If node is a string, use it as the label
                node_name = node
                node_attrs = ''
            elif isinstance(node, list):
                # If node is a list, parse the node name and attributes from the first item
                if '  (' in node[0]:
                    node_name, node_attrs = node[0].split('  (', maxsplit=1)
                else:
                    node_name = node[0]
                    node_attrs = ''
                if len(node) > 1:
                    # If the node has children, add them as a list of dictionaries
                    children = []
                    for child_node in node[1:]:
                        child_name, child_attrs = child_node.split('  (', maxsplit=1)
                        child_attrs = child_attrs.rstrip(')').split(' ')
                        child_dict = {
                            'name': child_name,
                        }
                        for attr in child_attrs:
                            k, v = attr.split('=')
                            child_dict[k] = v
                        children.append(child_dict)
                    parsed_node = {'name': node_name, 'attrs': node_attrs, 'children': children}
                else:
                    parsed_node = {'name': node_name, 'attrs': node_attrs}
                parsed_plan.append(parsed_node)
        print(parsed_plan)
        
        self.create_query_plan_tree(parsed_plan)

    

    def create_query_plan_tree(self,query_plan):
        # define graph
        G = nx.DiGraph()

        # add nodes
        for i, node in enumerate(query_plan):
            label = node['name']
            cost = node['attrs']
            if i == 0:
                G.add_node(label, cost=cost)
            elif 'Hash Join' in label:
                # add join condition to label
                join_cond = query_plan[i-1]['name'].split('->')[1].strip() + ' = ' + label.split('Hash Cond: ')[1].strip()
                G.add_node(join_cond, cost='')
                G.add_node(label, cost=cost)
                G.add_edge(query_plan[i-1]['name'], join_cond)
                G.add_edge(join_cond, label)
            else:
                G.add_node(label, cost=cost)
                G.add_edge(query_plan[i-1]['name'], label)

        # draw graph
        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
        nx.draw_networkx_edges(G, pos, arrows=True)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
        plt.axis('off')
        plt.show()
            

        