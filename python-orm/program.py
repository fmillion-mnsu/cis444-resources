from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# For Oracle
import oracle_models as models
ORACLE_HOST = "cis444.campus-quest.com"
ORACLE_PORT = 1521 # your port here!
ORACLE_USER = "ZEOTADB" # you can change this to another DB.
ORACLE_PASSWORD = "your_password_here" # you must put your password here!
ORACLE_SID = 'xe' # this can be left alone

# For MSSQL - uncomment this code
# Change the import name from "models" if you are using both servers at once.
# import mssql_models as models
# MSSQL_HOST = "cis444.campus-quest.com"
# MSSQL_PORT = 1433 # your port here!
# MSSQL_USER = "sa" 
# MSSQL_PASSWORD = "your_password_here" # you must put your password here!
# MSSQL_DATABASE = "your_database_name_here" # e.g. FAOES, ZeotaDB...

raise SystemError("You must read the instructions first.")

# For Oracle
connection_string = f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/?service_name={ORACLE_SID}"
# For MSSQL:
#connection_string = f"mssql+pymssql://{MSSQL_USER}:{MSSQL_PASSWORD}@{MSSQL_HOST}:{MSSQL_PORT}/{MSSQL_DATABASE}"

# Create engine
engine = create_engine(connection_string)

# Create a session
with Session(engine) as session:

    print("Connected to database OK.")

    # Basic query to get all orders
    all_products = session.query(models.PRODUCT).all()

    # Print results
    print("All Products:")
    for product in all_products:
        print(f"no: {product.PRODUCT_NO}, name: {product.PRODUCT_DESCRIPTION}")
    
    # Query with filter
    in_stock = session.query(models.PRODUCT).filter(models.PRODUCT.QOH > 0).all()
    
    print(f"\nThere are {len(in_stock)} products in stock.")
    
    # Query with ordering
    highest_paid = session.query(models.EMP_SALARY)\
        .filter(models.EMP_SALARY.AMOUNT > 2000) \
        .order_by(models.EMP_SALARY.AMOUNT.desc()) \
        .limit(5) \
        .all()
    
    print("\nHighest paid employees:")
    for emp in highest_paid:
        print(f"position ID: {emp.EMP_POS_NO}, amount: {emp.AMOUNT}")
    
    # Using SQL Expression Language (alternative to ORM syntax)
    companies_with_a = select(models.COMPANY).where(models.COMPANY.COMP_NAME.like("A%"))
    result = session.execute(companies_with_a)
    
    print("\nCompanies starting with A:")
    for row in result:
        # row is a tuple with one element
        company: models.COMPANY = row[0]
        print(f"company ID: {company.COMP_NO}, name: {company.COMP_NAME}")

    # This query only works if you're using MSSQL, since the Oracle tables don't define foreign keys right now.

    # Query that uses foreign key relationships
    # employees_at_branch = session.query(models.BRANCH).limit(1).all()
    # first_branch = employees_at_branch[0]
    # print(f"\nThe first branch is branch number {first_branch.BRANCH_NO} at {first_branch.BRANCH_ADDRESS}.")
    # for emp in first_branch.EMPLOYEE:
    #     print(f"  - {emp.FNAME} {emp.LNAME} works there.")