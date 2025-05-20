from pymongo import MongoClient

uri = "mongodb+srv://Z33xD:<MxVEi2OTvIs4HfjM>@cluster0.7n8pqpy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["test_db"]
print(db.list_collection_names())