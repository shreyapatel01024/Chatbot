import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("chatbot.db")

# Create cursor object
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE dsa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    description1 TEXT,
    description2 TEXT
)
''')

# Insert sample data
cursor.executemany('''
INSERT INTO dsa (topic, description1, description2)
VALUES (?, ?, ?)
''', [
    ("linkedlist", "A linked list is a linear data structure...", "It consists of nodes connected via pointers."),
    ("stack", "A stack follows Last In First Out (LIFO)...", "Used in undo operations, call stack, etc."),
    ("queue", "A queue follows First In First Out (FIFO)...", "Used in process scheduling, printer queues."),
    ("tree", "A tree is a hierarchical data structure...", "Nodes are connected via edges with one root."),
    ("graph", "A graph is a set of nodes and edges...", "Used to represent networks like social or transport."),
])

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created and populated successfully.")
