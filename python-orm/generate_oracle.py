from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, inspect
from sqlalchemy.ext.declarative import declarative_base
import sys
import cx_Oracle

def printerr(*args, **kwargs):
    print(*args, file=sys.stderr, flush=True, **kwargs)

# Connection details

ORACLE_HOST = "cis444.campus-quest.com"
ORACLE_PORT = 1521 # your port here!
ORACLE_USER = "" # you can change this to another DB.
ORACLE_PASSWORD = "" # you must put your password here!
ORACLE_SID = 'xe' # this can be left alone

raise SystemError("Please read the instructions first.")

# Connect directly with cx_Oracle first to get table info
connection = cx_Oracle.connect(f"{ORACLE_USER}/{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SID}")
cursor = connection.cursor()

# Get all tables owned by the user
cursor.execute("SELECT table_name FROM user_tables")
tables = [row[0] for row in cursor]

printerr(f"Found {len(tables)} tables")

# Create model template file
sys.stdout.write("from sqlalchemy import Column, Integer, String, Float, Date\n")
sys.stdout.write("from sqlalchemy.ext.declarative import declarative_base\n\n")
sys.stdout.write("Base = declarative_base()\n\n")

# For each table, create a class definition
for table_name in sorted(tables):
    printerr(f"Reflecting {table_name}...")
    # Get column information
    cursor.execute(f"""
        SELECT column_name, data_type, data_length, nullable
        FROM user_tab_columns
        WHERE table_name = '{table_name}'
    """)
    columns = cursor.fetchall()
    
    # Get primary key columns
    cursor.execute(f"""
        SELECT cols.column_name
        FROM user_constraints cons, user_cons_columns cols
        WHERE cons.constraint_name = cols.constraint_name
        AND cons.constraint_type = 'P'
        AND cons.table_name = '{table_name}'
    """)
    pk_columns = [row[0] for row in cursor]
    
    # Write class definition
    sys.stdout.write(f"class {table_name}(Base):\n")
    sys.stdout.write(f"    __tablename__ = '{table_name}'\n")
    
    # Write column definitions
    for col in columns:
        col_name = col[0]
        data_type = col[1]
        length = col[2]
        nullable = col[3] == 'Y'
        
        # Map Oracle data types to SQLAlchemy types
        if data_type == 'NUMBER':
            sa_type = 'Integer'
        elif data_type.startswith('VARCHAR'):
            sa_type = f'String({length})'
        elif data_type == 'DATE':
            sa_type = 'Date'
        else:
            sa_type = 'String(255)'  # Default fallback
        
        # Is this a primary key?
        is_pk = col_name in pk_columns
        if is_pk:
            pk_text = ", primary_key=True" if is_pk else ""
            pk_col_name = col_name
        nullable_text = "" if is_pk or not nullable else ", nullable=True"
        
        sys.stdout.write(f"    {col_name} = Column({sa_type}{pk_text}{nullable_text})\n")
    
    sys.stdout.write("\n    def __repr__(self):\n")
    sys.stdout.write(f"        return f\"<{table_name.title()}(id={{self.{pk_col_name}}})>\"\n\n")

connection.close()
printerr("Models file generated successfully!")