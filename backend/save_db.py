import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# MongoDB connection
myclient = pymongo.MongoClient(os.getenv("MONGO_URL"))
myDB = myclient[os.getenv("DB")]
myCol = myDB[os.getenv("COLLECTION")]

# Get all submissions sorted by score
submissions = list(myCol.find({}).sort("score", -1))

if len(submissions) == 0:
    print("No data in database!")
    exit()

# Create filename with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"leaderboard_{timestamp}.txt"

# Write to file
with open(filename, 'w') as f:
    f.write("=" * 70 + "\n")
    f.write(f"CaSScade Leaderboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 70 + "\n\n")
    
    # Table header
    f.write(f"{'Rank':<8} {'Username':<30} {'Score':<12} {'Round':<8}\n")
    f.write("-" * 70 + "\n")
    
    # Table rows
    for idx, submission in enumerate(submissions, 1):
        name = submission.get('name', 'Unknown')
        score = submission.get('score', 0)
        round_num = submission.get('round', 'N/A')
        
        f.write(f"{idx:<8} {name:<30} {score:<12.3f} {round_num:<8}\n")
    
    f.write("=" * 70 + "\n")
    f.write(f"Total Submissions: {len(submissions)}\n")

print(f"✓ Leaderboard saved to {filename}")
print(f"Total submissions: {len(submissions)}")

