from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv


# Get passwords
load_dotenv()
db_password = os.getenv("DB_PASSWORD")
uri = f"mongodb+srv://AI:{db_password}@cluster0.gtl6qtn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client:MongoClient = MongoClient(uri, server_api=ServerApi('1'))
db = client['db-data']

# Update
try:
    db.cats.update_one(
    {'_id': ObjectId('6602c6ca234d7fc4956e0e2b')},
    {
      '$set': {
        'name': 'puri',
        'age': 3,
        'features': ['ходить в капці', 'дає себе гладити', 'рудий'],
       }
    })
    print("Updated!")
except Exception as e:
    print(e)

# Create
new_record_id = None
try:
    result = db.cats.insert_one({
        'name': 'barsik',
        'age': 3,
        'features': ['ходить в капці', 'дає себе гладити', 'рудий'],
    })
    print("Added!")
    new_record_id = result.inserted_id
    print("Id:", result.inserted_id)
except Exception as e:
    print(e)

# Find
print(list(db.cats.find()))

# Delete
try:
    db.cats.delete_one({'_id': ObjectId(new_record_id)})
    print("Deleted!")
except Exception as e:
    print(e)
