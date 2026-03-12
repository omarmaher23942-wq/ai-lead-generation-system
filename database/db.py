import sqlite3

def init_db():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        website TEXT,
        description TEXT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_lead(name, email, phone, website, description):
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    
    # متحفظش نفس الإيميل مرتين
    cursor.execute("SELECT id FROM leads WHERE email = ?", (email,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute("""
        INSERT INTO leads (name, email, phone, website, description)
        VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, website, description))
        conn.commit()
        print(f"💾 Saved: {name}")
    else:
        print(f"⏭️ Already exists: {name}")
    
    conn.close()

def get_all_leads():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads")
    leads = cursor.fetchall()
    conn.close()
    return leads