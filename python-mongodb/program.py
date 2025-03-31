import pymongo as mongo

# BEFORE YOU RUN THE PROGRAM, you must CHANGE this information 
# to match the required information for your Oracle server!
# Change "your_server", "1521" (port number) and "database_name" in this URL!
MONGODB_SERVER = "cis444.campus-quest.com"
MONGODB_PORT = 20020
MONGODB_USER = "admin"
MONGODB_PASSWORD = "Academic2025U0!"

# Leave these alone for the example.
# Change these once you start working with your own code.
# You can also omit these and just specify the database 
#   and collection names in the code itself.
MONGODB_DATABASE = "zeota"
MONGODB_COLLECTION = "employee"

# BEFORE YOU RUN THE PROGRAM, you must COMMENT OUT OR REMOVE
# this line! Only do this after you have updated the above
# lines to point to YOUR database server!
#raise SystemError("You did not read the instructions!")

# Attempts to create a connection to MongoDB.
try:
    _MONGODB_URL = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_SERVER}:{MONGODB_PORT}/?tls=true&tlsInsecure=true"
    conn_mongo = mongo.MongoClient(_MONGODB_URL)
    conn_mongo.server_info()
    print("MongoDB connected OK.")
except Exception as e:
    print(f"Exception connecting to MongoDB: {e}")
    exit(1)

print("Connection was made successfully.")
print()

# This query was created in MongoDB Compass and exported using Export To Language.
# You should assign the query to a variable - it helps keep the code more readable.
query = [
    {
        '$match': {
            'city': {
                '$regex': '^MANKATO$'
            }
        }
    }, {
        '$sort': {
            'birthdate': -1
        }
    }, {
        '$limit': 3
    }
]

try:
    # Connects to a specific database
    db = conn_mongo[MONGODB_DATABASE]
    # Connects to a specific collection within the database
    collection = db[MONGODB_COLLECTION]

    # Run query
    results = collection.aggregate(query)

    print("Query results:")
    for result in results:
        print(result)

except Exception as e:
    print(f"Exception running query: {e}")
    exit(1)