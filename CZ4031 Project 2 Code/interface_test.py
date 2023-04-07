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
import preprocessing
import json

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

        queries_text = {
            "Query 1": "select * from customer C, orders O where C.c_mktsegment like 'BUILDING' and C.c_custkey = O.o_custkey",
            "Query 2": "select * from customer C, orders O where C.c_custkey = O.o_custkey",
            "Query 3": "SELECT col1, AVG(col2) FROM table3 GROUP BY col1;",
            "Query 4": "UPDATE table4 SET col1='new_value' WHERE col2='value';",
            "Query 5": "INSERT INTO table5 (col1, col2) VALUES ('value1', 'value2');",
            "Query 6": "DELETE FROM table6 WHERE col1='value';",
            "Query 7": "SELECT * FROM table7 WHERE col1 IN (SELECT col1 FROM table8 WHERE col2='value');"
        }
        queries_selection = list(queries_text.keys())



        # Initial Query ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.sql_container1 = ttk.Frame(self.window_container_left,borderwidth=0)
        self.sql_container1.pack(pady = 10, fill=tk.BOTH)

        my_label = Label(self.sql_container1, text="Initial Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(padx=10,pady=10,anchor = NW, side=LEFT)

        value1 = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.sql_container1, value1, queries_selection[0], *queries_selection)
        self.example_query.pack(padx=10,pady=10,anchor = NE, side = RIGHT)

        self.text_container1 = ttk.Frame(self.window_container_left,borderwidth=0)
        self.text_container1.pack()

        self.query_1 = Text(self.text_container1, width=70, height=10)
        self.query_1.pack(pady=10, padx=10)

        def update_query1(*args):
            selected_query = value1.get()
            selected_text = queries_text[selected_query]
            self.query_1.delete('1.0', tk.END)
            self.query_1.insert(tk.END, selected_text)

        value1.trace('w', update_query1)
        self.query_1.insert('1.0',"select * from customer C, orders O where C.c_custkey = O.o_custkey")



        # New Query ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.sql_container2 = ttk.Frame(self.window_container_left,borderwidth=0)
        self.sql_container2.pack(pady = 10, fill=tk.BOTH)

        my_label = Label(self.sql_container2, text="New Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(padx=10,pady=10,anchor = NW, side=LEFT)
        
        # queries_selection = list(queries_text.keys())
        value2 = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.sql_container2, value2, queries_selection[0], *queries_selection)
        self.example_query.pack(padx=10,pady=10,anchor = NE, side = RIGHT)

        self.text_container2 = ttk.Frame(self.window_container_left,borderwidth=0)
        self.text_container2.pack()

        self.query_2 = Text(self.text_container2, width=70, height=10)
        self.query_2.pack(pady=10, padx=10)

        def update_query2(*args):
            selected_query = value2.get()
            selected_text = queries_text[selected_query]
            self.query_2.delete('1.0', tk.END)
            self.query_2.insert(tk.END, selected_text)

        value2.trace('w', update_query2)
        self.query_2.insert('1.0',"select * from customer C, orders O where C.c_mktsegment like 'BUILDING' and C.c_custkey = O.o_custkey")

        #TODO: fix the submit button, only submit once
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


    # Compare the execution plans and identify any differences
    def comparePlan(self, initialPlan, newPlan, added_analysis_text):
        textToReturn = ""
        added_analysis_text = added_analysis_text + "\n================================================================== \n"
        #TODO: when initial plan > new Plan
        print('initial: ', len(initialPlan))
        print('new: ', len(newPlan))
        if (len(initialPlan) <= len(newPlan)):
            print("i should be here")
            added_analysis_text =  added_analysis_text + str(initialPlan['Node Type']) 
            added_analysis_text =  added_analysis_text + "\n" + str("‾‾" * len(initialPlan['Node Type']))

            for i in range(len(initialPlan)):
                
                initialKey = list(initialPlan.keys())[i]
                initialValue = initialPlan[initialKey]
                print("-----------------------------------------------------------")
                print("Initial key:", initialKey)
                print("Initial value:" , initialValue)

                

                for j in range(len(newPlan)):
                    newKey = list(newPlan.keys())[j]
                    newValue = newPlan[newKey]
                    print("New key:", newKey)
                    print("New value:" , newValue, "\n")
                    
                    # if they both have same keys, compare them
                    if newKey == initialKey: 

                        # if isinstance(newValue, list):
                        #     print("Recursively going through Plans here: \n")
                        #     # added_analysis_text = added_analysis_text + "\n ================================================================== \n"
                        #     for dicts_count in range(len(newPlan['Plans'])):
                        #         print("Comparing: \n", initialPlan['Plans'][dicts_count], "\n ==WITH== \n", newPlan['Plans'][dicts_count])
                        #         textToReturn = self.comparePlan(initialPlan['Plans'][dicts_count], newPlan['Plans'][dicts_count], added_analysis_text)
                        
                        if newValue != initialValue and newKey == "Startup Cost":
                            startupString = self.startupCostCompare(initialValue, newValue)
                            added_analysis_text = added_analysis_text + str(startupString)
                        
                        if newValue != initialValue and newKey == "Total Cost":
                            totalString = self.totalCostCompare(initialValue, newValue)
                            added_analysis_text = added_analysis_text + str(totalString)

                        if newValue != initialValue and newKey == "Plan Rows":
                            planRowString = self.planRowsCompare(initialValue, newValue)
                            added_analysis_text = added_analysis_text + str(planRowString)
                        
                        if newValue != initialValue and newKey != "Plans":
                            print("%%%%%%hefkwofjwiofnweo")
                            added_analysis_text = added_analysis_text + "\n\n" + newKey + " of the initial query has changed from " + str(initialValue) + " to " + str(newValue) + " in the new query." 
                            textToReturn = added_analysis_text
                            # print(textToReturn)
                        

                        break
        
            return textToReturn
        

    def why_change(self,initial,new):
        print("\nInitial_query:\n",initial)
        print("\nNew_query:\n",new)
        preprocessor = preprocessing.Preprocessing()


        updated_clause = self.get_updated_clause(initial, new)
        if updated_clause == None:
            self.analysis_text.insert('1.0', "SQL Queries are the same, please ensure they are different!")
            self.analysis_text.config(state=DISABLED)
        else:
            print(f'\nDifference in New SQL Query: ', updated_clause)
            added_analysis_text = "Difference in New SQL Query: \n" + updated_clause + "\n"

            initialPlan = preprocessor.get_query_plan(self.initial_query)
            newPlan = preprocessor.get_query_plan(self.new_query)

            # print plans in readable format
            initial_dict = json.dumps(initialPlan,indent=4)
            print("\n\n\nInitial Plan:\n", initial_dict)

            new_dict = json.dumps(newPlan,indent=4)
            print("\n\n\nNew Plan:\n", new_dict)

            # compare plans
            if initialPlan == newPlan:
                print('\n\nExecution plans are the same') 
            else:
                added_analysis_text = self.comparePlan(initialPlan, newPlan, added_analysis_text)
                self.analysis_text.insert('1.0', added_analysis_text)
                self.analysis_text.config(state=DISABLED)

     
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






    def startupCostCompare(self, initialCost, newCost):
        startupString = ""
        if initialCost > newCost:
            startupString = "\n" + "Reduced Startup Cost: The Startup Cost of the new plan has been reduced from " + str(initialCost) + " to " + str(newCost) +" . This means that the new plan requires less initial resources to start up and execute, making it faster." + "\n"
        else:
            startupString = "\n" + "Increased Startup Cost: The Startup Cost of the new plan has been increased from " + str(initialCost) + " to " + str(newCost) +" . This means that the new plan requires more initial resources to start up and execute, making it slower." + "\n"           
        return startupString


    def totalCostCompare(self, initialCost, newCost):
        totalString = ""
        if initialCost > newCost:
            totalString = "\n" + "Reduced Total Cost: The Total Cost of the new plan has been reduced from " + str(initialCost) + " to " + str(newCost) +" . This means that the overall cost of executing the query is lower in the new plan, which should result in faster execution times." + "\n"
        else:
            totalString = "\n" + "Increased Total Cost: The Total Cost of the new plan has been increased from " + str(initialCost) + " to " + str(newCost) +" . This means that the overall cost of executing the query is higher in the new plan, which should result in slower execution times." + "\n"
        return totalString


    def planRowsCompare(self, initialCost, newCost):
        planRowString = ""
        if initialCost > newCost:
            planRowString = "\n" + "Reduced Plan Rows: The Plan Rows of the new plan has been reduced from " + str(initialCost) + " to " + str(newCost) +" . This means that the new plan is expected to return fewer rows, which can result in faster execution times." + "\n"
        else:
            planRowString = "\n" + "Increased Plan Rows: The Plan Rows of the new plan has been increased from " + str(initialCost) + " to " + str(newCost) +" . This means that the new plan is expected to return more rows, which can result in slower execution times." + "\n"
        return planRowString

