from graphviz import Digraph

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
    