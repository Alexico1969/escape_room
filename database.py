import sqlite3

def connector():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, username TEXT, password TEXT, level INTEGER, score INTEGER, inventory TEXT )')
    print("Table 'users' created successfully")
    conn.close()
    
def check_login(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    data = c.fetchall()
    conn.close()
    if len(data) == 0:
        return False
    return True

def get_user_data(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    data = c.fetchall()
    conn.close()
    return data

def register_user(name, email, username, password, level, score, inventory):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, username, password, level, score, inventory) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, email, username, password, level, score, inventory))
    conn.commit()
    conn.close()


# room variables: level : [furneture, inventory, type, keywords, output, info]
rooms = {
    1: ["1", "You are in a room. There is a table and a chair. There is a door to your right.", "table,chair" , "key", "inventory", "key", "", ""],
    2: ["2", "table,computer,chair", "code", "print,Hello,World", "Hello World", ""],
}