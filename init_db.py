import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pengirim TEXT NOT NULL,
    isi_pesan TEXT NOT NULL,
    label_ai TEXT
)
""")

conn.commit()
conn.close()