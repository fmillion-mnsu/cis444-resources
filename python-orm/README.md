# Using an ORM from Python to access databases

An ORM, or **O**bject **R**elational **M**apper, is a software library that allows programmatic access to data in relational databases without needing to write SQL queries directly. An ORM handles many functions, such as:

* converting code you write that works with collections into appropriate SQL statements.
* provide classes in the language you're using that allow you to represent rows in a database as instances of a class
* providing tools to *reverse-engineer* an existing database, generating appropriate classes for the database
    * ... and also tools that convert a set of classes into appropriate DDL statements for initializing and seeding a database

The advantages of using an ORM:

* **Safety.** Since the ORM is responsible for generating SQL code, you don't have to worry about potential issues such as SQL injection.
* **Performance.** ORMs can often devise highly efficient queries, especially if you are working with multiple data objects at the same time. 
* **Readability.** Someone else who reads your code doesn't necessarily need to understand your particular server's dialect of SQL to understand your intent.
* **Language-native data structures.** With an ORM, you can work with data in the native structures of your language. In Python, you can treat a table of rows as if it was a list of dictionaries. You can edit data by simply changing values in the dictionaries. You can add rows by adding them to the list, and you can delete rows by removing them from the list. You can even filter data using list comprehensions or the `filter` statement, which will be *translated* into SQL where possible by the ORM. (In the case that it is impossible to generate SQL for your statement, an equivalent `SELECT *` will be used to retrieve all data, which will then be processed locally as it would for any list or collection.)
* **Cross-compatibility.** The ORM provides a single high-level interface to data that could potentially exist in multiple different types of database engines. You don't need to do anything different to work with data in Oracle, MySQL or SQL Server (among others).
    * You *do* need to account for the unique characteristics of the RDBMS's you're connecting to when you're doing database reverse engineering, or when you're configuring the connection to each specific RDBMS.

ORMs are extremely popular in line-of-business and production applications due to the many advantages they offer both developers and database administrators (DBAs). It also can greatly simplify the time-to-production for data-driven applications and scenarios, allowing developers to stay focused in one language or environment (e.g. Python) rather than switching between different environments.

ORMs are available for most major programming languages and offer connectivity to most popular RDBMS's. We will be focusing on **[SQLAlchemy](https://www.sqlalchemy.org/)** for **Python** in this content, but several other ORMs exist:

* [Peewee](https://docs.peewee-orm.com/en/latest/) - for Python, a simplified ORM which is compact and fast, but doesn't offer some advanced functions like reverse engineering.
* [Django ORM](https://docs.djangoproject.com/en/5.1/topics/db/) - for Python, an ORM heavily integrated into the Django application framework, which is commonly used for writing web applications. If you're writing an app using Django, it makes sense to use its built in ORM.
* [Entity Framework](https://learn.microsoft.com/en-us/ef/) - for Microsoft .NET/C#, it is a mature, stable ORM that originally focused on connecting and working with Microsoft SQL Server, but has since been extended to connect to other databases such as MySQL or any ODBC-compatible data source. It also offers a robust reverse-engineering tool.
* [SeaORM](https://www.sea-ql.org/SeaORM/) - for Rust, a type-safe and performant ORM for Rust applications.
* [GORM](https://gorm.io/) - for Go, the most popular ORM for the Go language.
* And many others.

## SQLAlchemy

SQLAlchemy is one of the most popular ORMs for Python. Its popularity stems from its high performance and support of a wide variety of database backends. SQLAlchemy has first-class support for Microsot SQL Server, MySQL, PostgreSQL, Oracle, SQLite, and many custom and purpose-specific database systems such as CockroachDB.

SQLAlchemy follows object-oriented programming paradigms. To access a database, you first define **classes** for that database's tables and views. You then create an **engine**, which represents the actual connection to the database server, and is associated with a schema of classes representing the database's objects. From there, you can execute queries that read data, and you can also insert, update and delete records, including using SQL transactions for safety and performance.

## Getting Started

If you already have an existing database, you will need to use an ORM that supports **reverse engineering**. The process of reverse engineering involves connecting to the database and traversing all of its objects, creating classes that provide equivalent data types and interfaces for those objects.

To get started, we'll first need to install SQLAlchemy. For your convenience, this folder contains a `requirements.txt` file. As with the other Python examples in this repository, you can (and should) create a virtual environment within the `python-orm` folder.

The steps you will follow are as follows:

1. Make sure Python is set up on your system and the requirements for virtual environments are installed.
    - If you use Anaconda, you can [use it instead of `virtualenv`](#alternative-steps-for-anaconda-users). More information on this is included further on in the instructions.
2. [Download the code](#repository-download), [open it in your editor](#open-the-project-in-your-editor) and create a virtual environment. Your IDE may offer to do this for you; if not, [follow these instructions](#if-your-editor-does-not-offer-to-setup-the-environment-or-if-you-are-using-a-different-ide).
3. [Reverse-engineer a database](#reverse-engineering) to create a `models.py` file of the tables in the database.
4. [Work with the data](#queries-with-sqlalchemy) in Python using SQLAlchemy.

### Initial requirements setup

You also need to have `pip` installed, which is Python's built in package management toolset. On Windows, once you have Python installed, you should be able to run these commands at a command prompt to make sure `pip` is installed and updated to the latest version:

    python -m ensurepip
    python -m pip install -U pip

> On Windows, you may need to execute `python3` instead of `python` when installing `pip`. If you type `python` and receive a Windows Store popup, try `python3`.
>
> Note that once you activate a virtual environment, you must use `python` and **not** `python3`. This is due to a quirk in how Windows handles symbolic links.

Finally, you need the `virtualenv` module, which lets you setup virtual environments. Alternatively, `anaconda` has a similar capability with the `conda` package manager. These instructions will use `virtualenv`, but if you're using `anaconda`, I can provide separate support for that. 

To install `virtualenv`:

    python -m pip install virtualenv

### Repository download

Download the repository by [**clicking this link**](https://github.com/fmillion-mnsu/it544-python/archive/refs/heads/master.zip).

Extract the contents of the repository to somewhere on your computer.

### Open the project in your editor

Open the `python-mongodb` folder within the `cis444-resources` folder you extracted above. (Note that depending on how you extracted the data, you may have a nested folder - e.g. `cis444-resources\cis444-resources`. You want to select the *inner* folder in this case.)

Your editor may offer to create and setup the virtual environment for you. If so, you can allow it to do so. However, you will need to use the built-in terminal within your editor to ensure the environment is activated when you execute console commands. You can manually activate the environment in other terminals if you desire.

If you plan to use an external console regularly, you can follow the below instructions instead of allowing the IDE to set up the environment for you.

#### If your editor does not offer to setup the environment, or if you are using a different IDE

Open a **command prompt** and use the `cd` command to move to the path you extracted the files to.

Run the following command to create a virtual environment:

    python3 -m virtualenv venv

Now, run one of the following commands depending on your environment:

* **Windows, normal command shell**: `venv\scripts\activate.bat`
* **Windows, PowerShell**: `. .\venv\scripts\activate.ps1`
* **Mac/Linux**: `source venv/bin/activate`

    > Windows users: You can determine if you are using PowerShell by looking at your prompt - if it starts with `PS` (e.g. `PS C:\Users\...`), you are on PowerShell. If not (e.g. it starts with just `C:\Users\...`) then you are using the normal command shell.

You will know that the virtual environment activated successfully if you see that your prompt now begins with `(venv)`.

Finally, run this command to install the libraries into the virtual environment.

    pip install -r requirements.txt

### Alternative steps for Anaconda users

If you use Anaconda, you can setup a `conda` environment instead of using `virtualenv`. 

Open the **Anaconda Powershell Prompt** from your Start menu and `cd` to the directory you have extracted the code to. Then, run these commands to setup your environment (note: you can replace `cis444` with whatever environment name you wish; just make sure to use the same name whenever referencing the environment.)

    conda create cis544
    conda activate cis544
    conda install pip
    pip install -r requirements.txt

From here on, you can open the code in PyCharm or whatever editor you are using. Note that in some cases PyCharm may fail to detect the Conda environment, so you may need to keep the Anaconda prompt window open to manually run your code.

### Reverse engineering

Before we can work with data using an ORM, we need to have **classes** in our code that represent all of the data objects we might work with from the database. If we were building a new application from scratch, we could define those classes ourselves in Python, following the requirements of the ORM, and then have the ORM generate and execute DDL statements (`CREATE TABLE` etc.) to create the structure we define in the database. 

However, in our case, we already have existing databases. While we could manually examine the databases and create classes by hand, this tedious process has thankfully been mostly automated by the process of *reverse engineering*. The reverse engineering process essentially means that the ORM will "do the work for you" - it will connect to the database, enumerate all of the tables and views, examine their structures and produce correct class code for you. 

#### Oracle

Oracle 11g is an older database engine, and thus SQLAlchemy, while it can access Oracle 11g just fine, has trouble handling the advanced steps needed to do the *reflection* step (where SQLAlchemy discovers the structure of the database tables). Therefore, I have provided you with a script called `generate_oracle.py` that will assist with generating the classes manually for Oracle databases.

1. Open the `generate_oracle.py` file.
1. **Edit** the variables to point to your server.
1. **Comment out** the `raise` statement - this proves you read the instructions!
1. Save the script.
1. Run it by typing `python generate_oracle.py > oracle_models.py`.

    This step will run the script, connect to the Oracle server and generate classes for your tables in the file `oracle_models.py`, which you will use later for accessing the database via SQLAlchemy.

#### Microsoft SQL Server

SQL Server is well supported using SQLAlchemy's built in reflection and generation tools.

This command is all you need to generate your MS SQL tables:

    sqlacodegen mssql+pymssql://<username>:<password>!@cis444.campus-quest.com:<port>/<database> > mssql_models.py

> Remember to replace any item in angle brackets (`< >`) with the appropriate value for *your* team!

You should now have two model files - one for Oracle and one for MS SQL.

> Note that you can create as many models for as many databases as you like. You can simply change the name of the file at the end of the command to write to a different file. So, for example, you might write the `ZeotaDB` tables in MSSQL to `zeota_mssql_models.py`.

### Queries with SQLAlchemy

Now that we have a model file, we can write code to actually interact with the database using SQLAlchemy!

The `program.py` script shows you how to connect to and use the database. The code supports both Oracle models and MSSQL models. 
