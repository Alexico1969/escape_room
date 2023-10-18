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


class Room:
    def __init__(self="", level=0, description="", type="", door_locked=True, furniture="", objects="", expected_words="", expected_output=""):
        self.level = level
        self.description = description
        self.type = type
        self.door_locked = door_locked
        self.furniture = furniture
        self.objects = objects
        self.expected_words = expected_words
        self.expected_output = expected_output

def init_rooms():
    room = [1,1,1]
    #level 1
    room[0] = Room()
    room[1] = Room(1, 
                   "You are in a room. There is a table and a chair. There is a door to your left.", 
                   "inventory",
                   True,
                   "table,chair,door" , 
                   {"table":"key", "door":"doorlock", "chair":""}, 
                   "", 
                   "")
    return room
    


'''
rooms = {
    1: ["1", "You are in a room. There is a table and a chair. There is a door to your left.", "table,chair,door" , {"table":"key"}, "inventory", "key", "", ""],
    2: ["2", "table,computer,chair", {}, "code", "print,Hello,World", "Hello World", ""],
}

'''