import difflib
import re
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import string
import ttkbootstrap as ttk
import sqlparse
from preprocessing import *
# import pyodbc
import sql_metadata

# FONT SETTINGS
FONT = "Palatino"
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
        s.configure('TFrame', background='#2C3143')
        self.window_container = ttk.Frame(self, style='TFrame')
        self.window_container.pack(fill=tk.BOTH)
        self.app_label = ttk.Label(self.window_container, text="CZ4031 Project 2", font=FONT_TITLE, anchor=CENTER, background="#2C3143", foreground='white')
        self.app_label.pack(fill=tk.X, pady=[30,30])

        # Horizontal line below title
        s.configure("Line.TSeparator", background="black")
        separator = ttk.Separator(self.window_container, orient='horizontal', style="Line.TSeparator")
        separator.pack(fill='x')
        
        
        #Create Panedwindow  
        panedwindow=PanedWindow(self, orient=HORIZONTAL, bd=4, bg="#1C1C1E")  
        panedwindow.pack(fill=BOTH, expand=True)  
        

        # Frame for left
        self.window_container_left = ttk.Frame(panedwindow,width=250,height=400)
        self.window_container_left.pack(fill=tk.BOTH, side= LEFT)
        
        # Frame for right
        self.window_container_right = ttk.Frame(panedwindow,width=250,height=400)
        self.window_container_right.pack(fill=tk.BOTH, side= RIGHT)

        panedwindow.add(self.window_container_left)  
        panedwindow.add(self.window_container_right)  


        # Left window -----------------------------------------------------------------------------------

        # self.initial_query_label = ttk.Label(self.window_container_left, text="Initial Query:", background="#2C3143")
        # self.initial_query_label.pack()

        # Initial Query ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.sql_container1 = ttk.Frame(self.window_container_left,borderwidth=0)
        self.sql_container1.pack(pady = 10, fill=tk.BOTH)

        my_label = Label(self.sql_container1, text="Initial Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(padx=10,pady=10,anchor = NW, side=LEFT)

        queries_selection = ["Query 1","Query 2","Query 3", "Query 4","Query 5","Query 6", "Query 7"]
        value = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.sql_container1, value, queries_selection[0], *queries_selection)
        self.example_query.pack(padx=10,pady=10,anchor = NE, side = RIGHT)

        self.text_container1 = ttk.Frame(self.window_container_left,borderwidth=0)
        self.text_container1.pack()

        self.query_1 = Text(self.text_container1, width=70, height=10)
        self.query_1.insert('1.0',"select * from customer C, orders O where C.c_custkey = O.o_custkey")
        self.query_1.pack(pady=10, padx=10)

        # New Query ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.sql_container2 = ttk.Frame(self.window_container_left,borderwidth=0)
        self.sql_container2.pack(pady = 10, fill=tk.BOTH)

        my_label = Label(self.sql_container2, text="New Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(padx=10,pady=10,anchor = NW, side=LEFT)
        
        queries_selection = ["Query 1","Query 2","Query 3", "Query 4","Query 5","Query 6", "Query 7"]
        value = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.sql_container2, value, queries_selection[0], *queries_selection)
        self.example_query.pack(padx=10,pady=10,anchor = NE, side = RIGHT)

        self.text_container2 = ttk.Frame(self.window_container_left,borderwidth=0)
        self.text_container2.pack()

        self.query_2 = Text(self.text_container2, width=70, height=10)
        self.query_2.insert('1.0',"select * from customer C, orders O where C.c_mktsegment like 'BUILDING' and C.c_custkey = O.o_custkey  ")
        self.query_2.pack(pady=10, padx=10)

        self.submit_button = ttk.Button (self.text_container2, text="Submit", command=self.submit_queries , bootstyle="secondary")
        self.submit_button.pack(pady=20)

        
        
        # Right window -----------------------------------------------------------------------------------

        s.configure("Custom.TNotebook", tabposition="n", background="#2C3143", bordercolor="#2C3143")
        s.configure("Custom.TNotebook.Tab",background="#6C788B",foreground='white')
        s.map("Custom.TNotebook.Tab", background=[("selected", "#2C3143")], foreground=[("selected", "white")])

        # s.configure("Custom.TNotebook.Tab",background="#6C788B",foreground='white', font=("Helvetica", 20))
        # s.map("Custom.TNotebook.Tab", background=[("selected", "#2C3143")], foreground=[("selected", "white")], font=[("selected", ("Helvetica", 20))])

        # create the notebook with the custom style
        self.tabs_holders = ttk.Notebook(self.window_container_right, style="Custom.TNotebook" )
        self.tabs_holders.pack(pady=[30,30])


        # Query Plan Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.query_container = ttk.Frame(self.tabs_holders,borderwidth=0)
        self.query_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.query_container, text="Query Plan")
        
        self.initial_query_plan_label = Label(self.query_container, text="Initial Query:", font=("Helvetica", 18))
        self.initial_query_plan_label.configure(background='#2C3143', foreground='white')        
        self.initial_query_plan_label.pack(pady=20)
        self.initial_query_plan_text = Text(self.query_container, width=70, height=10)
        self.initial_query_plan_text.pack(pady=10, padx=10)

        self.new_query_plan_label = Label(self.query_container, text="New Query:", font=("Helvetica", 18))
        self.new_query_plan_label.configure(background='#2C3143', foreground='white')        
        self.new_query_plan_label.pack(pady=20)
        self.new_query_plan_text = Text(self.query_container, width=70, height=10)
        self.new_query_plan_text.pack(pady=10, padx=10)


        # Analysis Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.analysis_container = ttk.Frame(self.tabs_holders,borderwidth=0)
        self.analysis_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.analysis_container, text="Analysis")

        self.analysis_label = Label(self.analysis_container, text="What has changed and why:", font=("Helvetica", 18))
        self.analysis_label.configure(background='#2C3143', foreground='white')
        self.analysis_label.pack(pady=20)
        self.analysis_text = Text(self.analysis_container, width=70, height=50)
        self.analysis_text.pack(pady=10, padx=10)



    def submit_queries(self):
            """
            Starts the whole analysis process of the given query.

            Trigger: By button click or shortcut key [F5]
            """
            # Disable button to prevent spamming
            self.submit_button.configure(state=DISABLED)

            # Get query from user input and clean query
            self.initial_query = self.query_1.get('1.0', 'end-1c')
            self.initial_query = self.initial_query.strip()
            self.initial_query = self.initial_query.replace('\n', ' ')

            self.new_query = self.query_2.get('1.0', 'end-1c')
            self.new_query = self.new_query.strip()
            self.new_query = self.new_query.replace('\n', ' ')
            
            self.why_change(self.initial_query,self.new_query)



    def get_updated_clause(self, initial_query, new_query):
        initial_query_parts = initial_query.split('where')
        new_query_parts = new_query.split('where')
        
        if len(initial_query_parts) == 1 or len(new_query_parts) == 1:
            return None  # Both queries don't have a WHERE clause
        
        initial_conditions = set(initial_query_parts[1].strip().split(' and '))
        new_conditions = set(new_query_parts[1].strip().split(' and '))
        added_conditions = new_conditions - initial_conditions
        
        if not added_conditions:
            return None  # There are no added conditions
        
        return ' and '.join(added_conditions)



    def why_change(self,initial,new):
        print("\nInitial_query:\n",initial)
        print("\nNew_query:\n",new)

        updated_clause = self.get_updated_clause(initial, new)
        print(f'\nDifference in New SQL Query: ', updated_clause)
        updated_clause = "Difference in New SQL Query: \n" + updated_clause
        # Compare the execution plans
        self.db = DBConnection()
        initalPlan = self.db.execute(self.initial_query)
        newPlan = self.db.execute(self.new_query)
        print("\n\n\nInitial Plan:\n",initalPlan)
        print("\nNew Plan:\n",newPlan)

        # Compare the execution plans and identify any differences
        if initalPlan == newPlan:
            print('\n\nExecution plans are the same')
            
        else:
            print("\n\n")
            string_plan = "\n\nDifference in New Query Plan:"
            for i in range(len(initalPlan)):
                if initalPlan[i] != newPlan[i]:
                    print(f'\nStep: {i}')
                    print(f'  Initial Plan:: {initalPlan[i]}')
                    print(f'  New Plan: {newPlan[i]}')
                    string_plan += f'\nStep {i}:\n' + f'  Initial Plan: {initalPlan[i]}\n' + f'  New Plan: {newPlan[i]}\n'
         
    
        self.analysis_text.insert('1.0', string_plan)
        self.analysis_text.insert('1.0', updated_clause)
        self.analysis_text.config(state=DISABLED)

        # diffs = sql_metadata.diff(plan1, plan2)

        # # Describe the changes in the execution plans
        # description = "During the data exploration, we made changes to the WHERE clause in the SQL query, which resulted in changes to the execution plan. In the original plan, the query used a {join_type} to combine the data from different tables. However, in the updated plan, the query now uses a {new_join_type} to combine the data. This change in the join type is due to the changes made in the WHERE clause of the SQL query, which affected the optimizer's decision on the most efficient way to retrieve the data.".format(join_type=diffs['join_type'], new_join_type=diffs['new_join_type'])
        



















        # my_label = Label(self.analysis_container, text="New Query:", font=("Helvetica", 18))
        # my_label.configure(background='#2C3143', foreground='white')
        # my_label.pack(pady=20)
        # my_text = Text(self.analysis_container, width=70, height=10)
        # my_text.pack(pady=[10,80], padx=10)


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
