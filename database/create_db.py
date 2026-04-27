import sqlite3

def create_finance_tracker_db(db_path="finance_tracker.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Krijimi i tabelave
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        category TEXT,
        transaction_type TEXT CHECK(transaction_type IN ('income','expense')) NOT NULL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        notes TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount_limit REAL NOT NULL,
        period TEXT NOT NULL, -- shembull: '2024-06'
        spent_amount REAL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        target_amount REAL NOT NULL,
        current_amount REAL DEFAULT 0,
        deadline DATETIME,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto_holdings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        quantity REAL NOT NULL,
        avg_price REAL NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category_type TEXT CHECK(category_type IN ('income','expense')),
        color TEXT
    );""")

    # Ruajtja e ndryshimeve dhe mbyllja
    conn.commit()
    conn.close()
    print(f"Database '{db_path}' u krijua me sukses me të gjitha tabelat.")

if __name__ == "__main__":
    create_finance_tracker_db()