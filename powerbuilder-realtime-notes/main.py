from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Header
from pydantic import BaseModel
from typing import List
import sqlite3
import os
from passlib.hash import bcrypt
import jwt
import datetime

app = FastAPI()

# ✅ Secure Secret Key using Environment Variables
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")

# ✅ Database Connection Function
def get_db_connection():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Ensure Users & Notes Tables Exist
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    # Create notes table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Check if 'user_id' column exists
    cursor.execute("PRAGMA table_info(notes);")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE notes ADD COLUMN user_id INTEGER;")
        print("✅ Added missing 'user_id' column to notes table.")

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

# ✅ Run database initialization at startup
initialize_database()

# ✅ Pydantic Models
class UserSignup(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Note(BaseModel):
    title: str
    content: str

class NoteWithID(Note):
    id: int

# ✅ Authentication Function (Extract JWT Token)
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✅ User Registration Endpoint
@app.post("/signup")
def signup(user: UserSignup):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password and store
    hashed_password = bcrypt.hash(user.password)
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                   (user.username, hashed_password))
    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}

# ✅ User Login Endpoint (Returns JWT Token)
@app.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    user_data = cursor.fetchone()

    if not user_data or not bcrypt.verify(user.password, user_data["password_hash"]):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate JWT Token
    payload = {
        "sub": user_data["username"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    conn.close()
    return {"access_token": token}

# ✅ WebSockets for Real-time Updates
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keeps connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_message(message: str):
    """Send real-time updates to all active WebSocket connections."""
    for connection in active_connections:
        await connection.send_text(message)

# ✅ Get All Notes (Requires Authentication)
@app.get("/notes", response_model=List[NoteWithID])
def get_notes(username: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user_id
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=401, detail="User not found")

    # Fetch notes for the logged-in user
    cursor.execute("SELECT id, title, content FROM notes WHERE user_id = ?", (user["id"],))
    notes = cursor.fetchall()
    conn.close()

    return [{"id": row["id"], "title": row["title"], "content": row["content"]} for row in notes]

# ✅ Add a New Note (Requires Authentication)
@app.post("/notes")
async def add_note(note: Note, username: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user_id
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=401, detail="User not found")

    # Insert note into database
    cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)", 
                   (user["id"], note.title, note.content))
    conn.commit()
    conn.close()

    await broadcast_message("New note added")
    return {"message": "Note added successfully"}

# ✅ Delete a Note (Requires Authentication)
@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, username: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user_id
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=401, detail="User not found")

    # Check if the note belongs to the user before deleting
    cursor.execute("SELECT * FROM notes WHERE id = ? AND user_id = ?", (note_id, user["id"]))
    note = cursor.fetchone()

    if not note:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found or unauthorized")

    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

    await broadcast_message(f"Note with ID {note_id} deleted")
    return {"message": "Note deleted successfully"}

# ✅ Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI Notes API with Authentication!"}
