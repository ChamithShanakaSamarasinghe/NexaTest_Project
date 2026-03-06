import os

# BASE_DIR = project root folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # points to src\db folder
# Move up two levels to get project root
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

# Database is in the root folder
DB_PATH = os.path.join(ROOT_DIR, "db.sqlite3")

print(f"✅ Using database at: {DB_PATH}")