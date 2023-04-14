'''
Contains code for Graphical User Interface
'''

import tkinter as tk
from tkinter import *
from tkinter import font, messagebox
import ttkbootstrap as ttk
from explain import *
import explain
from PIL import ImageTk, Image
from ttkbootstrap.tableview import Tableview

# Fonts
FONT_TITLE = ("Palatino BOLD", 40)
FONT_NORMAL = ("Helvetica", 18)
FONT_BOLD = ("Helvetica BOLD", 20)
FONT_UNDERLINE = ("Helvetica UNDERLINE", 18)

# Example Queries for dropdown
QUERIES_TEXT = {
            "Example Queries": " ",
            "Query 1": "SELECT * FROM customer C, orders O WHERE C.c_mktsegment like 'BUILDING' and C.c_custkey = O.o_custkey", #if query is the same
            "Query 2": "SELECT * FROM customer C, orders O WHERE C.c_mktsegment like 'AUTOMOBILE' AND C.c_custkey = O.o_custkey", #

            "Query 3": """SELECT l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue
            FROM customer, orders, lineitem 
            WHERE customer.c_custkey = orders.o_orderkey 
                AND lineitem.l_orderkey = orders.o_orderkey 
                AND orders.o_orderdate < '1995-03-15'  
            GROUP BY l_orderkey, o_orderdate, o_shippriority 
            ORDER BY revenue desc, o_orderdate 
            LIMIT 20""",

            "Query 4": """SELECT l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue 
            FROM customer, orders, lineitem 
            WHERE customer.c_custkey = orders.o_orderkey 
                AND lineitem.l_orderkey = orders.o_orderkey 
                AND orders.o_orderdate < '1995-03-15'  
                AND c_mktsegment = 'BUILDING' 
            GROUP BY l_orderkey, o_orderdate, o_shippriority 
            ORDER BY revenue desc, o_orderdate 
            LIMIT 20""",

            "Query 5": """SELECT o_orderdate, o_shippriority
            FROM customer, orders 
            WHERE customer.c_custkey = orders.o_orderkey 
                AND orders.o_orderdate < '1995-03-15'
                AND customer.c_acctbal > '9000'
                AND customer.c_mktsegment = 'BUILDING' 
            GROUP by o_orderdate, o_shippriority""",

            "Query 6": """SELECT o_orderdate, o_shippriority
            FROM customer, orders 
            WHERE customer.c_custkey = orders.o_orderkey 
                AND orders.o_orderdate < '1995-03-15'
                AND customer.c_mktsegment = 'BUILDING' 
            GROUP by o_orderdate, o_shippriority""",

            "Query 7": """SELECT *
            FROM customer
            WHERE customer.c_phone = '25-989-741-2988'""",

            "Query 8": """SELECT *
            FROM customer
            WHERE customer.c_phone = '25-989-741-2988'
            OR customer.c_nationkey > '20'""",

            "Query 9": """SELECT o_orderdate, o_shippriority
            FROM customer, orders 
            WHERE customer.c_custkey = orders.o_orderkey 
                AND orders.o_orderdate < '1995-03-15'
            OR customer.c_custkey= '2' 
            GROUP by o_orderdate, o_shippriority
            LIMIT 20""",

            "Query 10": """SELECT o_orderdate, o_shippriority
            FROM customer, orders 
            WHERE customer.c_custkey = orders.o_orderkey 
                AND orders.o_orderdate < '1995-03-15'
            GROUP by o_orderdate, o_shippriority
            LIMIT 20""",

            "Query 11": """SELECT * 
            FROM customer C, orders O 
            WHERE C.c_mktsegment like 'BUILDING' 
                AND C.c_custkey = O.o_custkey""",

            "Query 12": """SELECT * 
            FROM customer C, orders O 
            WHERE C.c_mktsegment like 'HOUSEHOLD' 
                AND C.c_custkey = O.o_custkey
                AND C.c_acctbal > '300000'""",

            "Query 13": """SELECT *  
            FROM customer C, orders O 
            WHERE C.c_custkey = O.o_custkey""",

            "Query 14": """SELECT C.c_custkey  
            FROM customer C, orders O 
            WHERE C.c_custkey = O.o_custkey""",

            "Query 15": """SELECT orders.o_orderkey, customer.c_custkey, lineitem.l_partkey, lineitem.l_quantity, lineitem.l_extendedprice
            FROM orders, customer, lineitem
            WHERE orders.o_custkey = customer.c_custkey
                AND orders.o_orderkey = lineitem.l_orderkey
                AND orders.o_orderdate BETWEEN '1994-01-01' AND '1994-01-31'
                AND lineitem.l_discount BETWEEN 0.05 AND 0.10
                AND customer.c_mktsegment = 'AUTOMOBILE'
            ORDER BY orders.o_orderkey, customer.c_custkey, lineitem.l_partkey;""",

            "Query 16": """SELECT orders.o_orderkey, customer.c_custkey
            FROM orders, customer
            WHERE orders.o_custkey = customer.c_custkey
                AND orders.o_orderdate BETWEEN '1994-01-01' 
                AND '1994-01-31'
                AND customer.c_mktsegment = 'AUTOMOBILE'
            ORDER BY orders.o_orderkey, customer.c_custkey;""",
            
            "Query 17": """SELECT l_orderkey, SUM(l_extendedprice*(1-l_discount)) AS revenue, o_orderdate, o_shippriority
            FROM customer, orders, lineitem
            WHERE c_mktsegment = 'HOUSEHOLD'
                AND c_custkey = o_custkey 
                AND l_orderkey = o_orderkey 
                AND o_orderdate < '1995-03-15' 
                AND l_shipdate > '1995-03-15' 
            GROUP BY l_orderkey, o_orderdate, o_shippriority
            HAVING SUM(l_extendedprice*(1-l_discount)) > 10000
            ORDER BY o_orderdate
            LIMIT 10;""",

            "Query 18": """SELECT l_orderkey, SUM(l_extendedprice*(1-l_discount)) AS revenue, o_orderdate, o_shippriority
            FROM customer, orders, lineitem
            WHERE c_mktsegment = 'HOUSEHOLD'
                AND c_custkey = o_custkey 
                AND l_orderkey = o_orderkey 
                AND o_orderdate < '1995-03-15' 
                AND l_shipdate > '1995-03-15' 
            GROUP BY l_orderkey, o_orderdate
            HAVING SUM(l_extendedprice*(1-l_discount)) > 10000
            ORDER BY o_orderdate
            LIMIT 10;""",

            "Query 19": """SELECT l_orderkey, SUM(l_extendedprice*(1-l_discount)) AS revenue, o_orderdate 
            FROM customer, orders, lineitem 
            WHERE c_mktsegment = 'HOUSEHOLD'
                AND c_custkey = o_custkey 
                AND l_orderkey = o_orderkey 
                AND o_orderdate < '1995-03-15' 
                AND l_shipdate > '1995-03-15'  
            GROUP BY l_orderkey, o_orderdate 
            HAVING SUM(l_extendedprice*(1-l_discount)) > 10000 
            ORDER BY revenue DESC, o_orderdate 
            LIMIT 10; """,

            "Query 20": """SELECT l_orderkey, SUM(l_extendedprice*(1-l_discount)) AS revenue, o_orderdate, o_shippriority
            FROM customer, orders, lineitem 
            WHERE c_mktsegment = 'HOUSEHOLD'
                AND c_custkey = o_custkey 
                AND l_orderkey = o_orderkey 
                AND o_orderdate < '1995-03-15' 
                AND l_shipdate > '1995-03-15'  
            GROUP BY l_orderkey, o_orderdate, o_shippriority
            HAVING SUM(l_extendedprice*(1-l_discount)) > 10000 
            ORDER BY o_orderdate 
            LIMIT 10; """,
            
            "Query 21": """SELECT l_orderkey, SUM(l_extendedprice*(1-l_discount)) AS revenue, o_orderdate, o_shippriority 
            FROM customer, orders, lineitem 
            WHERE c_mktsegment = 'HOUSEHOLD'
                AND c_custkey = o_custkey 
                AND l_orderkey = o_orderkey 
                AND o_orderdate < '1995-03-15' 
                AND l_shipdate > '1995-03-15'  
            GROUP BY l_orderkey, o_orderdate, o_shippriority 
            HAVING revenue > 10000
            ORDER BY revenue DESC, o_orderdate 
            LIMIT 10; """,

            "Query 22": """SELECT l_orderkey, SUM(l_extendedprice*(1-l_discount)) AS revenue, o_orderdate, o_shippriority 
            FROM customer, orders, lineitem 
            WHERE c_mktsegment = 'HOUSEHOLD'
                AND c_custkey = o_custkey 
                AND l_orderkey = o_orderkey 
                AND o_orderdate < '1995-03-15' 
                AND l_shipdate > '1995-03-15'  
            GROUP BY l_orderkey, o_orderdate, o_shippriority 
            ORDER BY revenue DESC, o_orderdate 
            LIMIT 10; """,
            
        }

class Application(ttk.Window):
    def __init__(self, master=None):
        '''
         Initialize the Tkinter Application.
        '''
        super().__init__(self)

        # Set the title and dimensions of the window
        self.title("CZ4031 Project 2")
        self.geometry("1920x1080")
        self.generate_UI()
        self.configure(bg='#2C3143')

        # Set application icon
        self.favicon_ico_path = 'img/logo.ico'
        self.icon_photo = ImageTk.PhotoImage(
            Image.open(self.favicon_ico_path))
        self.iconphoto(False, self.icon_photo)

    def generate_UI(self):
        '''
         Generate and return the UI for CZ4031 Project 2.
        '''

        s = ttk.Style()
        s.configure('TFrame', background='#2C3143')
        self.window_container = ttk.Frame(self, style='TFrame')
        self.window_container.pack(fill=tk.BOTH)
        self.app_label = ttk.Label(self.window_container, text="CZ4031 Project 2", font=FONT_TITLE, anchor=CENTER, background="#2C3143", foreground='white')
        self.app_label.pack(fill=tk.X, pady=[30, 30])

        # Horizontal line below title
        s.configure("Line.TSeparator", background="black")
        separator = ttk.Separator(self.window_container, orient='horizontal', style="Line.TSeparator")
        separator.pack(fill='x')

        # Create Panedwindow
        panedwindow = PanedWindow(self, orient=HORIZONTAL, bd=4, bg="#1C1C1E")
        panedwindow.pack(fill=BOTH, expand=True)

        # Frame for left
        self.window_container_left = ttk.Frame(panedwindow, width=250, height=400)
        self.window_container_left.pack(fill=tk.BOTH, side=LEFT)

        # Frame for right
        self.window_container_right = ttk.Frame(panedwindow, width=250, height=400)
        self.window_container_right.pack(fill=tk.BOTH, side=RIGHT)

        panedwindow.add(self.window_container_left)
        panedwindow.add(self.window_container_right)

        # Left window -----------------------------------------------------------------------------------

        # Initial Query ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.sql_container1 = ttk.Frame(self.window_container_left, borderwidth=0)
        self.sql_container1.pack(pady=10, fill=tk.BOTH)

        my_label = Label(self.sql_container1, text="Initial Query:", font=FONT_NORMAL)
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(padx=10, pady=10, anchor=NW, side=LEFT)

        queries_selection = list(QUERIES_TEXT.keys())
        value1 = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.sql_container1, value1, queries_selection[0], *queries_selection)
        self.example_query.pack(padx=10, pady=10, anchor=NE, side=RIGHT)

        self.text_container1 = ttk.Frame(self.window_container_left, borderwidth=0)
        self.text_container1.pack(fill=X)

        self.query_1 = Text(self.text_container1, width=70,height=14, wrap="word")
        self.query_1.pack(pady=10, padx=10,fill=X)

        def update_query1(*args):
            '''
             Update initial query input to match selected query in dropdown. This is called when user selects an Example Query in the dropdown.
            '''
            selected_query = value1.get()
            selected_text = QUERIES_TEXT[selected_query]
            self.query_1.delete('1.0', tk.END)
            self.query_1.insert(tk.END, selected_text)

        value1.trace('w', update_query1)

        # New Query ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.sql_container2 = ttk.Frame(self.window_container_left, borderwidth=0)
        self.sql_container2.pack(pady=10, fill=tk.BOTH)

        my_label = Label(self.sql_container2, text="New Query:", font=FONT_NORMAL)
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(padx=10, pady=10, anchor=NW, side=LEFT)

        value2 = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.sql_container2, value2, queries_selection[0], *queries_selection)
        self.example_query.pack(padx=10, pady=10, anchor=NE, side=RIGHT)

        self.text_container2 = ttk.Frame(self.window_container_left, borderwidth=0)
        self.text_container2.pack(fill=X)

        self.query_2 = Text(self.text_container2, width=70,height=14, wrap="word")
        self.query_2.pack(pady=10, padx=10,fill=X)

        def update_query2(*args):
            '''
             Update new query input to match selected query in dropdown. This is called when user selects an Example Query in the dropdown.
            '''
            selected_query = value2.get()
            selected_text = QUERIES_TEXT[selected_query]
            self.query_2.delete('1.0', tk.END)
            self.query_2.insert(tk.END, selected_text)

        value2.trace('w', update_query2)

        self.submit_button = ttk.Button(self.text_container2, text="Submit", command=self.submit_queries, bootstyle="secondary")
        self.submit_button.pack(pady=20)


        # Right window -----------------------------------------------------------------------------------

        s.configure("Custom.TNotebook", tabposition="n", background="#2C3143", bordercolor="#2C3143")
        s.configure("Custom.TNotebook.Tab", background="#6C788B", foreground='white')
        s.map("Custom.TNotebook.Tab", background=[("selected", "#2C3143")], foreground=[("selected", "white")])

        self.tabs_holders = ttk.Notebook(self.window_container_right, style="Custom.TNotebook")
        self.tabs_holders.pack(fill=tk.BOTH, padx=40, pady=20)

        # Query Plan Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.query_container = ttk.Frame(self.tabs_holders, borderwidth=0)
        self.query_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.query_container, text="Query Plan")

        self.initial_subframe = ttk.Frame(self.query_container, borderwidth=0)
        self.new_subframe2 = ttk.Frame(self.query_container, borderwidth=0)

        self.initial_query_plan_label = Label(self.initial_subframe, text="Initial Query:", font=FONT_UNDERLINE)
        self.initial_query_plan_label.configure(background='#2C3143', foreground='white')
        self.initial_query_plan_label.pack(padx=20, pady=20, expand=True, fill=BOTH)
        self.initial_query_plan_text = Text(self.initial_subframe, width=40, height=50, wrap="word")
        self.initial_query_plan_text.pack(padx=10, pady=10, expand=True, fill=BOTH)

        self.new_query_plan_label = Label(self.new_subframe2, text="New Query:", font=FONT_UNDERLINE)
        self.new_query_plan_label.configure(background='#2C3143', foreground='white')
        self.new_query_plan_label.pack(padx=20, pady=20, expand=True, fill=BOTH)
        self.new_query_plan_text = Text(self.new_subframe2, width=40, height=50, wrap="word")
        self.new_query_plan_text.pack(padx=10, pady=10, expand=True, fill=BOTH)

        self.initial_subframe.pack(expand=True, fill=BOTH, side=LEFT)
        self.new_subframe2.pack(expand=True, fill=BOTH, side=LEFT)

        # Analysis Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.analysis_container = ttk.Frame(self.tabs_holders, borderwidth=0)
        self.analysis_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.analysis_container, text="Analysis")

        self.analysis_label = Label(self.analysis_container, text="What has changed and why:", font=("Helvetica", 18))
        self.analysis_label.configure(background='#2C3143', foreground='white')
        self.analysis_label.pack(pady=20)
        self.analysis_text = Text(self.analysis_container, width=70, height=50, wrap="word")
        self.analysis_text.pack(pady=10, padx=10, expand=True, fill=BOTH)
        
        # Output (Inital Query) Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.sql_output_container_initial = ttk.Frame(self.tabs_holders, borderwidth=0)
        self.sql_output_container_initial.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.sql_output_container_initial, text="Output (Initial Query)")

        # Output (New Query) Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.sql_output_container_new = ttk.Frame(self.tabs_holders, borderwidth=0)
        self.sql_output_container_new.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.sql_output_container_new,text="Output (New Query)")

        # Login ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.login_window = Toplevel(self.window_container)
        self.login_window.title("Login")
        self.login_window.grab_set()
        width = 300
        height = 240
        screen_width = self.window_container.winfo_screenwidth()
        screen_height = self.window_container.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width / 2)
        y_coordinate = (screen_height / 2) - (height / 2)
        self.login_window.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))

        # Create the login form
        self.host_label = ttk.Label(self.login_window, text="Host:")
        self.host_entry = ttk.Entry(self.login_window)
        self.host_entry.insert(0, "localhost")

        self.port_label = ttk.Label(self.login_window, text="Port:")
        self.port_entry = ttk.Entry(self.login_window)
        self.port_entry.insert(0, '5432')

        self.database_label = ttk.Label(self.login_window, text="Database:")
        self.database_entry = ttk.Entry(self.login_window)

        self.user_label = ttk.Label(self.login_window, text="User:")
        self.user_entry = ttk.Entry(self.login_window)

        self.password_label = ttk.Label(self.login_window, text="Password:")
        self.password_entry = ttk.Entry(self.login_window, show="*")

        self.login_button = ttk.Button(self.login_window, text="Login", command=self.login)

        # Lay out the login form using grid
        self.host_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.port_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        self.database_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.database_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        self.user_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.user_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        self.password_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.password_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        self.login_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Focus the username entry widget
        self.host_entry.focus_set()

        # Bind the <Return> key to the login method
        self.login_window.bind("<Return>", self.login)
        self.login_window.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

    def login(self, event=None):
        '''
         Connects to the database. This is called when the user clicks the login button.
        '''
        self.configList = [self.host_entry.get(),
                           self.port_entry.get(),
                           self.database_entry.get(),
                           self.user_entry.get(),
                           self.password_entry.get()]
        try:
            preprocessor = explain.Preprocessing(self.configList)
            messagebox.showinfo("Login", "You are now logged in!")
            self.login_window.destroy()
        except Exception as e:
            messagebox.showinfo("Failed", "Login failed")


    def submit_queries(self):
        '''
         Submit the user's input SQL queries to illustrating_changes.
        '''
        # Disable the submit button until the results are generated
        self.submit_button.configure(state=DISABLED)

        # Get the SQL queries from user input and clean queries
        self.initial_query = self.query_1.get('1.0', 'end-1c')
        self.initial_query = self.initial_query.strip()
        self.initial_query = self.initial_query.replace('\n', ' ')

        self.new_query = self.query_2.get('1.0', 'end-1c')
        self.new_query = self.new_query.strip()
        self.new_query = self.new_query.replace('\n', ' ')

        # Pass in the cleaned queries into illustrating_changes
        self.illustrating_changes(self.initial_query, self.new_query)

        self.submit_button.config(state="normal")

    def initial_query_validation(self, initial_query, new_query, preprocessor):
        '''
         Validates the initial and new queries.
         
         Args:
         	 initial_query: The initial SQL query to be validated
         	 new_query: The new SQL query to be validated
         	 preprocessor: The preprocessor that is used to perform preprocessing
         
         Returns: 
         	 True if both queries are valid and False if either or both queries are invalid
        '''
        validation1 = preprocessor.validate_query(initial_query)
        validation2 = preprocessor.validate_query(new_query)

        if validation1["error"] == True:
            messagebox.showerror(
                "showwarning", "Initial Query: " + validation1["error_message"])
            return False

        if validation2["error"] == True:
            messagebox.showerror(
                "showwarning", "New Query: " + validation2["error_message"])
            return False
        return True


    def illustrating_changes(self, initial, new):
        '''
        Displays the Query Plans and Analysis.
        
        Args:
            initial: The initial SQL query
            new: The new SQL query

        '''

        preprocessor = explain.Preprocessing(self.configList)
        isValid = self.initial_query_validation(initial, new, preprocessor)
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        body_font = font.Font(family="Helvetica", size=14)

        # If the SQL Queries are valid
        if isValid:
            comparing = explain.Comparison()
            updated_clause = comparing.comparing(initial, new)

            # If the SQL Queries are the same (no updates/changes to the initial SQL query)
            if updated_clause == None:
                messagebox.showerror("showwarning", "SQL Queries are the same, please ensure they are different!")
                self.analysis_text.config(state=DISABLED)

            else:
                added_analysis_text = updated_clause + "\n\n"
                self.analysis_text.config(state="normal")
                self.analysis_text.delete('1.0', END)
                self.analysis_text.insert(END, "Difference in SQL Queries: \n\n", ("title",))
                self.analysis_text.insert(END, added_analysis_text, ("body",))

                # Get Query plans from initial and new SQL queries
                try:
                    initialPlan = preprocessor.get_query_plan(self.initial_query)
                    newPlan = preprocessor.get_query_plan(self.new_query)
                except Exception as e:
                    messagebox.showerror("showwarning", "Please input a working SQL Query!")
                    return

                # Ensuring that previous SQL output table generated has been removed before generating a new table
                for widget in self.sql_output_container_initial.winfo_children():
                    widget.destroy()

                self.initial_button = ttk.Button(self.sql_output_container_initial, text="Generate Table", command=lambda: self.tableTab(self.initial_query, self.sql_output_container_initial), bootstyle="secondary")
                self.initial_button.pack(pady=20, expand=True)

                # Ensuring that previous SQL output table generated has been removed before generating a new table
                for widget in self.sql_output_container_new.winfo_children():
                    widget.destroy()

                self.new_button = ttk.Button(self.sql_output_container_new, text="Generate Table", command=lambda: self.tableTab(self.new_query, self.sql_output_container_new), bootstyle="secondary")
                self.new_button.pack(pady=20, expand=True)

                try:
                    # Generate Graph as images
                    annotator = explain.Annotation(initialPlan)
                    annotator.generate_graph("img/initialPlan")
                    annotator = explain.Annotation(newPlan)
                    annotator.generate_graph("img/newPlan")

                    self.initial_query_plan_text.config(state="normal")
                    self.initial_query_plan_text.delete('1.0', END)
                    
                    # Resize image while maintaining aspect ratio
                    imgInitial = Image.open("img/initialPlan.png")
                    w, h = imgInitial.size
                    ratio = min(self.initial_query_plan_text.winfo_width() / w, self.initial_query_plan_text.winfo_height() / h)
                    new_size = (int(w * ratio), int(h * ratio))
                    imgInitial = imgInitial.resize(new_size)

                    # Insert image for initial query plan
                    self.initial_img = ImageTk.PhotoImage(imgInitial)
                    self.initial_query_plan_text.image_create(END, image=self.initial_img)
                    self.initial_query_plan_text.config(state=DISABLED)

                    self.new_query_plan_text.config(state="normal")
                    self.new_query_plan_text.delete('1.0', END)
                    
                    # Resize images while maintaining aspect ratio
                    imgNew = Image.open("img/newPlan.png")
                    w, h = imgNew.size
                    ratio = min(self.new_query_plan_text.winfo_width() / w, self.new_query_plan_text.winfo_height() / h)
                    new_size = (int(w * ratio), int(h * ratio))
                    imgNew = imgNew.resize(new_size)

                    # Insert image for new query plan
                    self.new_img = ImageTk.PhotoImage(imgNew)
                    self.new_query_plan_text.image_create(END, image=self.new_img)
                    self.new_query_plan_text.config(state=DISABLED)

                    if initialPlan == newPlan:
                        pass

                    else:
                        searchFunction = explain.SearchNode()

                        # Get all Initial Query Joins and Relations
                        self.analysis_text.config(state="normal")
                        self.analysis_text.insert(END, "In the Initial Query:\n", ("title",))
                        joinResults, scanResults = searchFunction.searchJoin(initialPlan)
                        initialJoinString = self.printJoin(joinResults, scanResults, self.analysis_text)

                        # Get all New Query Joins and Relations
                        self.analysis_text.insert(END, "\nIn the New Query:\n", ("title",))
                        joinResults, scanResults = searchFunction.searchJoin(newPlan)
                        newJoinString = self.printJoin(joinResults, scanResults, self.analysis_text)

                        # If the inital join string is the same as the new join string, remove it
                        if initialJoinString == newJoinString:
                            self.analysis_text.delete('1.0', END)
                            self.analysis_text.insert(END, "Difference in SQL Queries: \n\n", ("title",))
                            self.analysis_text.insert(END, added_analysis_text, ("body",))

                    # Get cost of both plans and compare them
                    costFunction = explain.CalculateCost()
                    costString = costFunction.printCost(initialPlan, newPlan)
                    self.analysis_text.insert(END, "\nTotal Cost Comparison:\n\n", ("title",))
                    self.analysis_text.insert(END, costString, ("body",))
                    self.analysis_text.tag_configure("title", font=title_font, underline=True)
                    self.analysis_text.tag_configure("body", font=body_font)
                    self.analysis_text.config(state=DISABLED)

                except Exception as e:
                    messagebox.showerror("showwarning", "Both Queries are the same!")

    def printJoin(self, join_dict, scan_dict, container):
        '''
         Prints out the joins in a query.
         
         Args:
         	 join_dict: Dictionary with the joins as keys and the relation as values
         	 scan_dict: Dictionary with the relations as keys and the relation as values
         	 container: Container to insert the relations into.
         
         Returns: 
         	 The string that is displayed in the Analysis tab
        '''
        listToReturn = []
        body_font = font.Font(family="Helvetica", size=12)
        container.config(state="normal")

        # Concatenating the strings together
        for join in join_dict:
            try:
                joinString = f"\n{join[:-1]} was used between '{join_dict[join][0]}'({scan_dict[join_dict[join][0]]}) and '{join_dict[join][1]}'({scan_dict[join_dict[join][1]]})\n"
                listToReturn.append(joinString)
                container.insert(END, joinString, ("body",))
            except Exception as e:
                try:
                    joinString = f"\n{join[:-1]} was used between '{join_dict[join][0]}'({scan_dict[join_dict[join][0]]}) and '{join_dict[join][1]}'\n"
                    listToReturn.append(joinString)
                    container.insert(END, joinString, ("body",))

                except Exception as e:
                    joinString = f"\n{join[:-1]} was used between '{join_dict[join][0]}' and '{join_dict[join][1]}'\n"
                    listToReturn.append(joinString)
                    container.insert(END, joinString, ("body",))

        self.analysis_text.tag_configure("body", font=body_font)
        return listToReturn

    def createTableOutput(self, output, columns, container):
        '''
         Create table with output from get_query_results. 
         
         Args:
         	 output: List of rows of data
         	 columns: List of column headers to be displayed in table
         	 container: Container to insert the created table into
        '''

        column_data, row_data = [], []

        # Add a header column to the columnData
        for header in columns:
            header_column = {"text": f"{header}", "stretch": True}
            column_data.append(header_column)

        # Append the output to rowData
        for row in output:
            row_data.append(row)

        # Create table view
        table = Tableview(
            master=container,
            coldata=column_data,
            rowdata=row_data,
            autoalign=True,
            autofit=True,
            paginated=True,
            pagesize=40,
            searchable=True,
            stripecolor=(None, None)
        )

        table.pack(padx=10, pady=10, expand=True, fill=BOTH)

    def tableTab(self, query, container):
        '''
        Create table based on query. 
        
        Args:
            query: The query to use for the execution. It can be a string or a list of strings.
            container: The container that will contain the table. This container must be a tab
        '''

        # Clear SQL queries in container
        for child in container.winfo_children():
            child.destroy()  # Clean up sql output
        preprocessor = explain.Preprocessing(self.configList)

        output, columns = preprocessor.get_query_results(query)

        # Create table in container
        if (output is None or (len(output) == 0)):
            ttk.Label(container, text="No results matching the query provided.", font=FONT_BOLD, anchor=CENTER, background="#2C3143", foreground='white').pack(pady=20, fill=tk.X)

        else:
            self.createTableOutput(output, columns, container)
