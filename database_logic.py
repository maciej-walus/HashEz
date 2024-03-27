import sqlite3, hasher
con = sqlite3.connect("HashEZ.db")
cur = con.cursor()
def initialize_table():
    cur.execute("PRAGMA table_info(users)")
    if cur.fetchone() is None:
        cur.execute("CREATE TABLE users(login, hashed_seeded_password, seed)")
    else:
        print("Table has already been created.")

def add_entry(login, hashed_password, seed):
    # Check whether said user already exists
    cur.execute("SELECT EXISTS (SELECT 1 FROM users WHERE login=?)", (login,))
    if cur.fetchone()[0]:
        print("User already exists.")
    else:
        cur.execute("INSERT INTO users(login, hashed_seeded_password, seed) VALUES (?, ?, ?)", (login, hashed_password, seed))
        con.commit()

def modify_entry(index, new_login, new_hashed_password, new_seed):
    cur.execute("SELECT COUNT(*) FROM users WHERE rowid=?", (index,))
    if cur.fetchone()[0] == 0:
        print("Record not found.")

    cur.execute("UPDATE users SET login=?, hashed_seeded_password=?, seed=? WHERE rowid=?", (new_login, new_hashed_password, new_seed, index))
    con.commit()

def delete_entry_by_index(cur, con, index):
    cur.execute("SELECT COUNT(*) FROM users WHERE rowid=?", (index,))
    if cur.fetchone()[0] == 0:
        print("Record not found.")

    # Delete the record
    cur.execute("DELETE FROM users WHERE rowid=?", (index,))
    con.commit()

def select_entries(index=-1):
    if index == -1:
        # Returns the whole table
        cur.execute("SELECT * FROM users")
        return cur.fetchall()
    else:
        cur.execute("SELECT COUNT(*) FROM users WHERE rowid=?", (index,))
        if cur.fetchone()[0] == 0:
            print("Record not found.")
        cur.execute("SELECT * FROM users WHERE rowid=?", (index,))
        return cur.fetchone()

def check_password(login, password):
    cur.execute("SELECT hashed_seeded_password, seed FROM users WHERE login=?", (login,))
    result = cur.fetchone()
    if result is not None:

        hashed_password, salt = result
        password = hasher.hash_password(password, salt)

        if hashed_password == password:
            print("The user-provided password is correct.")
        else:
            print("The user-provided password is incorrect.")
    else:
        print("The specified login does not exist in the database.")
