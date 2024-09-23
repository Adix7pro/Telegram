import sqlite3

con = sqlite3.connect('db.sqlite3')
try:
    with con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE Users (
        id INTEGER NOT NULL UNIQUE,
        user_id INTEGER NOT NULL UNIQUE,
        PRIMARY KEY (id AUTOINCREMENT)
        );
        
""")
except:
    pass

def sql_code(text):
    try:
        with sqlite3.connect('db.sqlite3') as conn:
            cur = conn.cursor()
            r = cur.execute(text)
            conn.commit()
            return r.fetchall()
    except Exception as e:
        return e        