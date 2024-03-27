import database_logic as db, hasher

if __name__ == '__main__':

    db.initialize_table()
    login = input("Insert your username: ")
    password = input("Insert your desired password: ")
    db.add_entry(login, hasher.hash_password(password)[0], hasher.hash_password(password)[1])
    print(db.select_entries())
    db.check_password(login, password)

