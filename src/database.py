import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("database/absensi.db")
DB_PATH.parent.mkdir(exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            waktu TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_absensi(nama):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO absensi (nama, waktu) VALUES (?, ?)",
        (nama, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def export_csv(filepath="rekap_absensi.csv"):
    import csv
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM absensi")

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nama", "Waktu"])
        writer.writerows(cur.fetchall())

    conn.close()
