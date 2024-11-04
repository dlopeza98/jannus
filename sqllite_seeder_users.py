import sqlite3

# Crear conexión a SQLite
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Drop the table if it exists and recreate it
cursor.execute("DROP TABLE IF EXISTS users")

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    uses_available INTEGER DEFAULT 5,
    active INTEGER DEFAULT 1
)
""")

max_requests = 10

# Agregar usuarios iniciales
initial_users = [
    ("demo1", "@Yfemz8Q7ENtB", max_requests, 1),
    ("demo2", "8oBHBLZrL-sqd", max_requests, 1),
    ("demo3", "C@R7.AHnMWAB_", max_requests, 1),
    ("demo4", "mBmz@aQdtTt2.", max_requests, 1),
    ("demo5", "3hqNjoCs4@h7D", max_requests, 1),
    ("demo6", "PQa5!ze9LxRb", max_requests, 1),
    ("demo7", "xNv@0BpRkV9#", max_requests, 1),
    ("demo8", "L#zW2g0.AyNc", max_requests, 1),
    ("demo9", "8Hv@Dq3j.C4s", max_requests, 1),
    ("demo10", "k5Tz-Bm@9A7Y", max_requests, 1),
    ("demo11", "3Gs.qxR@6J9t", max_requests, 1),
    ("demo12", "FvT#8aLk@z9M", max_requests, 1),
    ("demo13", "wN@5.Pq4hV8y", max_requests, 1),
    ("demo14", "7Bx#Lm3GvT9@", max_requests, 1),
    ("demo15", "qA8#2yP.Z5kR", max_requests, 1),
    ("demo16", "kT#3c4.GxR9y", max_requests, 1),
    ("demo17", "Vz8#xP@3yRq7", max_requests, 1),
    ("demo18", "A4Tz.W@9yBx2", max_requests, 1),
    ("demo19", "pQ5@Jm6zY#9t", max_requests, 1),
    ("demo20", "6Zx@8nPq#4Yb", max_requests, 1),
]

# Insertar usuarios en la tabla si no existen
for user in initial_users:
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", user)

conn.commit()
conn.close()
