import os
import sqlite3

def get_conn():
    db_url = os.getenv("DATABASE_URL")
    
    if db_url and db_url.startswith("postgresql"):
        import psycopg2
        return psycopg2.connect(db_url), "pg"
    else:
        return sqlite3.connect("leads.db"), "sqlite"

def init_db():
    conn, db_type = get_conn()
    cursor = conn.cursor()
    
    if db_type == "pg":
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            website TEXT,
            description TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            website TEXT,
            description TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    
    conn.commit()
    conn.close()

def save_lead(name, email, phone, website, description):
    conn, db_type = get_conn()
    cursor = conn.cursor()
    
    try:
        if db_type == "pg":
            cursor.execute("""
            INSERT INTO leads (name, email, phone, website, description)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            """, (name, email, phone, website, description))
        else:
            cursor.execute("SELECT id FROM leads WHERE email = ?", (email,))
            if not cursor.fetchone():
                cursor.execute("""
                INSERT INTO leads (name, email, phone, website, description)
                VALUES (?, ?, ?, ?, ?)
                """, (name, email, phone, website, description))
        
        conn.commit()
        print(f"💾 Saved: {name}")
    except Exception as e:
        print(f"⚠️ Save error: {e}")
    finally:
        conn.close()

def get_all_leads():
    conn, db_type = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY scraped_at DESC")
    leads = cursor.fetchall()
    conn.close()
    return leads