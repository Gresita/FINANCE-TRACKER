import sqlite3

def test_database_connection(db_path='finance_tracker.db'):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Kontrollo nëse tabela users ekziston
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            print("Tabela 'users' nuk ekziston në DB.")
            return False

        # Kontrollo nëse ka fare përdorues
        cursor.execute("SELECT * FROM users LIMIT 1;")
        user = cursor.fetchone()
        if user:
            print("Lidhja me DB funksionon. Gjeta një përdorues:", user)
        else:
            print("Lidhja me DB funksionon, por tabela users është bosh.")
        
        conn.close()
        return True
        
    except Exception as e:
        print("Gabim gjatë lidhjes me DB:", e)
        return False

if __name__ == "__main__":
    if test_database_connection():
        print("Testi i lidhjes me bazën e të dhënave kaloi me sukses!")
    else:
        print("Testi i lidhjes me bazën e të dhënave dështoi.")