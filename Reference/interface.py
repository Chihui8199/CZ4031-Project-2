"""
Contains code for GUI
"""
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import *
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from ttkbootstrap.icons import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from tkinter import font, messagebox
from ttkbootstrap.tableview import Tableview
import colorama
from colorama import Fore, Back, Style
import psycopg2
import sqlparse


#logger.py
colorama.init(autoreset=True)  # auto reset color back to default after printing

INFO = "INFO"
SUCCESS = "SUCCESS"
WARNING = "WARNING"
ERROR = "ERROR"


def log(type, message):
    if (type.upper() == INFO):
        print(f'{Fore.CYAN}{Style.BRIGHT}[INFO] {message}')
    elif (type.upper() == WARNING):
        print(f'{Fore.YELLOW}{Style.BRIGHT}[WARNING] {message}')
    elif (type.upper() == SUCCESS):
        print(f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[SUCCESS] {message}')
    elif (type.upper() == ERROR):
        print(f'{Fore.RED}{Style.BRIGHT}[ERROR] {message}')
    else:
        raise InvalidLogTypeException()


class InvalidLogTypeException(Exception):
    """
    Raised when unsupported log type is provided
    """

    def __init__(self, msg='Invalid Log Type provided', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

#node_types.py
# A complete list of node types to be returned from PostgresSQL query plan
NODE_TYPES = ['LIMIT', 'SORT', 'NESTED LOOP', 'MERGE JOIN', 'HASH', 'HASH JOIN', 'AGGREGATE', 'HASHAGGREGATE',
              'SEQ SCAN', 'INDEX SCAN', 'INDEX ONLY SCAN', 'BITMAP HEAP SCAN', 'BITMAP INDEX SCAN', 'CTE SCAN']

NODE_TYPES_CATEGORY_SCAN = 'SCAN'
NODE_TYPES_CATEGORY_JOIN = 'JOIN'

NODE_TYPES_CATEGORY_MAPPING = {
    # JOINS
    NODE_TYPES_CATEGORY_JOIN: ["NESTED LOOP", "MERGE JOIN", 'HASH JOIN'],
    NODE_TYPES_CATEGORY_SCAN: ['SEQ SCAN', 'INDEX SCAN', 'INDEX ONLY SCAN', 'BITMAP HEAP SCAN', 'BITMAP INDEX SCAN',
                               'CTE_SCAN']

}

# PLANNER CONFIGURATION MAPPING:
CONSTRAINT_ENABLE_ASYNC_APPEND = "ENABLE_ASYNC_APPEND"
CONSTRAINT_ENABLE_BITMAPSCAN = "ENABLE_BITMAPSCAN"
CONSTRAINT_ENABLE_GATHERMERGE = "ENABLE_GATHERMERGE"
CONSTRAINT_ENABLE_HASHAGG = "ENABLE_HASHAGG"
CONSTRAINT_ENABLE_HASHJOIN = "ENABLE_HASHJOIN"
CONSTRAINT_ENABLE_INCREMENTAL_SORT = "ENABLE_INCREMENTAL_SORT"
CONSTRAINT_ENABLE_INDEXSCAN = "ENABLE_INDEXSCAN"
CONSTRAINT_ENABLE_INDEXONLYSCAN = "ENABLE_INDEXONLYSCAN"
CONSTRAINT_ENABLE_MATERIAL = "ENABLE_MATERIAL"
CONSTRAINT_ENABLE_MEMOIZE = "ENABLE_MEMOIZE"
CONSTRAINT_ENABLE_MERGEJOIN = "ENABLE_MERGEJOIN"
CONSTRAINT_ENABLE_NESTLOOP = "ENABLE_NESTLOOP"
CONSTRAINT_ENABLE_PARALLEL_APPEND = "ENABLE_PARALLEL_APPEND"
CONSTRAINT_ENABLE_PARALLEL_HASH = "ENABLE_PARALLEL_HASH"
CONSTRAINT_ENABLE_PARTITION_PRUNING = "ENABLE_PARTITION_PRUNING"
CONSTRAINT_ENABLE_PARTITIONWISE_JOIN = "ENABLE_PARTITIONWISE_JOIN"
CONSTRAINT_ENABLE_PARTITIONWISE_AGGREGATE = "ENABLE_PARTITIONWISE_AGGREGATE"
CONSTRAINT_ENABLE_SEQSCAN = "ENABLE_SEQSCAN"
CONSTRAINT_ENABLE_SORT = "ENABLE_SORT"
CONSTRAINT_ENABLE_TIDSCAN = "ENABLE_TIDSCAN"

NODE_TYPES_CONSTRAINTS_MAPPING = {
    # JOINS
    'NESTED LOOP': CONSTRAINT_ENABLE_NESTLOOP,
    'MERGE JOIN': CONSTRAINT_ENABLE_MERGEJOIN,
    'HASH JOIN': CONSTRAINT_ENABLE_HASHJOIN,

    # SCANS
    'SEQ SCAN': CONSTRAINT_ENABLE_SEQSCAN,
    'INDEX SCAN': CONSTRAINT_ENABLE_INDEXSCAN,
    'INDEX ONLY SCAN': CONSTRAINT_ENABLE_INDEXONLYSCAN,
    'BITMAP HEAP SCAN': CONSTRAINT_ENABLE_BITMAPSCAN,
    'BITMAP INDEX SCAN': CONSTRAINT_ENABLE_BITMAPSCAN,
}

# Key attribute in a node that will help to identify which SQL query correspond to this node
KEY_PROPERTY = {'LIMIT': ['Plan Rows'], 'SORT': ['Sort Key'], 'NESTED LOOP': [], 'MERGE JOIN': ['Merge Cond'],
                'HASH': [], 'HASH JOIN': ['Hash Cond'], 'AGGREGATE': ['Group Key'], 'HASHAGGREGATE': ['Group Key'],
                'SEQ SCAN': ['Relation Name', 'Filter'], 'INDEX SCAN': ['Index Cond', 'Filter'],
                'INDEX ONLY SCAN': ['Index Cond', 'Filter', 'Alias'],
                'BITMAP HEAP SCAN': ['Recheck Cond', 'Filter', 'Alias'],
                'BITMAP INDEX SCAN': ['Index Cond', 'Filter', 'Alias'],
                'CTE SCAN': ['Index Cond', 'Filter', 'Alias']}

# Used for visualization
ATTRIBUTE = {'LIMIT': ['Plan Rows'], 'SORT': ['Sort Method', 'Sort Key'], 'NESTED LOOP': [],
             'MERGE JOIN': ['Merge Cond'],
             'HASH': ['Output'], 'HASH JOIN': ['Hash Cond', 'Output'], 'AGGREGATE': ['Group Key'],
             'HASHAGGREGATE': ['Group Key'],
             'SEQ SCAN': ['Relation Name'], 'INDEX SCAN': ['Index Cond'], 'GATHER MERGE': ['Output'],
             'INDEX ONLY SCAN': ['Index Cond', 'Index Name', 'Relation Name'], 'BITMAP HEAP SCAN': ['Recheck Cond'],
             'BITMAP INDEX SCAN': ['Index Cond'], 'CTE SCAN': ['Index Cond']}

# A complete list of keywords in Postgresql
KEYWORDS = ['A', 'ABORT', 'ABS', 'ABSENT', 'ABSOLUTE', 'ACCESS', 'ACCORDING', 'ACTION', 'ADA', 'ADD', 'ADMIN',
            'AFTER', 'AGGREGATE', 'ALL', 'ALLOCATE', 'ALSO', 'ALTER', 'ALWAYS', 'ANALYSE', 'ANALYZE', 'AND', 'ANY',
            'ARE', 'ARRAY', 'ARRAY_AGG', 'ARRAY_MAX_CARDINALITY', 'AS', 'ASC', 'ASENSITIVE', 'ASSERTION',
            'ASSIGNMENT', 'ASYMMETRIC', 'AT', 'ATOMIC', 'ATTACH', 'ATTRIBUTE', 'ATTRIBUTES', 'AUTHORIZATION',
            'AVG', 'BACKWARD', 'BASE64', 'BEFORE', 'BEGIN', 'BEGIN_FRAME', 'BEGIN_PARTITION', 'BERNOULLI',
            'BETWEEN', 'BIGINT', 'BINARY', 'BIT', 'BIT_LENGTH', 'BLOB', 'BLOCKED', 'BOM', 'BOOLEAN', 'BOTH',
            'BREADTH', 'BY', 'C', 'CACHE', 'CALL', 'CALLED', 'CARDINALITY', 'CASCADE', 'CASCADED', 'CASE', 'CAST',
            'CATALOG', 'CATALOG_NAME', 'CEIL', 'CEILING', 'CHAIN', 'CHAR', 'CHARACTER', 'CHARACTERISTICS',
            'CHARACTERS', 'CHARACTER_LENGTH', 'CHARACTER_SET_CATALOG', 'CHARACTER_SET_NAME',
            'CHARACTER_SET_SCHEMA', 'CHAR_LENGTH', 'CHECK', 'CHECKPOINT', 'CLASS', 'CLASS_ORIGIN', 'CLOB', 'CLOSE',
            'CLUSTER', 'COALESCE', 'COBOL', 'COLLATE', 'COLLATION', 'COLLATION_CATALOG', 'COLLATION_NAME',
            'COLLATION_SCHEMA', 'COLLECT', 'COLUMN', 'COLUMNS', 'COLUMN_NAME', 'COMMAND_FUNCTION',
            'COMMAND_FUNCTION_CODE', 'COMMENT', 'COMMENTS', 'COMMIT', 'COMMITTED', 'CONCURRENTLY', 'CONDITION',
            'CONDITION_NUMBER', 'CONFIGURATION', 'CONFLICT', 'CONNECT', 'CONNECTION', 'CONNECTION_NAME',
            'CONSTRAINT', 'CONSTRAINTS', 'CONSTRAINT_CATALOG', 'CONSTRAINT_NAME', 'CONSTRAINT_SCHEMA',
            'CONSTRUCTOR', 'CONTAINS', 'CONTENT', 'CONTINUE', 'CONTROL', 'CONVERSION', 'CONVERT', 'COPY', 'CORR',
            'CORRESPONDING', 'COST', 'COUNT', 'COVAR_POP', 'COVAR_SAMP', 'CREATE', 'CROSS', 'CSV', 'CUBE',
            'CUME_DIST', 'CURRENT', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_DEFAULT_TRANSFORM_GROUP',
            'CURRENT_PATH', 'CURRENT_ROLE', 'CURRENT_ROW', 'CURRENT_SCHEMA', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
            'CURRENT_TRANSFORM_GROUP_FOR_TYPE', 'CURRENT_USER', 'CURSOR', 'CURSOR_NAME', 'CYCLE', 'DATA',
            'DATABASE', 'DATALINK', 'DATE', 'DATETIME_INTERVAL_CODE', 'DATETIME_INTERVAL_PRECISION', 'DAY', 'DB',
            'DEALLOCATE', 'DEC', 'DECIMAL', 'DECLARE', 'DEFAULT', 'DEFAULTS', 'DEFERRABLE', 'DEFERRED', 'DEFINED',
            'DEFINER', 'DEGREE', 'DELETE', 'DELIMITER', 'DELIMITERS', 'DENSE_RANK', 'DEPENDS', 'DEPTH', 'DEREF',
            'DERIVED', 'DESC', 'DESCRIBE', 'DESCRIPTOR', 'DETACH', 'DETERMINISTIC', 'DIAGNOSTICS', 'DICTIONARY',
            'DISABLE', 'DISCARD', 'DISCONNECT', 'DISPATCH', 'DISTINCT', 'DLNEWCOPY', 'DLPREVIOUSCOPY',
            'DLURLCOMPLETE', 'DLURLCOMPLETEONLY', 'DLURLCOMPLETEWRITE', 'DLURLPATH', 'DLURLPATHONLY',
            'DLURLPATHWRITE', 'DLURLSCHEME', 'DLURLSERVER', 'DLVALUE', 'DO', 'DOCUMENT', 'DOMAIN', 'DOUBLE',
            'DROP', 'DYNAMIC', 'DYNAMIC_FUNCTION', 'DYNAMIC_FUNCTION_CODE', 'EACH', 'ELEMENT', 'ELSE', 'EMPTY',
            'ENABLE', 'ENCODING', 'ENCRYPTED', 'END', 'END-EXEC', 'END_FRAME', 'END_PARTITION', 'ENFORCED', 'ENUM',
            'EQUALS', 'ESCAPE', 'EVENT', 'EVERY', 'EXCEPT', 'EXCEPTION', 'EXCLUDE', 'EXCLUDING', 'EXCLUSIVE',
            'EXEC', 'EXECUTE', 'EXISTS', 'EXP', 'EXPLAIN', 'EXPRESSION', 'EXTENSION', 'EXTERNAL', 'EXTRACT',
            'FALSE', 'FAMILY', 'FETCH', 'FILE', 'FILTER', 'FINAL', 'FIRST', 'FIRST_VALUE', 'FLAG', 'FLOAT',
            'FLOOR', 'FOLLOWING', 'FOR', 'FORCE', 'FOREIGN', 'FORTRAN', 'FORWARD', 'FOUND', 'FRAME_ROW', 'FREE',
            'FREEZE', 'FROM', 'FS', 'FULL', 'FUNCTION', 'FUNCTIONS', 'FUSION', 'G', 'GENERAL', 'GENERATED', 'GET',
            'GLOBAL', 'GO', 'GOTO', 'GRANT', 'GRANTED', 'GREATEST', 'GROUP', 'GROUPING', 'GROUPS', 'HANDLER',
            'HAVING', 'HEADER', 'HEX', 'HIERARCHY', 'HOLD', 'HOUR', 'ID', 'IDENTITY', 'IF', 'IGNORE', 'ILIKE',
            'IMMEDIATE', 'IMMEDIATELY', 'IMMUTABLE', 'IMPLEMENTATION', 'IMPLICIT', 'IMPORT', 'IN', 'INCLUDING',
            'INCREMENT', 'INDENT', 'INDEX', 'INDEXES', 'INDICATOR', 'INHERIT', 'INHERITS', 'INITIALLY', 'INLINE',
            'INNER', 'INOUT', 'INPUT', 'INSENSITIVE', 'INSERT', 'INSTANCE', 'INSTANTIABLE', 'INSTEAD', 'INT',
            'INTEGER', 'INTEGRITY', 'INTERSECT', 'INTERSECTION', 'INTERVAL', 'INTO', 'INVOKER', 'IS', 'ISNULL',
            'ISOLATION', 'JOIN', 'K', 'KEY', 'KEY_MEMBER', 'KEY_TYPE', 'LABEL', 'LAG', 'LANGUAGE', 'LARGE', 'LAST',
            'LAST_VALUE', 'LATERAL', 'LEAD', 'LEADING', 'LEAKPROOF', 'LEAST', 'LEFT', 'LENGTH', 'LEVEL', 'LIBRARY',
            'LIKE', 'LIKE_REGEX', 'LIMIT', 'LINK', 'LISTEN', 'LN', 'LOAD', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP',
            'LOCATION', 'LOCATOR', 'LOCK', 'LOCKED', 'LOGGED', 'LOWER', 'M', 'MAP', 'MAPPING', 'MATCH', 'MATCHED',
            'MATERIALIZED', 'MAX', 'MAXVALUE', 'MAX_CARDINALITY', 'MEMBER', 'MERGE', 'MESSAGE_LENGTH',
            'MESSAGE_OCTET_LENGTH', 'MESSAGE_TEXT', 'METHOD', 'MIN', 'MINUTE', 'MINVALUE', 'MOD', 'MODE',
            'MODIFIES', 'MODULE', 'MONTH', 'MORE', 'MOVE', 'MULTISET', 'MUMPS', 'NAME', 'NAMES', 'NAMESPACE',
            'NATIONAL', 'NATURAL', 'NCHAR', 'NCLOB', 'NESTING', 'NEW', 'NEXT', 'NFC', 'NFD', 'NFKC', 'NFKD', 'NIL',
            'NO', 'NONE', 'NORMALIZE', 'NORMALIZED', 'NOT', 'NOTHING', 'NOTIFY', 'NOTNULL', 'NOWAIT', 'NTH_VALUE',
            'NTILE', 'NULL', 'NULLABLE', 'NULLIF', 'NULLS', 'NUMBER', 'NUMERIC', 'OBJECT', 'OCCURRENCES_REGEX',
            'OCTETS', 'OCTET_LENGTH', 'OF', 'OFF', 'OFFSET', 'OIDS', 'OLD', 'ON', 'ONLY', 'OPEN', 'OPERATOR',
            'OPTION', 'OPTIONS', 'OR', 'ORDER', 'ORDERING', 'ORDINALITY', 'OTHERS', 'OUT', 'OUTER', 'OUTPUT',
            'OVER', 'OVERLAPS', 'OVERLAY', 'OVERRIDING', 'OWNED', 'OWNER', 'P', 'PAD', 'PARALLEL', 'PARAMETER',
            'PARAMETER_MODE', 'PARAMETER_NAME', 'PARAMETER_ORDINAL_POSITION', 'PARAMETER_SPECIFIC_CATALOG',
            'PARAMETER_SPECIFIC_NAME', 'PARAMETER_SPECIFIC_SCHEMA', 'PARSER', 'PARTIAL', 'PARTITION', 'PASCAL',
            'PASSING', 'PASSTHROUGH', 'PASSWORD', 'PATH', 'PERCENT', 'PERCENTILE_CONT', 'PERCENTILE_DISC',
            'PERCENT_RANK', 'PERIOD', 'PERMISSION', 'PLACING', 'PLANS', 'PLI', 'POLICY', 'PORTION', 'POSITION',
            'POSITION_REGEX', 'POWER', 'PRECEDES', 'PRECEDING', 'PRECISION', 'PREPARE', 'PREPARED', 'PRESERVE',
            'PRIMARY', 'PRIOR', 'PRIVILEGES', 'PROCEDURAL', 'PROCEDURE', 'PROGRAM', 'PUBLIC', 'PUBLICATION',
            'QUOTE', 'RANGE', 'RANK', 'READ', 'READS', 'REAL', 'REASSIGN', 'RECHECK', 'RECOVERY', 'RECURSIVE',
            'REF', 'REFERENCES', 'REFERENCING', 'REFRESH', 'REGR_AVGX', 'REGR_AVGY', 'REGR_COUNT',
            'REGR_INTERCEPT', 'REGR_R2', 'REGR_SLOPE', 'REGR_SXX', 'REGR_SXY', 'REGR_SYY', 'REINDEX', 'RELATIVE',
            'RELEASE', 'RENAME', 'REPEATABLE', 'REPLACE', 'REPLICA', 'REQUIRING', 'RESET', 'RESPECT', 'RESTART',
            'RESTORE', 'RESTRICT', 'RESULT', 'RETURN', 'RETURNED_CARDINALITY', 'RETURNED_LENGTH',
            'RETURNED_OCTET_LENGTH', 'RETURNED_SQLSTATE', 'RETURNING', 'RETURNS', 'REVOKE', 'RIGHT', 'ROLE',
            'ROLLBACK', 'ROLLUP', 'ROUTINE', 'ROUTINE_CATALOG', 'ROUTINE_NAME', 'ROUTINE_SCHEMA', 'ROW', 'ROWS',
            'ROW_COUNT', 'ROW_NUMBER', 'RULE', 'SAVEPOINT', 'SCALE', 'SCHEMA', 'SCHEMAS', 'SCHEMA_NAME', 'SCOPE',
            'SCOPE_CATALOG', 'SCOPE_NAME', 'SCOPE_SCHEMA', 'SCROLL', 'SEARCH', 'SECOND', 'SECTION', 'SECURITY',
            'SELECT', 'SELECTIVE', 'SELF', 'SENSITIVE', 'SEQUENCE', 'SEQUENCES', 'SERIALIZABLE', 'SERVER',
            'SERVER_NAME', 'SESSION', 'SESSION_USER', 'SET', 'SETOF', 'SETS', 'SHARE', 'SHOW', 'SIMILAR', 'SIMPLE',
            'SIZE', 'SKIP', 'SMALLINT', 'SNAPSHOT', 'SOME', 'SOURCE', 'SPACE', 'SPECIFIC', 'SPECIFICTYPE',
            'SPECIFIC_NAME', 'SQL', 'SQLCODE', 'SQLERROR', 'SQLEXCEPTION', 'SQLSTATE', 'SQLWARNING', 'SQRT',
            'STABLE', 'STANDALONE', 'START', 'STATE', 'STATEMENT', 'STATIC', 'STATISTICS', 'STDDEV_POP',
            'STDDEV_SAMP', 'STDIN', 'STDOUT', 'STORAGE', 'STRICT', 'STRIP', 'STRUCTURE', 'STYLE',
            'SUBCLASS_ORIGIN', 'SUBMULTISET', 'SUBSCRIPTION', 'SUBSTRING', 'SUBSTRING_REGEX', 'SUCCEEDS', 'SUM',
            'SYMMETRIC', 'SYSID', 'SYSTEM', 'SYSTEM_TIME', 'SYSTEM_USER', 'T', 'TABLE', 'TABLES', 'TABLESAMPLE',
            'TABLESPACE', 'TABLE_NAME', 'TEMP', 'TEMPLATE', 'TEMPORARY', 'TEXT', 'THEN', 'TIES', 'TIME',
            'TIMESTAMP', 'TIMEZONE_HOUR', 'TIMEZONE_MINUTE', 'TO', 'TOKEN', 'TOP_LEVEL_COUNT', 'TRAILING',
            'TRANSACTION', 'TRANSACTIONS_COMMITTED', 'TRANSACTIONS_ROLLED_BACK', 'TRANSACTION_ACTIVE', 'TRANSFORM',
            'TRANSFORMS', 'TRANSLATE', 'TRANSLATE_REGEX', 'TRANSLATION', 'TREAT', 'TRIGGER', 'TRIGGER_CATALOG',
            'TRIGGER_NAME', 'TRIGGER_SCHEMA', 'TRIM', 'TRIM_ARRAY', 'TRUE', 'TRUNCATE', 'TRUSTED', 'TYPE', 'TYPES',
            'UESCAPE', 'UNBOUNDED', 'UNCOMMITTED', 'UNDER', 'UNENCRYPTED', 'UNION', 'UNIQUE', 'UNKNOWN', 'UNLINK',
            'UNLISTEN', 'UNLOGGED', 'UNNAMED', 'UNNEST', 'UNTIL', 'UNTYPED', 'UPDATE', 'UPPER', 'URI', 'USAGE',
            'USER', 'USER_DEFINED_TYPE_CATALOG', 'USER_DEFINED_TYPE_CODE', 'USER_DEFINED_TYPE_NAME',
            'USER_DEFINED_TYPE_SCHEMA', 'USING', 'VACUUM', 'VALID', 'VALIDATE', 'VALIDATOR', 'VALUE', 'VALUES',
            'VALUE_OF', 'VARBINARY', 'VARCHAR', 'VARIADIC', 'VARYING', 'VAR_POP', 'VAR_SAMP', 'VERBOSE', 'VERSION',
            'VERSIONING', 'VIEW', 'VIEWS', 'VOLATILE', 'WHEN', 'WHENEVER', 'WHERE', 'WHITESPACE', 'WIDTH_BUCKET',
            'WINDOW', 'WITH', 'WITHIN', 'WITHOUT', 'WORK', 'WRAPPER', 'WRITE', 'XML', 'XMLAGG', 'XMLATTRIBUTES',
            'XMLBINARY', 'XMLCAST', 'XMLCOMMENT', 'XMLCONCAT', 'XMLDECLARATION', 'XMLDOCUMENT', 'XMLELEMENT',
            'XMLEXISTS', 'XMLFOREST', 'XMLITERATE', 'XMLNAMESPACES', 'XMLPARSE', 'XMLPI', 'XMLQUERY', 'XMLROOT',
            'XMLSCHEMA', 'XMLSERIALIZE', 'XMLTABLE', 'XMLTEXT', 'XMLVALIDATE', 'YEAR', 'YES', 'ZONE']

COLORS = [
    ('#ff6459', 'black'),
    ('#e91e63', 'black'),
    ('#9c27b0', 'white'),
    ('#673ab7', 'white'),
    ('#3f51b5', 'black'),
    ('#2196f3', 'black'),
    ('#03a9f4', 'black'),
    ('#00bcd4', 'black'),
    ('#009688', 'black'),
    ('#47d34d', 'black'),
    ('#8bc34a', 'black'),
    ('#cddc39', 'black'),
    ('#ffeb3b', 'black'),
    ('#ffc107', 'black')
]

NODE_COLORS = {node_type: color
               for node_type, color in zip(NODE_TYPES, COLORS)}


#config.py
# DATABASE CONNECTIONS
DATABASE_NAME = "cz4031"
DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "63632625"
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 5432

# FONT SETTINGS
FONT = "Arial"
BOLD = "BOLD"
ITALIC = "ITALIC"
UNDERLINE = "UNDERLINE"
FONT_REGULAR = (FONT, 12)
FONT_BOLD = (f"{FONT} {BOLD}", 12)
FONT_TITLE = (f"{FONT} {BOLD}", 16)
FONT_CREDITS = (f"{FONT} {ITALIC}", 10)

# APP THEME (REFER TO TTKBOOTSTRAP). LEAVETHE ONE YOU WANT TO USE UNCOMMENTEd
## DARK THEMES
# THEME="solar"
THEME="superhero"
# THEME="darkly"
# THEME="cyborg"
# THEME="vapor"
## LIGHT THEMES
# THEME="cosmo"
# THEME="flatly"
# THEME="journal"
# THEME="litera"
# THEME="lumen"
# THEME="minty"
# THEME="pulse"
# THEME="sandstone"
# THEME="united"
# THEME="yeti"
# THEME="morph"
# THEME="simplex"
# THEME="cerculean"

#interface.py
class QEPAnalyzer(ttk.Window):
    """
    A Query Exceution Plan (QEP) analyzer created. Given a SQL input, it communicates with the database to get QEP and Alternative Query Execution Plan using constraints under POSTGRES.

    After that it will try to compare whereever applicable in order to do a analysis of why the QEP decided is better than the rest.
    """

    def __init__(self, preprocessor, annotator, *args, **kwargs):   
        kwargs["themename"] = THEME
        ttk.Window.__init__(self, *args, **kwargs)
        
        # Link other necessary classess
        self.preprocessor = preprocessor
        self.annotator = annotator

        # Connect to database.
        self.connect_to_database()
        
        # Initialize application level settings
        self.title("CZ4031 QEP Analyzer")
        self.geometry("1400x800")
        self.option_add("*Font", FONT_REGULAR)
        self.favicon_ico_path = 'Reference/database.ico'
        self.icon_photo = ImageTk.PhotoImage(
            Image.open(self.favicon_ico_path))
        self.iconphoto(False, self.icon_photo)

        # Initialize tracking variables that will be used by the appliaction.
        self.query_option_tracker_sql_output = IntVar(self, value=0) # Tracks if we should output the actual SQL or just do a normal analysis.

        # Generate UI
        self.generate_UI()

    def generate_UI(self):
        """
        Generate the main UI screen for most user interactions.
        """

        self.window_container = ttk.Frame(self)
        self.window_container.pack(fill=tk.BOTH)

        self.app_label = ttk.Label(self.window_container, text="CZ4031 QEP Analyzer (2022)", font=FONT_TITLE, anchor=CENTER)
        self.app_label.pack(fill=tk.X, pady=[10,0])

        self.creators_label = ttk.Label(self.window_container, text="By Group 14: Qi Wei, Kong Tat, Ryan, Xing Kun, Lyndon", font=FONT_CREDITS, anchor=CENTER)
        self.creators_label.pack(fill=tk.X)

    
        # Add tab holders and tabs
        self.tabs_holders = ttk.Notebook(self.window_container, bootstyle=SUCCESS)
        self.tabs_holders.pack(fill=tk.BOTH, padx=10, pady=10)

        self.query_container = ttk.Frame(self.tabs_holders)
        self.query_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.query_container, text="Query")

        self.tree_output_container = ttk.Frame(self.tabs_holders)
        self.tree_output_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.tree_output_container, text="Analysis Results")

        self.sql_output_container = ttk.Frame(self.tabs_holders)
        self.sql_output_container.pack(fill=tk.BOTH)
        self.tabs_holders.add(self.sql_output_container, text="SQL Output (if applicable)")

        # Create frame for user input
        self.instruction_label = ttk.Label(self.query_container, text="Enter your sql query below and click button to analyze (or use shortcut: F5 key)", font=FONT_BOLD)
        self.query_entry = ScrolledText(master=self.query_container, autohide=True)
        self.analyze_btn = ttk.Button(self.query_container, text="ANALYZE QUERY", command=self.analyze_query, bootstyle=PRIMARY)
        # Bind query entry to F5 Shortcut key
        self.bind_all("<F5>", self.analyze_query)
        self.query_option = ttk.Checkbutton(self.query_container, text="Return SQL output with analysis", variable=self.query_option_tracker_sql_output, onvalue=1, offvalue=0)
        # Pack all elements for user input
        self.instruction_label.pack(fill=tk.X, padx=20, pady=10)
        self.query_entry.pack(fill=tk.BOTH,padx=20, pady=10)
        self.query_option.pack(side=tk.LEFT, padx=20, pady=10)
        self.analyze_btn.pack(side=tk.RIGHT, fill=tk.X, padx=20, pady=10)
        
        # Create frame for tree output
        self.left_annotated_sql_frame = ttk.Frame(self.tree_output_container)
        self.left_annotated_sql_query_display = ScrolledText(master=self.left_annotated_sql_frame, autohide=True, state=DISABLED)
        self.left_annotated_sql_analysis_display = ScrolledText(master=self.left_annotated_sql_frame, autohide=True, state=DISABLED)
        self.right_tree_frame = ttk.Frame(self.tree_output_container)
        self.qep_tooltip = ttk.Label(self.right_tree_frame, text="Click on or hover over the nodes to view analysis information.", font=FONT_BOLD)
        self.qep_tree =  QEPTreeVisualizer(self.right_tree_frame, self.left_annotated_sql_query_display, self.left_annotated_sql_analysis_display)
        # Pack all elements for tree output
        self.left_annotated_sql_frame.pack(side=LEFT) 
        self.left_annotated_sql_query_display.pack(side=tk.TOP, fill=tk.X)
        self.left_annotated_sql_analysis_display.pack(side=tk.BOTTOM,fill=tk.X)
        self.right_tree_frame.pack(side=LEFT, padx=20, fill=tk.BOTH) 
        self.qep_tooltip.pack(fill=tk.X, pady=5, side=TOP)
        self.qep_tree.pack(fill=tk.X, padx=20, anchor=CENTER)
        
        # Add default labels
        ttk.Label(self.sql_output_container, text = "Please select option to display SQL output in [Query] tab.", font=FONT_BOLD).pack(fill=tk.X, padx=20, pady=10, anchor=CENTER)
        for node_type, color in NODE_COLORS.items():
            self.left_annotated_sql_query_display.text.tag_configure(node_type, background=color[0], foreground=color[1])
        self.left_annotated_sql_query_display.text.tag_configure('OTHER', background='#ff9800', foreground='black')

    
    def get_image(self, path, size = (100, 100)):
        """
        Returns the image from the current path with the specified size
        """
        return ImageTk.PhotoImage(Image.open(path).resize(size))


    def connect_to_database(self):
        """
        Connects to database
        """
        log(INFO, f"Trying to connect to database [{DATABASE_NAME}] at {DATABASE_HOST}:{DATABASE_PORT}")
        try:
            print(DATABASE_NAME,DATABASE_USERNAME,DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)
            self.conn = psycopg2.connect(
                dbname=DATABASE_NAME,
                user=DATABASE_USERNAME,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT
            )
            log(SUCCESS, (f"Database connection established as [{DATABASE_USERNAME}] successfully to database [{DATABASE_NAME}] at {DATABASE_HOST}:{DATABASE_PORT}"))


        except:
            # Connection issues
            log(ERROR, ("There was something wrong with your database connection. Please check your settins and try again!"))
            exit()  
          

    def analyze_query(self, binded = None):
        """
        Starts the whole analysis process of the given query.

        Trigger: By button click or shortcut key [F5]
        """
        if binded is not None:
            print("Trigger by binded button")

        # Disable button to prevent spamming
        self.analyze_btn.configure(state=DISABLED)

        # Get query from user input and clean query
        self.query = self.query_entry.get('1.0', 'end-1c')
        self.query = self.query.strip()
        self.query = self.query.replace('\n', ' ')
        self.query = sqlparse.format(self.query, reindent=True, keyword_case='upper')        

        # Check if we should print out the actual output (Determined by checkbox)
        # If not add helpful messages to indicate
        return_sql_output = self.query_option_tracker_sql_output.get()
        for child in self.sql_output_container.winfo_children():
            child.destroy() # Clean up sql output
        if (return_sql_output):
            # Send execute the STANDARD query (no analysis)
            actual_output = self.execute_query(self.query, run_explain=False)
            if (actual_output is None):
                self.analyze_btn.configure(state=ACTIVE)
                return
            elif (len(actual_output) == 0):
                ttk.Label(self.sql_output_container, text = "No results matching.", font=FONT_BOLD).pack(fill=tk.X, padx=20, pady=10, anchor=CENTER)
            else:
                self.create_table_view(actual_output) 


        # Send execute the EXPLAIN query
        query_results = self.execute_query(self.query, run_explain=True)
        if (query_results is None):
            self.analyze_btn.configure(state=ACTIVE)
            return


        ## FROM THIS POINT ON: ONLY PROCEED IF THE SQL QUERY IS VALID

        # SQL Annotation Frame - Insert the sql query into the UI. DISALBED is used to keep the frame as "readonly"
        self.left_annotated_sql_query_display.text.configure(state=NORMAL)
        self.left_annotated_sql_query_display.delete('1.0', END)
        self.left_annotated_sql_query_display.insert(END, self.query)
        self.left_annotated_sql_query_display.text.configure(state=DISABLED)

        # Get QEP in the form of JSON data and build the annotated tree
        json_data = self.preprocessor.get_json(query_results)
        # Build build data structure
        root_node = self.annotator.build_tree([json_data['Plan']])[0]


        # Process the whole QEP and get the various operations used.
        node_category_output_mapping_list = self.annotator.build_node_category_output_mapping(root_node) # Get the node_type_output_mapping_dict
        print("MAPPING! =>")
        print(node_category_output_mapping_list)
        constraints = self.preprocessor.get_planner_method_configuration_constraints(root_node)
        for constraint in constraints:
            print(f"Current Constraint => {constraint}")
            aqp_output = self.get_aqp(self.query, constraint)
            if (aqp_output is not None):
                aqp_json_data = self.preprocessor.get_json(aqp_output)
                aqp_root_node = self.annotator.build_tree([aqp_json_data['Plan']])[0]
                result = self.annotator.add_aqp_analysis_to_qep(root_node, aqp_root_node, node_category_output_mapping_list, constraint) # update the output mapping after adding aqp    
                if (result != None):
                    root_node, node_category_output_mapping_list = result
        self.reset_aqp_constraints()

        # Assign some constraint and loop through, each time disabling one only 
        # Then get the results and append it to the node appropriately (need check the structure)
        
        # We won't show the alternative query plan since we only show one constraint at a time.


        # SQL Annotation Frame - Prepare index mapping to match query text
        sql_query_character_map = self.preprocessor.prepare_highlighting_sql_query_character_map(self.query)
        token_matcher_dict = self.annotator.build_invert_relation(self.query, root_node)
        self.qep_tree.set_query_reference(self.query) # Updates the query in the qep tree
        self.qep_tree.set_sql_query_character_map(sql_query_character_map) # Updates the character mapping used in the qep tree
        self.qep_tree.set_token_matcher_dict(token_matcher_dict) # Updates the token matcher
        # Draw the QEP tree
        self.qep_tree.draw_tree(root_node)
        
        # Re-enable button & change focus to output tabs
        self.analyze_btn.configure(state=ACTIVE)
        self.tabs_holders.select(self.tree_output_container)
        
    def reset_aqp_constraints(self):
        """
        Manually reset aqp constraint manually. This is required to for cleaning up any constraints set.
        """
        reset_query = "RESET ALL;"
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    print("Resetting")
                    curs.execute(reset_query)
                    # result = curs.fetchall()
                except:
                    Messagebox.show_warning(
                        message = "AQP Reset Query failed. Please check your query and try again.",
                        title="Invalid SQL Query",
                        parent=self,
                    )
                    return None


    def get_aqp(self, query, constraint):
        """
        Gets the alternative query plans by setting constraint

        constraint: The flag to set in the database
        """
        constraint = constraint.upper()
        if "EXPLAIN" not in query:
                query = f"EXPLAIN (ANALYZE FALSE, VERBOSE, FORMAT JSON) {query};"
        aqp_query = f"""
        RESET ALL;
        SET {constraint} TO OFF;
        {query}
        """
        print(f"AQP QUERY {aqp_query}")
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(aqp_query)
                    result = curs.fetchall()
                    return result
                except:
                    Messagebox.show_warning(
                        message = "AQP Query failed. Please check your query and try again.",
                        title="Invalid SQL Query",
                        parent=self,
                    )
                    return None
    
    def create_table_view(self, output):
        """
        Used to create a table view for the sql output. Extracts the row and column information
        """
        # Get columns in output
        first_row_json = output[0][0]
        column_names = [key for key in first_row_json.keys()]
        
        # Prepare column data
        coldata = []
        for name in column_names:
            header_column = {"text": f"{name}", "stretch": True}
            coldata.append(header_column)
        
        # Prepare row data
        rowdata = []
        for row in output:
            current_row_json = row[0]
            current_row_data = []
            for val in current_row_json.values():
                current_row_data.append(val)
            rowdata.append(current_row_data)

        # Create table view
        dt = Tableview(
            master=self.sql_output_container,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            pagesize=50,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(None, None),
        )
        dt.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

    
    def execute_query(self, query, run_explain = True):
        """
        Gets a cursor using the connection to the database and executes a given query.

        run_explain: This is a flag to determine if we should run a analysis to get the QEP or run the sql output to get the actual results. 

        Reason for this is to have a single method to parse all the process the query and return the output we desired (actual sql output & estiamted plans.)
        """
        if (query.strip() == ''):
            Messagebox.show_warning(
                message = "Please enter a query first!",
                title="Invalid SQL Query",
                parent=self,
            )
            self.query_entry.focus()
            return None

        if (run_explain == False):
            # Remove the ; since we using the query subquery (see below)
            reversed = query[::-1]
            query = reversed.replace(';', '', 1)[::-1]
            
            # Prepare query to get rows in json format                
            query = f"SELECT row_to_json(RESULT_TABLE) FROM ({query}) AS RESULT_TABLE"
            print(query)
        else:
            if "EXPLAIN" not in query:
                query = f"EXPLAIN (ANALYZE FALSE, VERBOSE, FORMAT JSON) {query}"
        
        with self.conn:
            with self.conn.cursor() as curs:
                try:
                    curs.execute(query)
                    result = curs.fetchall()
                    return result
                except (Exception, psycopg2.DatabaseError) as error:
                    messagebox.showerror("test",error)


class QEPTreeVisualizer(ttk.Frame):
    """
    A class wrap the visualizer for the  QEP tree
    """

    def __init__(self, root, sql_query_display, sql_query_analysis_display, **kwargs):
        ttk.Frame.__init__(self, root, **kwargs)
        self.canvas = tk.Canvas(self, bg='#c5ded2')
        self.canvas.pack(fill=tk.BOTH)
        self.sql_query_display = sql_query_display
        self.sql_query_analysis_display = sql_query_analysis_display

        self._on_hover_listener = self.tree_on_hover_listener
        self._on_click_listener = self.tree_on_click_listener
        self._on_hover_end_listener = self.tree_on_hover_end_listener
        self.query = None
        self.sql_query_character_map = {}
        self.token_matcher_dict = None

    def set_query_reference(self, query):
        """
        Updates the self.query attribute to be used in this class whenever this tree is updated with the latest sql query
        """
        self.query = query

    def set_sql_query_character_map(self, sql_query_character_map):
        """
        Updates the self.sql_query_character_map attribute used in this class for identifying the indexes to highlight
        """
        self.sql_query_character_map = sql_query_character_map

    def set_token_matcher_dict(self, token_matcher_dict):
        """
        Used to update the self.token_matcher_dict attribute used to keep track of tokens parsed in the sql query.
        """
        self.token_matcher_dict = token_matcher_dict

    def tree_on_click_listener(self, node):
        """
        Listener for when node is click on the generated QEP Tree
        """
        self.show_node_analysis_info(node)

    def tree_on_hover_listener(self, node):
        """
        Listener for when cursor hovers over the node generated by the QEP Tree
        """
        if node in self.token_matcher_dict:
            for start, end in self.token_matcher_dict[node]:
                self.highlight_sql(start, end, node.node_type)

    def tree_on_hover_end_listener(self, node):
        """
        Listener for when cursor hovers over the node generated by the QEP Tree
        """
        self.clear_highlighting()

    def clear_highlighting(self):
        for node_type in NODE_TYPES + ['OTHER']:
            self.sql_query_display.text.tag_remove(node_type, '1.0', 'end')

    def highlight_sql(self, start, end, node_type):
        """
        Used to highlight the reference SQL query in the analysis tab 
        """
        if self.query is not None:
            print(f'query[{start}:{end}] = {self.query[start:end]}')
        if node_type in NODE_TYPES:
            self.sql_query_display.text.tag_add(node_type, self.sql_query_character_map[start], self.sql_query_character_map[end])
        else:
            self.sql_query_display.text.tag_add('OTHER', self.sql_query_character_map[start], self.sql_query_character_map[end])

    def show_node_analysis_info(self, node):
        """
        Based on the selected node, outputs the analysis onto the screen under the analysis tab
        """
        raw_json = node.raw_json
        print(raw_json)
        print("Showing node analysis information")
        self.sql_query_analysis_display.text.configure(state=NORMAL)
        self.sql_query_analysis_display.delete('1.0', END)
        self.sql_query_analysis_display.text.configure(state=DISABLED)
        node_type = None
        for index, (key, value) in enumerate(raw_json.items()):
            if key == "Node Type":
                node_type = value.upper()
                for operations in ATTRIBUTE:
                    if operations == node_type:
                        operation_type = ATTRIBUTE[operations]
            if key in operation_type:
                B = str(key) + ": " + str(value) + '\n'
                self.sql_query_analysis_display.text.configure(state=NORMAL)        
                self.sql_query_analysis_display.insert(END, B)
                # self.sql_query_analysis_display.insert(END, str(raw_json))
                self.sql_query_analysis_display.text.configure(state=DISABLED)
            if key == "aqp_analysis_message":
                node_category = None
                for category, type_list in NODE_TYPES_CATEGORY_MAPPING.items():
                        if node_type in type_list:
                            node_category = category
                            break
                if (node_category is not None):
                    analysis_string = f"\n ============ Insights with other {node_category} type operation ============\n{value}"
                    self.sql_query_analysis_display.text.configure(state=NORMAL)        
                    self.sql_query_analysis_display.insert(END, analysis_string)
                    self.sql_query_analysis_display.text.configure(state=DISABLED)

    def draw_tree(self, root_node):
        """
        Draw the tree on the canvas
        """
        self.clear_canvas()
        bbox = self._draw_node(root_node, 12, 12)
        self.canvas.configure(width=bbox[2] - bbox[0] + 24, height=bbox[3] - bbox[1] + 24)

    def clear_canvas(self):
        """
        Clear the whole canvas
        """
        self.canvas.delete("all")

    def _on_click(self, node):
        """
        On click Node
        """
        if self._on_click_listener is not None:
            self._on_click_listener(node)

    def _on_hover(self, node):
        """
        On hover over node
        """
        if self._on_hover_listener is not None:
            self._on_hover_listener(node)

    def _on_hover_end(self, node):
        """
        On hover end on node
        """
        if self._on_hover_end_listener is not None:
            self._on_hover_end_listener(node)

    def _draw_node(self, node, x1, y1):
        """
        Draw the exact button on canvas
        """
        child_x = x1
        left = x1
        right = -1
        top = y1
        bottom = -1
        button = tk.Button(self.canvas, text=node.node_type, padx=12,
                        bg='#7d8ed1', fg='white', anchor='center')
        button.bind('<Button-1>', lambda event: self._on_click(node)) # Bind to left click
        button.bind('<Enter>', lambda event: self._on_hover(node))
        button.bind('<Leave>', lambda event: self._on_hover_end(node))
        window = self.canvas.create_window((x1, y1), window=button, anchor='nw')
        bbox = self.canvas.bbox(window)
        child_bboxes = []
        if len(node.children) == 0:
            return bbox
        for child in node.children:
            child_bbox = self._draw_node(child, child_x, y1 + 60)  # (x1, y1, x2, y2)
            child_x = child_bbox[2] + 20
            right = max(right, child_bbox[2])
            bottom = max(bottom, child_bbox[3])
            child_bboxes.append(child_bbox)
        x_mid = (left + right) // 2
        bbox_mid_x = (bbox[0] + bbox[2]) // 2
        self.canvas.move(window, x_mid - bbox_mid_x, 0)
        for child_bbox in child_bboxes:
            child_mid_x = (child_bbox[0] + child_bbox[2]) // 2
            self.canvas.create_line(x_mid, bbox[3], child_mid_x, child_bbox[1], width=2, arrow=tk.FIRST)
        return left, top, right, bottom

    

   