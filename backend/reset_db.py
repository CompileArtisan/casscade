import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
myclient = pymongo.MongoClient(os.getenv("MONGO_URL"))
myDB = myclient[os.getenv("DB")]
myCol = myDB[os.getenv("COLLECTION")]

# Count current documents
count = myCol.count_documents({})
print(f"Current documents in database: {count}")

if count == 0:
    print("Database is already empty!")
    exit()

# Confirm deletion
confirm = input(f"Delete all {count} documents? (yes/no): ")

if confirm.lower() == 'yes':
    result = myCol.delete_many({})
    print(f"✓ Deleted {result.deleted_count} documents")
    print(f"Database is now empty")
else:
    print("Deletion cancelled")
