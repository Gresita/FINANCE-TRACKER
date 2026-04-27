def insert_test_user(db_path='finance_tracker.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fut një përdorues test në users
    try:
        cursor.execute("""
            INSERT INTO users (username, email, hashed_password) 
            VALUES (?, ?, ?)
        """, ("testuser", "testuser@example.com", "fakehashedpassword123"))
        conn.commit()
        print("Përdoruesi test u shtua me sukses!")
    except sqlite3.IntegrityError:
        print("Përdoruesi test ekziston tashmë.")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_test_user()