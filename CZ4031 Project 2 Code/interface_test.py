import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as ttk

from mo_sql_parsing import parse
from pprint import pprint
from deepdiff import DeepDiff

# FONT SETTINGS
FONT = "Arial"
BOLD = "BOLD"
ITALIC = "ITALIC"
UNDERLINE = "UNDERLINE"
FONT_REGULAR = (FONT, 12)
FONT_BOLD = (f"{FONT} {BOLD}", 12)
FONT_TITLE = (f"{FONT} {BOLD}", 40)
FONT_CREDITS = (f"{FONT} {ITALIC}", 10)

class Application(ttk.Window):
    def __init__(self, master=None):
        super().__init__(self)

        self.title("CZ4031 QEP Analyzer")
        self.geometry("1400x800")
        self.generate_UI()
        self.configure(bg='#2C3143')


    def generate_UI(self):
        """
        Generate the main UI screen for most user interactions.
        """






        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame', background='#2C3143')
        self.window_container = ttk.Frame(self)

        self.window_container.pack(fill=tk.BOTH)
        # self.window_container.configure(background='#ADD8E6')


        self.app_label = ttk.Label(self.window_container, text="CZ4031 Project 2", font=FONT_TITLE, anchor=CENTER, background="#2C3143", foreground='white')
        self.app_label.pack(fill=tk.X, pady=[30,30])

        separator = ttk.Separator(self.window_container, orient='horizontal')
        separator.pack(fill='x')
        
        #Create Panedwindow  
        panedwindow=ttk.Panedwindow(self, orient=HORIZONTAL)  
        panedwindow.pack(fill=BOTH, expand=True)  
        #Create Frams  

        # Frame for left
        self.window_container_left = ttk.Frame(panedwindow,width=250,height=400, relief=GROOVE)
        self.window_container_left.pack(fill=tk.BOTH, side= LEFT)
        
        # Frame for right
        self.window_container_right = ttk.Frame(panedwindow,width=250,height=400, relief=GROOVE)
        self.window_container_right.pack(fill=tk.BOTH, side= RIGHT)

        panedwindow.add(self.window_container_left, weight=5)  
        panedwindow.add(self.window_container_right, weight=5)  


        self.initial_query_label = ttk.Label(self.window_container_left, text="Initial Query:", background="#2C3143")
        self.initial_query_label.pack(side=LEFT)

        queries_selection = ["Query 1","Query 2","Query 3", "Query 4","Query 5","Query 6", "Query 7"]
        value = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.window_container_left, value, queries_selection[0], *queries_selection)
        self.example_query.pack(padx=50)

        # self.creators_label = ttk.Label(self.window_container, text="By Group 14: Qi Wei, Kong Tat, Ryan, Xing Kun, Lyndon", font=FONT_CREDITS, anchor=CENTER,  background="#2C3143")
        # self.creators_label.pack(fill=tk.X)
    
        self.tabs_holders = ttk.Notebook(self.window_container_right, bootstyle="SECONDARY")
        self.tabs_holders.pack(fill=tk.BOTH, padx=10, pady=10)

        self.query_container = ttk.Frame(self.tabs_holders)
        self.query_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.query_container, text="Query Plan")

        self.tree_output_container = ttk.Frame(self.tabs_holders)
        self.tree_output_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.tree_output_container, text="Analysis")

        # self.sql_output_container = ttk.Frame(self.tabs_holders)
        # self.sql_output_container.pack(fill=tk.BOTH)
        # self.tabs_holders.add(self.sql_output_container, text="SQL Output (if applicable)")

        # # Create frame for user input
        # self.instruction_label = ttk.Label(self.query_container, text="Enter your sql query below and click button to analyze (or use shortcut: F5 key)", font=FONT_BOLD)
        # # self.query_entry = ScrolledText(master=self.query_container, autohide=True)
        # # self.analyze_btn = ttk.Button(self.query_container, text="ANALYZE QUERY", command=self.analyze_query, bootstyle="PRIMARY")
        # # Bind query entry to F5 Shortcut key
        # self.bind_all("<F5>", self.analyze_query)
        # self.query_option = ttk.Checkbutton(self.query_container, text="Return SQL output with analysis", variable=self.query_option_tracker_sql_output, onvalue=1, offvalue=0)
        # # Pack all elements for user input
        # self.instruction_label.pack(fill=tk.X, padx=20, pady=10)
        # self.query_entry.pack(fill=tk.BOTH,padx=20, pady=10)
        # self.query_option.pack(side=tk.LEFT, padx=20, pady=10)
        # self.analyze_btn.pack(side=tk.RIGHT, fill=tk.X, padx=20, pady=10)
        
        # # Create frame for tree output
        # self.left_annotated_sql_frame = ttk.Frame(self.tree_output_container)
        # # self.left_annotated_sql_query_display = ScrolledText(master=self.left_annotated_sql_frame, autohide=True, state=DISABLED)
        # # self.left_annotated_sql_analysis_display = ScrolledText(master=self.left_annotated_sql_frame, autohide=True, state=DISABLED)
        # self.right_tree_frame = ttk.Frame(self.tree_output_container)
        # self.qep_tooltip = ttk.Label(self.right_tree_frame, text="Click on or hover over the nodes to view analysis information.", font=FONT_BOLD)
        # # self.qep_tree =  QEPTreeVisualizer(self.right_tree_frame, self.left_annotated_sql_query_display, self.left_annotated_sql_analysis_display)
        # # Pack all elements for tree output
        # self.left_annotated_sql_frame.pack(side=LEFT) 
        # self.left_annotated_sql_query_display.pack(side=tk.TOP, fill=tk.X)
        # self.left_annotated_sql_analysis_display.pack(side=tk.BOTTOM,fill=tk.X)
        # self.right_tree_frame.pack(side=LEFT, padx=20, fill=tk.BOTH) 
        # self.qep_tooltip.pack(fill=tk.X, pady=5, side=TOP)
        # self.qep_tree.pack(fill=tk.X, padx=20, anchor=CENTER)
        
        # Add default labels
        # ttk.Label(self.sql_output_container, text = "Please select option to display SQL output in [Query] tab.", font=FONT_BOLD).pack(fill=tk.X, padx=20, pady=10, anchor=CENTER)
        # for node_type, color in NODE_COLORS.items():
        #     self.left_annotated_sql_query_display.text.tag_configure(node_type, background=color[0], foreground=color[1])
        # self.left_annotated_sql_query_display.text.tag_configure('OTHER', background='#ff9800', foreground='black')

        # self.master = master
       
        # root = tk.Tk()
        # root.configure(bg="red")
        # root.title("CZ4031 Project 2")
        # # root.geometry("1151x631")
        # #setting window size
        
        # # width=1200
        # # height=800
        # root.geometry("1280x800")
        

        # self.window_container = ttk.Frame(self)
        
        # self.window_container.pack(fill=tk.BOTH)
        # self.window_container.configure(bg='#ADD8E6')
        # self.app_label = ttk.Label(self.window_container, text="CZ4031 QEP Analyzer (2022)", font=FONT_TITLE, anchor=CENTER)
        # self.app_label.pack(fill=tk.X, pady=[10,0])

        # self.input_container = ttk.Frame(self)
        # self.input_container.pack(side=LEFT)
        # self.input_container.inputs()

    # def inputs(self):

    #     def submit():
    #         input_1 = entry_1.get()
    #         input_2 = entry_2.get()
    #         print("Input 1:", input_1)
    #         print("Input 2:", input_2)    
         
        # Create label and entry for first input
        # label_1 = tk.Label(root, text="Input 1:")
        # label_1.pack()
        # entry_1 = tk.Entry(root)
        # entry_1.pack()

        # # Create label and entry for second input
        # label_2 = tk.Label(root, text="Input 2:")
        # label_2.pack()
        # entry_2 = tk.Entry(root)
        # entry_2.pack()

        # # Create submit button
        # submit_button = tk.Button(root, text="Submit", command=submit)
        # submit_button.pack()


    
class Comparison:
    def __init__(self):
        print("Looking for difference------------")
    
    def comparing(self,sql_query1, sql_query2):
        
        parsed_query1 = parse(sql_query1)
        parsed_query2 = parse(sql_query2)
        ddiff = DeepDiff(parsed_query1, parsed_query2)
        difference = self.comparing_changes(ddiff, sql_query1,sql_query2,parsed_query1, parsed_query2)
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
                            if isinstance(element, dict):
                                element = element.get('literal')
                            if isinstance(element, str):
                                conditions = [c.strip() for c in element.split('where')[1].split('and')]
                            else:
                                conditions = element
                            if 'new_value' in value and 'old_value' in value:
                                old_value = value['old_value']
                                new_value = value['new_value']
                                for cond in conditions:
                                    if f"'{old_value}'" in cond and f"'{new_value}'" not in cond:
                                        column = cond.split()[0]
                                        diffString += "\nThe " + column + "changed from " + old_value + "to" + new_value
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
            diffString = self.find_token_changed(ddiff)

        return diffString 

        


    

    