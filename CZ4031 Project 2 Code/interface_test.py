import difflib
import re
import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import string
from tkinter.tix import IMAGETEXT
import ttkbootstrap as ttk
import sqlparse
from preprocessing import *
# import pyodbc
import sql_metadata
import preprocessing
import json
import annotation
from PIL import ImageTk, Image
from ttkbootstrap.tableview import Tableview

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
        self.geometry("1920x1080")
        self.generate_UI()
        self.configure(bg='#2C3143')
        # self.iconbitmap("CZ4031 Project 2 Code/app_icon.ico")
        self.favicon_ico_path = 'CZ4031 Project 2 Code/cool.ico'
        self.icon_photo = ImageTk.PhotoImage(
        Image.open(self.favicon_ico_path))
        self.iconphoto(False, self.icon_photo)

    
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
            "default": "select l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue from customer, orders, lineitem where customer.c_custkey = orders.o_orderkey and lineitem.l_orderkey = orders.o_orderkey and orders.o_orderdate < '1995-03-15'  and l_shipdate < '1995-03-15' and c_mktsegment = 'BUILDING' GROUP by l_orderkey, o_orderdate, o_shippriority order by revenue desc, o_orderdate LIMIT 20",
            "W/O orderby": "select l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue from customer, orders, lineitem where customer.c_custkey = orders.o_orderkey and lineitem.l_orderkey = orders.o_orderkey and orders.o_orderdate < '1995-03-15'  and l_shipdate < '1995-03-15' and c_mktsegment = 'BUILDING' GROUP by l_orderkey, o_orderdate, o_shippriority order by o_orderdate LIMIT 20",
            "W/O where": "select l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue from customer, orders, lineitem where customer.c_custkey = orders.o_orderkey and lineitem.l_orderkey = orders.o_orderkey and orders.o_orderdate < '1995-03-15'  and l_shipdate < '1995-03-15' GROUP by l_orderkey, o_orderdate, o_shippriority order by revenue desc, o_orderdate LIMIT 20",
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

        self.query_1 = Text(self.text_container1, width=70, height=10, wrap="word")
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

        self.query_2 = Text(self.text_container2, width=70, height=10, wrap="word")
        self.query_2.pack(pady=10, padx=10)

        def update_query2(*args):
            selected_query = value2.get()
            selected_text = queries_text[selected_query]
            self.query_2.delete('1.0', tk.END)
            self.query_2.insert(tk.END, selected_text)

        value2.trace('w', update_query2)
        self.query_2.insert('1.0',"select * from customer C, orders O where C.c_mktsegment like 'BUILDING' and C.c_custkey = O.o_custkey")

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
        self.tabs_holders.pack(fill=tk.BOTH, padx=40, pady=20)


        # Label Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.query_container = ttk.Frame(self.tabs_holders,borderwidth=0)
        self.query_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.query_container, text="Query Plan")

        self.subframe = ttk.Frame(self.query_container, borderwidth=0)
        self.subframe.pack(side= TOP)

        self.initial_query_plan_label = Label(self.subframe, text=": Initial Query", font=("Helvetica", 18))
        self.initial_query_plan_label.configure(background='#2C3143', foreground='white')  
        # self.initial_query_plan_label.place(relx=0.5, rely=0.5,anchor=CENTER)      
        self.initial_query_plan_label.pack(padx=20,pady=20, side = LEFT)#, anchor=W, side= LEFT)

        self.new_query_plan_label = Label(self.subframe, text="New Query :", font=("Helvetica", 18))
        self.new_query_plan_label.configure(background='#2C3143', foreground='white')        
        # self.new_query_plan_label.place(relx=0.5, rely=0.5,anchor=CENTER)     
        self.new_query_plan_label.pack(padx=20, pady=20, side = RIGHT)#, anchor=E,side= RIGHT)

        # Inital Plan Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
        self.initial_text_container = ttk.Frame(self.query_container,borderwidth=0)
        self.initial_text_container.pack(side= LEFT, fill=BOTH)
        self.initial_query_plan_text = Text(self.initial_text_container, width=60, height=50, wrap="word")
        
        self.initial_query_plan_text.pack(pady=10, padx=10, side= LEFT, fill=BOTH)

        # New Plan Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.new_text_container = ttk.Frame(self.query_container,borderwidth=0)
        self.new_text_container.pack(side= RIGHT, fill=BOTH)
        self.new_query_plan_text = Text(self.new_text_container, width=60, height=50, wrap="word")
         
        self.new_query_plan_text.pack(pady=10, padx=10, side= RIGHT, fill=BOTH)

        # Analysis Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.analysis_container = ttk.Frame(self.tabs_holders,borderwidth=0)
        self.analysis_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.analysis_container, text="Analysis")

        self.analysis_label = Label(self.analysis_container, text="What has changed and why:", font=("Helvetica", 18))
        self.analysis_label.configure(background='#2C3143', foreground='white')
        self.analysis_label.pack(pady=20)
        self.analysis_text = Text(self.analysis_container, width=70, height=50, wrap="word")
        self.analysis_text.pack(pady=10, padx=10)

        self.sql_output_container_initial = ttk.Frame(self.tabs_holders,borderwidth=0)
        self.sql_output_container_initial.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.sql_output_container_initial, text="Output (Initial Query)")

        self.sql_output_container_new = ttk.Frame(self.tabs_holders,borderwidth=0)
        self.sql_output_container_new.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.sql_output_container_new, text="Output (New Query)")


    def submit_queries(self):
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
            self.submit_button.config(state="normal")


    # Compare the execution plans and identify any differences
    def comparePlan(self, initialPlan, newPlan, added_analysis_text):
        textToReturn = ""
        added_analysis_text = added_analysis_text + "\n================================================================== \n"
        
        # print('initial: ', len(initialPlan))
        # print('new: ', len(newPlan))
       
        if (len(initialPlan) <= len(newPlan)):
            added_analysis_text =  added_analysis_text + str(initialPlan['Node Type']) 
            added_analysis_text =  added_analysis_text + "\n" + str("‾‾" * len(initialPlan['Node Type']))

            for i in range(len(initialPlan)):
                
                initialKey = list(initialPlan.keys())[i]
                initialValue = initialPlan[initialKey]
                # print("-----------------------------------------------------------")
                # print("Initial key:", initialKey)
                # print("Initial value:" , initialValue)

                

                for j in range(len(newPlan)):
                    newKey = list(newPlan.keys())[j]
                    newValue = newPlan[newKey]
                    # print("New key:", newKey)
                    # print("New value:" , newValue, "\n")
                    
                    # if they both have same keys, compare them
                    if newKey == initialKey: 

                        if isinstance(newValue, list):
                            # print("Recursively going through Plans here: \n")
                            # added_analysis_text = added_analysis_text + "\n ================================================================== \n"
                            for dicts_count in range(len(newPlan['Plans'])):
                                # print("Comparing: \n", initialPlan['Plans'][dicts_count], "\n ==WITH== \n", newPlan['Plans'][dicts_count])
                                textToReturn = self.comparePlan(initialPlan['Plans'][dicts_count], newPlan['Plans'][dicts_count], added_analysis_text)
                        
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
                            # added_analysis_text = added_analysis_text + "\n\n" + newKey + " of the initial query has changed from " + str(initialValue) + " to " + str(newValue) + " in the new query." 
                            textToReturn = added_analysis_text
                        

                        break
       

            # Return text
            return textToReturn

        #TODO: when initial plan > new Plan
        # else:
        #     added_analysis_text =  added_analysis_text + str(newPlan['Node Type']) 
        #     added_analysis_text =  added_analysis_text + "\n" + str("‾‾" * len(newPlan['Node Type']))

        #     for i in range(len(initialPlan)):
                
        #         initialKey = list(initialPlan.keys())[i]
        #         initialValue = initialPlan[initialKey]
        #         print("-----------------------------------------------------------")
        #         print("Initial key:", initialKey)
        #         print("Initial value:" , initialValue)

                

        #         for j in range(len(newPlan)):
        #             newKey = list(newPlan.keys())[j]
        #             newValue = newPlan[newKey]
        #             print("New key:", newKey)
        #             print("New value:" , newValue, "\n")
                    
        #             # if they both have same keys, compare them
        #             if newKey == initialKey: 

        #                 # if isinstance(newValue, list):
        #                 #     print("Recursively going through Plans here: \n")
        #                 #     # added_analysis_text = added_analysis_text + "\n ================================================================== \n"
        #                 #     for dicts_count in range(len(newPlan['Plans'])):
        #                 #         print("Comparing: \n", initialPlan['Plans'][dicts_count], "\n ==WITH== \n", newPlan['Plans'][dicts_count])
        #                 #         textToReturn = self.comparePlan(initialPlan['Plans'][dicts_count], newPlan['Plans'][dicts_count], added_analysis_text)
                        
        #                 if newValue != initialValue and newKey == "Startup Cost":
        #                     startupString = self.startupCostCompare(initialValue, newValue)
        #                     added_analysis_text = added_analysis_text + str(startupString)
                        
        #                 if newValue != initialValue and newKey == "Total Cost":
        #                     totalString = self.totalCostCompare(initialValue, newValue)
        #                     added_analysis_text = added_analysis_text + str(totalString)

        #                 if newValue != initialValue and newKey == "Plan Rows":
        #                     planRowString = self.planRowsCompare(initialValue, newValue)
        #                     added_analysis_text = added_analysis_text + str(planRowString)
                        
        #                 if newValue != initialValue and newKey != "Plans":
        #                     # added_analysis_text = added_analysis_text + "\n\n" + newKey + " of the initial query has changed from " + str(initialValue) + " to " + str(newValue) + " in the new query." 
        #                     textToReturn = added_analysis_text
                        

        #                 break
        
        #     return textToReturn
        


    def why_change(self,initial,new):

        print("\nInitial_query:\n",initial)
        print("\nNew_query:\n",new)
        preprocessor = preprocessing.Preprocessing()
        custom_font = font.Font(family="Helvetica", size=18, weight="bold")

        updated_clause = self.get_updated_clause(initial, new)
        if updated_clause == None:
            # self.analysis_text.config(state="normal")
            # self.analysis_text.delete('1.0', END) # have to clear the output from before first before inserting
            # self.analysis_text.insert('1.0', "\n\n\n\n\n\n\n\n\n\n\n\n\n\nSQL Queries are the same, please ensure they are different!", ("custom",))
            # self.analysis_text.tag_configure("custom", font=custom_font, justify='center')
            messagebox.showerror("showwarning", "SQL Queries are the same, please ensure they are different!")

            self.analysis_text.config(state=DISABLED)
        else:
            
            print(f'\nDifference in New SQL Query: ', updated_clause)
            added_analysis_text = "Difference in New SQL Query: \n" + updated_clause + "\n"

            try:
                initialPlan = preprocessor.get_query_plan(self.initial_query)
                newPlan = preprocessor.get_query_plan(self.new_query)
            except Exception as e:
                messagebox.showerror("showwarning", "Please input a working SQL Query!")
                return
            
            
            def tableTab(query, container):
                for child in container.winfo_children():
                    child.destroy() # Clean up sql output

                actual_output, column_names  = preprocessor.get_query_results(query)

                if (actual_output is None):
                    self.analyze_btn.configure(state=ACTIVE)
                    return
                elif (len(actual_output) == 0):
                    ttk.Label(container, text = "No results matching.", font=FONT_BOLD).pack(fill=tk.X, padx=20, pady=10, anchor=CENTER)
                else:
                    self.create_table_view(actual_output, column_names, container) 
            
            # Initial Query Table ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            for child in self.sql_output_container_initial.winfo_children():
                child.destroy() # Clean up sql output

            actual_output_initial, column_names_initial  = preprocessor.get_query_results(self.initial_query)

            if (actual_output_initial is None):
                self.analyze_btn.configure(state=ACTIVE)
                return
            elif (len(actual_output_initial) == 0):
                ttk.Label(self.sql_output_container_initial, text = "No results matching.", font=FONT_BOLD).pack(fill=tk.X, padx=20, pady=10, anchor=CENTER)
            else:
                self.create_table_view(actual_output_initial, column_names_initial, self.sql_output_container_initial) 

            # New Query table ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            for child in self.sql_output_container_new.winfo_children():
                child.destroy() # Clean up sql output

            actual_output_new, column_names_new  = preprocessor.get_query_results(self.new_query)

            if (actual_output_new is None):
                self.analyze_btn.configure(state=ACTIVE)
                return
            elif (len(actual_output_new) == 0):
                ttk.Label(self.sql_output_container_new, text = "No results matching.", font=FONT_BOLD).pack(fill=tk.X, padx=20, pady=10, anchor=CENTER)
            else:
                self.create_table_view(actual_output_new, column_names_new, self.sql_output_container_new) 

            try:
                

                annotator = annotation.Annotation(initialPlan)
                annotator.generate_graph("img/initialPlan")
                annotator = annotation.Annotation(newPlan)
                annotator.generate_graph("img/newPlan")

                self.initial_query_plan_text.config(state="normal")
                self.initial_query_plan_text.delete('1.0', END) # have to clear the output from before first before inserting
                imgInitial = Image.open("img/initialPlan.png")
                # resized_initial_image= imgInitial.resize((self.initial_query_plan_text.winfo_width(), self.initial_query_plan_text.winfo_height()))
                # self.initial_img = ImageTk.PhotoImage(resized_initial_image)
                self.initial_img = ImageTk.PhotoImage(imgInitial)
                self.initial_query_plan_text.image_create(END, image=self.initial_img)
                self.initial_query_plan_text.config(state=DISABLED)

                self.new_query_plan_text.config(state="normal")
                self.new_query_plan_text.delete('1.0', END) # have to clear the output from before first before inserting
                imgNew = Image.open("img/newPlan.png")
                # resized_new_image= imgNew.resize((self.new_query_plan_text.winfo_width(), self.new_query_plan_text.winfo_height()))
                # self.new_img = ImageTk.PhotoImage(resized_new_image)
                self.new_img = ImageTk.PhotoImage(imgNew)
                self.new_query_plan_text.image_create(END, image=self.new_img)
                self.new_query_plan_text.config(state=DISABLED)

                # PUT STUFF HERE TO TEST

                # compare plans
                if initialPlan == newPlan:
                    print('\n\nExecution plans are the same') 
                    self.comparePlan(initialPlan, newPlan, added_analysis_text)
                    self.analysis_text.config(state="normal")
                    self.analysis_text.delete('1.0', END) # have to clear the output from before first before inserting
                    self.analysis_text.insert('1.0', "The SQL Queries have the same query plan!")
                    costString = self.printCost(initialPlan,newPlan)
                    self.analysis_text.insert('1.0', costString)
                    self.analysis_text.config(state=DISABLED)
                else:
                    added_analysis_text = self.comparePlan(initialPlan, newPlan, added_analysis_text)
                    self.analysis_text.config(state="normal")
                    self.analysis_text.delete('1.0', END) # have to clear the output from before first before inserting
                    # self.analysis_text.insert('1.0', added_analysis_text)

                    
                    # print("=============================================")
                    # compareInitialRelationString = self.printJoinRelations(initialPlan, "Initial Plan:")
                    # self.analysis_text.insert(END, compareInitialRelationString)
                    # print("=============================================")

                    # compareNewRelationString = self.printJoinRelations(newPlan, "\n\nNew Plan:")
                    # self.analysis_text.insert(END, compareNewRelationString)

                    self.analysis_text.config(state="normal")
                    self.analysis_text.insert(END, "==========================================================================\n")
                    self.analysis_text.insert(END, "\nIn the Initial Query:\n", ("custom",))
                    initialJoinString = self.searchJoin(initialPlan)

                    self.analysis_text.insert(END, "\n==========================================================================\n")
                    self.analysis_text.insert(END, "\nIn the New Query:\n", ("custom",))
                    newJoinString = self.searchJoin(newPlan)
                    self.analysis_text.insert(END, "\n==========================================================================\n\n\n")
                    if initialJoinString == newJoinString:
                        self.analysis_text.delete('1.0', END)
                    
                
                    costString = self.printCost(initialPlan,newPlan)
                    self.analysis_text.insert(END, "Total Cost Comparison:\n\n", ("custom",))
                    self.analysis_text.insert(END, costString)
                    self.analysis_text.tag_configure("custom", font=custom_font, underline=True)
                    self.analysis_text.config(state=DISABLED) 


            
            except Exception as e:
                messagebox.showerror("showwarning", "SQL Query is invalid, please try again!")
                        
            





    def checkClause(self, pattern, where_clause_initial, where_clause_new):
        match_initial = re.search(pattern, where_clause_initial, re.IGNORECASE)
        match_new = re.search(pattern, where_clause_new, re.IGNORECASE)

        if match_initial:
            where_clause_initial = where_clause_initial[:match_initial.start()]

        if match_new:
            where_clause_new = where_clause_new[:match_new.start()]

        print("\n\nInitial:\n", where_clause_initial)
        print("\n\nNew:\n", where_clause_new)
        return where_clause_initial, where_clause_new


    def checkSubClause(self, clause1, clauseList, clause_initial, clause_new):        
        # if groupby clauses exist for both
        if clause_initial and clause_new:
            # checking all the clauses
            clauseList = [r"(GROUP BY .*)", r"(HAVING .*)", r"(ORDER BY .*)"]

            for clause2 in clauseList:
                if clause1 == clause2:
                    continue
                clause_initial, clause_new = self.checkClause(clause2, clause_initial, clause_new)
                return clause_initial, clause_new
    
    
    def get_updated_clause(self, initial_query, new_query):
        difference = ""

        pattern = r"(WHERE .*)"
        where_match_initial = re.search(pattern, initial_query, re.IGNORECASE)
        where_match_new = re.search(pattern, new_query, re.IGNORECASE)

        # if where clauses exist for both
        if where_match_initial and where_match_new:
            # removing the first 5 characters (where)
            first_where_clause_initial = where_match_initial.group(1)[6:]
            print("\n\nInitial:\n", first_where_clause_initial)
            
            first_where_clause_new = where_match_new.group(1)[6:]
            print("\n\nNew:\n", first_where_clause_new)


            # checking all the clauses
            clauseList = [r"(GROUP BY .*)", r"(HAVING .*)", r"(ORDER BY .*)", r"(LIMIT .*)", r"(OFFSET .*)"]

            for clause in clauseList:
                where_clause_initial, where_clause_new = self.checkClause(clause, first_where_clause_initial, first_where_clause_new)
                
            if (where_clause_initial == where_clause_new):
                print("Where clause is the same")
                return None

            else:
                print("Different")
                
                initial_conditions = set(map(str.strip, where_clause_initial.split('and')))
                new_conditions = set(map(str.strip, where_clause_new.split('and')))
               
                # Getting the difference 

                # if new query is shorter than inital query
                if len(new_query) > len(initial_query):
                    diff_conditions = new_conditions - initial_conditions
                # if new query is longer than inital query
                else:
                    diff_conditions = initial_conditions - new_conditions

                print("\ninitial ", initial_conditions)
                print("\nnew ", new_conditions)
                print("\nDIFF ", diff_conditions)
                difference = difference + str(diff_conditions) + "in the WHERE clause"




            
            clauseList = [r"(GROUP BY .*)", r"(HAVING .*)", r"(ORDER BY .*)"]
            
            for clause1 in clauseList:
                clause_initial, clause_new = self.checkClause(clause1, first_where_clause_initial, first_where_clause_new)
                clause_initial, clause_new = self.checkSubClause(clause1, clauseList, clause_initial, clause_new)

                if clause1 == r"(GROUP BY .*)":
                    groupby_clause_initial = clause_initial
                    groupby_clause_new = clause_new

                if clause1 == r"(HAVING .*)":
                    having_clause_initial = clause_initial
                    having_clause_new = clause_new
                    print(having_clause_initial)
                    print(having_clause_new)

                if clause1 == r"(ORDER BY .*)":
                    orderby_clause_initial = clause_initial
                    orderby_clause_new = clause_new
                    print(orderby_clause_initial)
                    print(orderby_clause_new)

            
        else:
            print("WHERE clause not found.")

    
        return difference


    def calculateCost(self, plan):
        totalCost = 0
        for i in range(len(plan)):     
            initialKey = list(plan.keys())[i]
            initialValue = plan[initialKey]
            if initialKey == 'Total Cost':
                totalCost += initialValue
        return totalCost
            

    def printCost(self,initialPlan,newPlan):
        total_initial_cost = self.calculateCost(initialPlan)
        total_new_cost = self.calculateCost(newPlan)
        if total_new_cost < total_initial_cost:
            total_initial_cost_string = f"The total cost has reduced from {total_initial_cost} in the initial plan to {total_new_cost} in the new plan. This means that the overall cost of executing the query is lower in the new plan, which should result in faster execution times.\n"
            return str(total_initial_cost_string)
        
        else:
            total_initial_cost_string = f"The total cost has increased from {total_initial_cost} in the initial plan to {total_new_cost} in the new plan. This means that the overall cost of executing the query is higher in the new plan, which should result in slower execution times.\n"
            return str(total_initial_cost_string)


    def printJoinRelations(self, plan, resultString):
        for i in range(len(plan)):     
            print("iteration", i)
            initialKey = list(plan.keys())[i]
            initialValue = plan[initialKey]

            if initialKey == 'Node Type':

                if "Join" in initialValue or "Nested" in initialValue:
                    joinString = f"\n{initialValue} was used between "
                    resultString = resultString + joinString
                
                if "Scan" in initialValue:
                    scanString = f" ({initialValue})"

            elif initialKey == 'Relation Name':
                relationString = f"{initialValue}" + scanString
                print(relationString)
                resultString = resultString + relationString
                
            elif initialKey == 'Plans':
                count = 0
                for arrays in initialValue:
                    print(count)
                    if count == 1:
                        resultString = resultString + " and "
                    print("NESTINGGGGGG")
                    resultString = self.printJoinRelations(arrays, resultString)
                    count+=1

        return resultString



    def searchJoin(self,plan):

        joinList, relationList, scanList = [],[], []
        joinOrder = 0

        # find relations to join type and put into a list as a tuple
        def findRelations(plan,joinOrder,joinList, relationList):

            for i in range(len(plan)):
                initialKey = list(plan.keys())[i]
                initialValue = plan[initialKey]

                if initialKey == 'Node Type':
                
                    if "Join" in initialValue or "Nested Loop" in initialValue:
                        joinOrder += 1
                        joinList.append((joinOrder, initialValue))

                if initialKey == 'Relation Name':
                    relationList.append((joinOrder,initialValue))
                    scanList.append((initialValue, plan['Node Type']))
                    
                
                if initialKey == 'Plans':
                    for j in initialValue:
                        findRelations(j,joinOrder,joinList,relationList)
            
            return joinList, relationList
        

        joinList,relationList = findRelations(plan,joinOrder, joinList, relationList)

        # Make dictionary of Relations to Scan
        scan_dict = {}
        for relations,scan in scanList:
            scan_dict[relations] = scan
    
        join_dict = {}

        for join in joinList:
            tempList = []
            for relations in relationList:
                if join[0] <= relations[0]:
                    tempList.append(relations[1])
            join_dict[join[1]] = tempList

        for join in join_dict:

            for join2 in join_dict:
                if join == join2: 
                    continue

                if all(elem in join_dict[join2] for elem in join_dict[join]):
                    elemstring = ""
                    for elem in join_dict[join]:
                        join_dict[join2].remove(elem)
                        elemstring = elemstring + elem + ", "
                    elemstring = "[" + elemstring[:-2] + "]"
                    join_dict[join2].append(elemstring)
                        
                    
        print("Dict here",join_dict)
        listToReturn = []
        for join in join_dict:
            try:
                joinString = f"\n{join} was used between '{join_dict[join][0]}'({scan_dict[join_dict[join][0]]}) and '{join_dict[join][1]}'({scan_dict[join_dict[join][1]]})\n"
                listToReturn.append(joinString)
                self.analysis_text.config(state="normal")
                self.analysis_text.insert(END, joinString)
            except Exception as e:
                try:
                    joinString = f"\n{join} was used between '{join_dict[join][0]}'({scan_dict[join_dict[join][0]]}) and '{join_dict[join][1]}'\n"
                    listToReturn.append(joinString)
                    self.analysis_text.config(state="normal")
                    self.analysis_text.insert(END, joinString)

                except Exception as e:
                    joinString = f"\n{join} was used between '{join_dict[join][0]}' and '{join_dict[join][1]}'\n"
                    listToReturn.append(joinString)
                    self.analysis_text.config(state="normal")
                    self.analysis_text.insert(END, joinString)
                    
        return listToReturn
                    
        
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

    def create_table_view(self, output, columns, container):
        """
        Used to create a table view for the sql output. Extracts the row and column information
        """ 
        # Prepare column data
        coldata = []
        for name in columns:
            header_column = {"text": f"{name}", "stretch": True}
            coldata.append(header_column)
        
        # Prepare row data
        rowdata = []
        for row in output:
            rowdata.append(row)

        # Create table view
        dt = Tableview(
            master=container,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            pagesize=50,
            searchable=True,
            # bootstyle="primary",
            stripecolor=(None, None),
            autoalign= True,
            autofit = True
        )
        dt.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)