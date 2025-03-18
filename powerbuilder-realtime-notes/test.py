import sqlite3

# Connect to SQLite database (creates 'notes.db' if it doesn't exist)
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

print("Connected to database successfully.")

# Create 'users' table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')
print("Users table checked/created successfully.")

# Check if 'user_id' column exists in 'notes' table
cursor.execute("PRAGMA table_info(notes)")
columns = [column[1] for column in cursor.fetchall()]

if "user_id" not in columns:
    cursor.execute('ALTER TABLE notes ADD COLUMN user_id INTEGER')
    print("Column 'user_id' added to notes table.")
else:
    print("Column 'user_id' already exists in notes table. Skipping ALTER TABLE.")

# Commit changes and close connection
conn.commit()
conn.close()
print("Database setup completed successfully.")
