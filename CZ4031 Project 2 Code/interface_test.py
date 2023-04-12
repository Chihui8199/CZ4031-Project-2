import re
import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.tix import IMAGETEXT
import ttkbootstrap as ttk
from preprocessing import *
# import pyodbc
import preprocessing
import annotation
from PIL import ImageTk, Image
from ttkbootstrap.tableview import Tableview

from mo_sql_parsing import parse as sqlparser
from pprint import pprint
from deepdiff import DeepDiff

# FONT SETTINGS
FONT = "Helvetica"
FONT_MONSTERRAT = "Palatino"
BOLD = "BOLD"
ITALIC = "ITALIC"
UNDERLINE = "UNDERLINE"
FONT_NORMAL = (FONT, 18)
FONT_BOLD = (f"{FONT} {BOLD}", 20)
FONT_TITLE = (f"{FONT_MONSTERRAT} {BOLD}", 40)
FONT_UNDERLINE = (f"{FONT} {UNDERLINE}", 18)
FONT_CREDITS = (f"{FONT} {ITALIC}", 10)


class Application(ttk.Window):
    def __init__(self, master=None):
        super().__init__(self)

        self.title("CZ4031 QEP Analyzer")
        self.geometry("1920x1080")
        self.generate_UI()
        self.configure(bg='#2C3143')
        
        # set application icon
        self.favicon_ico_path = 'CZ4031 Project 2 Code/cool.ico'
        self.icon_photo = ImageTk.PhotoImage(
        Image.open(self.favicon_ico_path))
        self.iconphoto(False, self.icon_photo)

    
    def generate_UI(self):
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

        my_label = Label(self.sql_container1, text="Initial Query:", font=FONT_NORMAL)
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

        my_label = Label(self.sql_container2, text="New Query:", font=FONT_NORMAL)
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


        # Query Plan Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.query_container = ttk.Frame(self.tabs_holders,borderwidth=0)
        self.query_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.query_container, text="Query Plan")

        self.initial_subframe = ttk.Frame(self.query_container, borderwidth=0)
        self.new_subframe2 = ttk.Frame(self.query_container, borderwidth=0)
        
        self.initial_query_plan_label = Label(self.initial_subframe, text="Initial Query:", font=FONT_UNDERLINE)
        self.initial_query_plan_label.configure(background='#2C3143', foreground='white')  
        self.initial_query_plan_label.pack(padx = 20, pady = 20, expand = True, fill = BOTH)
        self.initial_query_plan_text = Text(self.initial_subframe, width=40, height=50, wrap="word")
        self.initial_query_plan_text.pack(padx = 10, pady = 10, expand = True, fill = BOTH)

        self.new_query_plan_label = Label(self.new_subframe2, text="New Query:", font=FONT_UNDERLINE)
        self.new_query_plan_label.configure(background='#2C3143', foreground='white')  
        self.new_query_plan_label.pack(padx = 20, pady = 20, expand = True, fill = BOTH)
        self.new_query_plan_text = Text(self.new_subframe2, width=40, height=50, wrap="word")
        self.new_query_plan_text.pack(padx = 10, pady = 10, expand = True, fill = BOTH)

        self.initial_subframe.pack(expand = True, fill = BOTH, side = LEFT)
        self.new_subframe2.pack(expand = True, fill = BOTH, side = LEFT)

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


    def why_change(self,initial,new):

        print("\nInitial_query:\n",initial)
        print("\nNew_query:\n",new)
        preprocessor = preprocessing.Preprocessing()
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        body_font = font.Font(family="Helvetica", size=12)

        updated_clause = self.get_updated_clause(initial, new)
        if updated_clause == None:
            messagebox.showerror("showwarning", "SQL Queries are the same, please ensure they are different!")
            self.analysis_text.config(state=DISABLED)

        else:
            print(f'\nDifference in New SQL Query: ', updated_clause)
            added_analysis_text = "Difference in New SQL Query: \n" + updated_clause + "\n"

            # Get Query plans from user input
            try:
                initialPlan = preprocessor.get_query_plan(self.initial_query)
                newPlan = preprocessor.get_query_plan(self.new_query)
            except Exception as e:
                messagebox.showerror("showwarning", "Please input a working SQL Query!")
                return
            
            # Get table output
            self.tableTab(self.initial_query,self.sql_output_container_initial)
            self.tableTab(self.new_query,self.sql_output_container_new)
            
            try:
                # Generate Graph as images
                annotator = annotation.Annotation(initialPlan)
                annotator.generate_graph("img/initialPlan")
                annotator = annotation.Annotation(newPlan)
                annotator.generate_graph("img/newPlan")

                # insert images into Text Box
                self.initial_query_plan_text.config(state="normal")
                self.initial_query_plan_text.delete('1.0', END)
                imgInitial = Image.open("img/initialPlan.png")
                w, h = imgInitial.size
                ratio = min(self.initial_query_plan_text.winfo_width() / w, self.initial_query_plan_text.winfo_height() / h)
                new_size = (int(w * ratio), int(h * ratio))
                imgInitial = imgInitial.resize(new_size)
                # resized_initial_image= imgInitial.resize((self.initial_query_plan_text.winfo_width(), self.initial_query_plan_text.winfo_height()))
                # self.initial_img = ImageTk.PhotoImage(resized_initial_image)
                self.initial_img = ImageTk.PhotoImage(imgInitial)
                self.initial_query_plan_text.image_create(END, image=self.initial_img)
                self.initial_query_plan_text.config(state=DISABLED)

                self.new_query_plan_text.config(state="normal")
                self.new_query_plan_text.delete('1.0', END)
                imgNew = Image.open("img/newPlan.png")
                w, h = imgNew.size
                ratio = min(self.new_query_plan_text.winfo_width() / w, self.new_query_plan_text.winfo_height() / h)
                new_size = (int(w * ratio), int(h * ratio))
                imgNew = imgNew.resize(new_size)
                # resized_new_image= imgNew.resize((self.new_query_plan_text.winfo_width(), self.new_query_plan_text.winfo_height()))
                # self.new_img = ImageTk.PhotoImage(resized_new_image)
                self.new_img = ImageTk.PhotoImage(imgNew)
                self.new_query_plan_text.image_create(END, image=self.new_img)
                self.new_query_plan_text.config(state=DISABLED)

                self.analysis_text.config(state="normal")
                self.analysis_text.delete('1.0', END)

                # compare plans
                if initialPlan == newPlan:
                    print('\n\nExecution plans are the same') 
                    self.comparePlan(initialPlan, newPlan, added_analysis_text)
                    self.analysis_text.config(state="normal")
                    self.analysis_text.delete('1.0', END) 
                    self.analysis_text.insert('1.0', "The SQL Queries have the same query plan!")

                else:
                    
                    # Get all Initial Query Join and Relations relationships
                    self.analysis_text.config(state="normal")
                    # self.analysis_text.insert(END, "==========================================================================\n")
                    self.analysis_text.insert(END, "In the Initial Query:\n", ("title",))
                    initialJoinString = self.searchJoin(initialPlan)

                    # Get all New Query Join and Relations relationships
                    # self.analysis_text.insert(END, "\n==========================================================================\n")
                    self.analysis_text.insert(END, "\nIn the New Query:\n", ("title",))
                    newJoinString = self.searchJoin(newPlan)
                    # self.analysis_text.insert(END, "\n==========================================================================\n\n\n")
                    if initialJoinString == newJoinString:
                        self.analysis_text.delete('1.0', END)
                    
                # Get cost of both plans and compare them
                costString = self.printCost(initialPlan,newPlan)
                self.analysis_text.insert(END, "\nTotal Cost Comparison:\n\n", ("title",))
                self.analysis_text.insert(END, costString, ("body",))
                self.analysis_text.tag_configure("title", font=title_font, underline=True)
                self.analysis_text.tag_configure("body", font=body_font)
                self.analysis_text.config(state=DISABLED) 

            except Exception as e:
                messagebox.showerror("showwarning", "SQL Query is invalid, please try again!")
                        
    # 
    def checkClause(self, clause, where_clause_initial, where_clause_new):
        match_initial = re.search(clause, where_clause_initial, re.IGNORECASE)
        match_new = re.search(clause, where_clause_new, re.IGNORECASE)

        if match_initial:
            where_clause_initial = where_clause_initial[:match_initial.start()]

        if match_new:
            where_clause_new = where_clause_new[:match_new.start()]

        print("\n\nInitial clause:\n", where_clause_initial)
        print("\n\nNew clause:\n", where_clause_new)
        return where_clause_initial, where_clause_new

    # 
    def checkSubClause(self, clause1, clauseList, clause_initial, clause_new):        
        # if clauses exist for both
        if clause_initial and clause_new:
            # checking all the clauses
            clauseList = [r"(GROUP BY .*)", r"(HAVING .*)", r"(ORDER BY .*)"]

            for clause2 in clauseList:
                if clause1 == clause2:
                    continue
                clause_initial, clause_new = self.checkClause(clause2, clause_initial, clause_new)
                return clause_initial, clause_new
    
    #TODO we are missing LIMIT and OFFSET clauses
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

    # Search for all Joins, Relations and Scan type for a plan
    def searchJoin(self,plan):

        joinList, relationList, scanList = [],[], []
        joinOrder = 0

        # find relations to join type and put into a list as a tuple
        def findRelations(plan,joinOrder,joinList, relationList):

            for i in range(len(plan)):
                initialKey = list(plan.keys())[i]
                initialValue = plan[initialKey]

                # append all Node Type that contains Join/NestedLoop with joinOrder
                if initialKey == 'Node Type':
                
                    if "Join" in initialValue or "Nested Loop" in initialValue:
                        joinOrder += 1
                        joinList.append((joinOrder, initialValue))

                # append all Relation Name with joinorder and get Scan type of relations
                if initialKey == 'Relation Name':
                    relationList.append((joinOrder,initialValue))
                    scanList.append((initialValue, plan['Node Type']))
                    
                # recursively iterate through all Plans
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
        joincount=0
        # Make a join dictionary that connects Join to Relations based on joinOrder
        for join in joinList:
            tempList = []
            joincount+=1
            for relations in relationList:
                if join[0] <= relations[0]:
                    tempList.append(relations[1])
            join_dict[join[1]+str(joincount)] = tempList

        
        # Remove duplicate relations in join_dict
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
                        
                    
        listToReturn = []
        body_font = font.Font(family="Helvetica", size=12)
        self.analysis_text.config(state="normal")

        # Print out join relations
        for join in join_dict:
            try:
                joinString = f"\n{join[:-1]} was used between '{join_dict[join][0]}'({scan_dict[join_dict[join][0]]}) and '{join_dict[join][1]}'({scan_dict[join_dict[join][1]]})\n"
                listToReturn.append(joinString)
                self.analysis_text.insert(END, joinString, ("body",) )
            except Exception as e:
                try:
                    joinString = f"\n{join[:-1]} was used between '{join_dict[join][0]}'({scan_dict[join_dict[join][0]]}) and '{join_dict[join][1]}'\n"
                    listToReturn.append(joinString)
                    self.analysis_text.insert(END, joinString, ("body",))

                except Exception as e:
                    joinString = f"\n{join[:-1]} was used between '{join_dict[join][0]}' and '{join_dict[join][1]}'\n"
                    listToReturn.append(joinString)
                    self.analysis_text.insert(END, joinString, ("body",))

        self.analysis_text.tag_configure("body", font=body_font) 
        return listToReturn
              
    def createTableOutput(self, output, columns, container):

        # Prepare column data
        columnData = []
        for header in columns:
            headerColumn = {"text": f"{header}", "stretch": True}
            columnData.append(headerColumn)
        
        # Prepare row data
        rowData = []
        for row in output:
            rowData.append(row)

        # Create table view
        dt = Tableview(
            master=container,
            coldata=columnData,
            rowdata=rowData,
            paginated=True,
            pagesize=50,
            searchable=True,
            stripecolor=(None, None),
            autoalign= True,
            autofit = True
        )
        dt.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

    def tableTab(self,query, container):
        for child in container.winfo_children():
            child.destroy() # Clean up sql output
        preprocessor = preprocessing.Preprocessing()

        actual_output, column_names  = preprocessor.get_query_results(query)

        if (actual_output is None):
            self.analyze_btn.configure(state=ACTIVE)
            return
        elif (len(actual_output) == 0):
            self.no_results = ttk.Label(container, text="No results matching the query provided.", font=FONT_BOLD, anchor=CENTER, background="#2C3143", foreground='white')
            self.no_results.pack(fill=tk.X, pady=[30,30])
        else:
            self.createTableOutput(actual_output, column_names, container) 

    
class Comparison:
    def __init__(self):
        print("Looking for difference------------")
    
    def comparing(self,sql_query1, sql_query2):
        parsed_query1 = sqlparser(sql_query1)
        parsed_query2 = sqlparser(sql_query2)
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
            diffString = self.find_token_changed(ddiff)

        return diffString 

        


    

    
