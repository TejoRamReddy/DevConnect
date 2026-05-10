import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # 1. Projects Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        skills TEXT NOT NULL,
        owner TEXT NOT NULL
    )
    ''')

    # 2. Join Requests Table (The Permission System)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        applicant TEXT,
        status TEXT DEFAULT 'Pending'
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()