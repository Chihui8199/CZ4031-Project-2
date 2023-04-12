import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import string
from tkinter.tix import IMAGETEXT
import ttkbootstrap as ttk
from explain import *
import explain 
from PIL import ImageTk, Image, ImageFilter
from ttkbootstrap.tableview import Tableview
import traceback

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
        # TODO: uncomment this to set application icon (currently not working)
        # self.favicon_ico_path = 'img/cool.ico'
        # self.icon_photo = ImageTk.PhotoImage(
        # Image.open(self.favicon_ico_path))
        # self.iconphoto(False, self.icon_photo)

    
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

        
        self.login_window = Toplevel(self.window_container)
        self.login_window.title("Login")
        self.login_window.geometry("400x300")

        # Create a background image
        # background_image = Image.open("img/background.png")
        # background_photo = ImageTk.PhotoImage(background_image)
        # background_canvas = Canvas(self.window_container, width=self.window_container.winfo_width(), height=self.window_container.winfo_height())
        # background_canvas.pack()
        # background_canvas.create_image(0, 0, image=background_photo, anchor=NW)

        
        # # Apply a blur effect to the parent window
        # self.blur_effect = Image.open("img/background.png").filter(ImageFilter.GaussianBlur(10))
        # self.blur_photo = ImageTk.PhotoImage(self.blur_effect)
        # self.parent_canvas = Canvas(self.window_container, width=self.window_container.winfo_width(), height=self.window_container.winfo_height())
        # self.parent_canvas.pack()
        # self.parent_canvas.create_image(0, 0, image=self.blur_photo, anchor=NW)
        
        # Create the login form
        self.host_label = ttk.Label(self.login_window, text="Host:")
        self.host_entry = ttk.Entry(self.login_window)
        self.host_entry.insert(0,"localhost")

        self.port_label = ttk.Label(self.login_window, text="Port:")
        self.port_entry = ttk.Entry(self.login_window)
        self.port_entry.insert(0,'5432')

        self.database_label = ttk.Label(self.login_window, text="Database:")
        self.database_entry = ttk.Entry(self.login_window)
        self.database_entry.insert(0,'cz4031')

        self.user_label = ttk.Label(self.login_window, text="User:")
        self.user_entry = ttk.Entry(self.login_window)
        self.user_entry.insert(0,'postgres')
        
        self.password_label = ttk.Label(self.login_window, text="Password:")
        self.password_entry = ttk.Entry(self.login_window, show="*")
        self.password_entry.insert(0,'63632625')

        self.login_button = ttk.Button(self.login_window, text="Login", command=  self.login)
        
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

        
        # print(self.configList)
        # Focus the username entry widget
        self.host_entry.focus_set()
        
        # Bind the <Return> key to the login method
        self.login_window.bind("<Return>", self.login)

    def login(self, event=None):
        self.configList = [self.host_entry.get(),
        self.port_entry.get(),
        self.database_entry.get(),
        self.user_entry.get(),
        self.password_entry.get()]
        try:
            # print("hellosdf", self.configList)
            preprocessor = explain.Preprocessing(self.configList)
            messagebox.showinfo("Login", "You are now logged in!")
            self.login_window.destroy()
            # print("db:",preprocessor)
        except Exception as e:
            print(e)
            messagebox.showinfo("Failed", "Login failed")
        
            # self.login_window.destroy()
            
        # self.parent_canvas.destroy()
        

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
        preprocessor = explain.Preprocessing(self.configList)
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        body_font = font.Font(family="Helvetica", size=14)

        comparing = explain.Comparison()
        updated_clause = comparing.comparing(initial, new)
        
        
        if updated_clause == None:
            messagebox.showerror("showwarning", "SQL Queries are the same, please ensure they are different!")
            self.analysis_text.config(state=DISABLED)

        else:
            added_analysis_text =  updated_clause + "\n\n"
            self.analysis_text.config(state="normal")
            self.analysis_text.delete('1.0', END)
            self.analysis_text.insert(END, "Difference in SQL Queries: \n", ("title",))
            self.analysis_text.insert(END, added_analysis_text, ("body",))

            # Get Query plans from user input
            try:
                initialPlan = preprocessor.get_query_plan(self.initial_query)
                newPlan = preprocessor.get_query_plan(self.new_query)
            except Exception as e:
                messagebox.showerror("showwarning", "Please input a working SQL Query!")
                return

            for widget in self.sql_output_container_initial.winfo_children():
                widget.destroy()

            self.initial_button = ttk.Button (self.sql_output_container_initial, text="Generate Table", command= lambda: self.tableTab(self.initial_query,self.sql_output_container_initial) , bootstyle="secondary")
            self.initial_button.pack(pady=20,expand=True)           

            for widget in self.sql_output_container_new.winfo_children():
                widget.destroy()

            self.new_button = ttk.Button (self.sql_output_container_new, text="Generate Table", command= lambda: self.tableTab(self.new_query,self.sql_output_container_new) , bootstyle="secondary")
            self.new_button.pack(pady=20,expand=True)
        
            # Get table output
            # self.tableTab(self.initial_query,self.sql_output_container_initial)
            # self.tableTab(self.new_query,self.sql_output_container_new)
            
            try:
                # Generate Graph as images
                annotator = explain.Annotation(initialPlan)
                annotator.generate_graph("img/initialPlan")
                annotator = explain.Annotation(newPlan)
                annotator.generate_graph("img/newPlan")

                # insert images into Text Box
                self.initial_query_plan_text.config(state="normal")
                self.initial_query_plan_text.delete('1.0', END)
                imgInitial = Image.open("img/initialPlan.png")

                # Resize Image
                w, h = imgInitial.size
                ratio = min(self.initial_query_plan_text.winfo_width() / w, self.initial_query_plan_text.winfo_height() / h)
                new_size = (int(w * ratio), int(h * ratio))
                imgInitial = imgInitial.resize(new_size)

                # Insert Image
                self.initial_img = ImageTk.PhotoImage(imgInitial)
                self.initial_query_plan_text.image_create(END, image=self.initial_img)
                self.initial_query_plan_text.config(state=DISABLED)

                self.new_query_plan_text.config(state="normal")
                self.new_query_plan_text.delete('1.0', END)
                imgNew = Image.open("img/newPlan.png")

                # Resize Image
                w, h = imgNew.size
                ratio = min(self.new_query_plan_text.winfo_width() / w, self.new_query_plan_text.winfo_height() / h)
                new_size = (int(w * ratio), int(h * ratio))
                imgNew = imgNew.resize(new_size)

                # Insert Image
                self.new_img = ImageTk.PhotoImage(imgNew)
                self.new_query_plan_text.image_create(END, image=self.new_img)
                self.new_query_plan_text.config(state=DISABLED)

                

                # compare plans
                if initialPlan == newPlan:
                    print('\n\nExecution plans are the same') 
                    self.comparePlan(initialPlan, newPlan, added_analysis_text)
                    self.analysis_text.config(state="normal")
                    # self.analysis_text.delete('1.0', END) 
                    self.analysis_text.insert('1.0', "The SQL Queries have the same query plan!")

                else:
                    
                    # Get all Initial Query Join and Relations relationships
                    self.analysis_text.config(state="normal")
                    self.analysis_text.insert(END, "In the Initial Query:\n", ("title",))
                    initialJoinString = self.searchJoin(initialPlan)

                    # Get all New Query Join and Relations relationships
                    self.analysis_text.insert(END, "\nIn the New Query:\n", ("title",))
                    newJoinString = self.searchJoin(newPlan)
                    
                    # if initialJoinString == newJoinString:
                    #     self.analysis_text.delete('1.0', END)
                    
                # Get cost of both plans and compare them
                costFunction = explain.CalculateCost()
                costString = costFunction.printCost(initialPlan,newPlan)
                self.analysis_text.insert(END, "\nTotal Cost Comparison:\n\n", ("title",))
                self.analysis_text.insert(END, costString, ("body",))
                self.analysis_text.tag_configure("title", font=title_font, underline=True)
                self.analysis_text.tag_configure("body", font=body_font)
                self.analysis_text.config(state=DISABLED) 

            except Exception as e:
                traceback.print_exc()
                messagebox.showerror("showwarning", "SQL Query is invalid, please try again!")
                    

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
        dataTable = Tableview(
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
        dataTable.pack(padx=10, pady=10, fill=BOTH, expand=TRUE)

    def tableTab(self,query, container):

        print("\n\n\n\nIM IN TABLE TABBBBBB*********************************************\n\n\n\n")
        for child in container.winfo_children():
            child.destroy() # Clean up sql output
        preprocessor = explain.Preprocessing(self.configList)

        actual_output, column_names  = preprocessor.get_query_results(query)

        if (actual_output is None or (len(actual_output) == 0)):
            self.no_results = ttk.Label(container, text="No results matching the query provided.", font=FONT_BOLD, anchor=CENTER, background="#2C3143", foreground='white')
            self.no_results.pack(fill=tk.X, pady=[30,30])
            
        else:
            self.createTableOutput(actual_output, column_names, container) 



    

    
