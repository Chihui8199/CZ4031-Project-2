import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as ttk
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
        self.sql_container = ttk.Frame(self.window_container_left,borderwidth=0)
        self.sql_container.pack(fill=tk.BOTH)

        my_label = Label(self.sql_container, text="Initial Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(pady=20)

        queries_selection = ["Query 1","Query 2","Query 3", "Query 4","Query 5","Query 6", "Query 7"]
        value = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.sql_container, value, queries_selection[0], *queries_selection)
        self.example_query.pack()

        my_text = Text(self.sql_container, width=70, height=10)
        my_text.pack(pady=10, padx=10)



        # New Query ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        my_label = Label(self.sql_container, text="New Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(pady=20)

        queries_selection = ["Query 1","Query 2","Query 3", "Query 4","Query 5","Query 6", "Query 7"]
        value = tk.StringVar()
        self.example_query = ttk.OptionMenu(self.sql_container, value, queries_selection[0], *queries_selection)
        self.example_query.pack()

        my_text = Text(self.sql_container, width=70, height=10)
        my_text.pack(pady=10, padx=10)

        my_button = ttk.Button (self.sql_container, text="Submit", bootstyle="secondary")
        my_button.pack(pady=20)

        
        
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
        
        my_label = Label(self.query_container, text="Initial Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')        
        my_label.pack(pady=20)
        my_text = Text(self.query_container, width=70, height=10)
        my_text.pack(pady=10, padx=10)

        my_label = Label(self.query_container, text="New Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')        
        my_label.pack(pady=20)
        my_text = Text(self.query_container, width=70, height=10)
        my_text.pack(pady=10, padx=10)


        # Analysis Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.analysis_container = ttk.Frame(self.tabs_holders,borderwidth=0)
        self.analysis_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.analysis_container, text="Analysis")

        my_label = Label(self.analysis_container, text="Initial Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(pady=20)
        my_text = Text(self.analysis_container, width=70, height=10)
        my_text.pack(pady=10, padx=10)


        my_label = Label(self.analysis_container, text="New Query:", font=("Helvetica", 18))
        my_label.configure(background='#2C3143', foreground='white')
        my_label.pack(pady=20)
        my_text = Text(self.analysis_container, width=70, height=10)
        my_text.pack(pady=[10,80], padx=10)


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


