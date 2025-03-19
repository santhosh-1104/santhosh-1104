import sqlite3

# Connect to SQLite database (creates it if not exists)
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

# Drop the table if it already exists (optional, to avoid conflicts)
cursor.execute("DROP TABLE IF EXISTS notes")

# Create a new table with the correct structure
cursor.execute("""
    CREATE TABLE notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
""")

# Commit and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")
