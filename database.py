import sqlite3

def connector():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, username TEXT, password TEXT, level INTEGER, score INTEGER, inventory TEXT )')
    print("Table 'users' active")
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

def update_user(username, inventory, level, score):
    inv_string = ""
    for el in inventory:
        inv_string += el + ","
    inventory = inv_string[:-1]
    print(f"*** Inventory: {inventory}")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET level = ?, score = ?, inventory = ? WHERE username = ?", (level, score, inventory, username))
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
    room = [1,1,1,1,1,1,1,1,1,1,1,1]
    #level 1
    room[0] = Room()
    room[1] = Room(1, 
                   "You are in a room. There is a table, a small cabinet and a chair. There is a door to your left.", 
                   "inventory",
                   True,
                   "table,chair,door,cabinet" , 
                   {"table":"key", "door":"<doorlock>", "chair":"", "cabinet":"<spider>"}, 
                   "", 
                   "")
    room[2] = Room(2,
                     "You are in a room. There is a table, a cabinet and 2 chairs. There is a door to your left.", 
                     "code",
                     True,
                     "table,chair,door,cabinet" , 
                     {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<fly>"}, 
                     "", 
                     "2222")
    
    room[3] = Room(3,
                     "You are in a room. There is a table, a small cabinet, a plant and a chair. There is a door to your left.", 
                     "code",
                     True,
                     "table,chair,door,cabinet,plant" , 
                     {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<spider>", "plant":"<leaf>"}, 
                     "", 
                     "51")
    
    room[4] = Room(4,
                        "You are in a room. There is a table and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":""},
                        "",
                        "1821")
    
    room[5] = Room(5,
                        "You are in a room. There is a table, a small cabinet, a painting and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<spider>", "painting":"<price-tag: $20>"},
                        "",
                        "8000")
    
    room[6] = Room(6,
                        "You are in a room. There is a table and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":""},
                        "",
                        "4444")
    
    room[7] = Room(7,
                        "You are in a room. There is a table, a small cabinet, a painting and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<spider>", "painting":"<price-tag: $20>"},
                        "",
                        "1.6")
    
    room[8] = Room(8,
                        "You are in a room. There is a table and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":""},
                        "",
                        "-20")
    
    room[9] = Room(9,
                        "You are in a room. There is a table and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":""},
                        "",
                        "24")
    
    room[10] = Room(10,
                        "You are in a room. There is a table and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":""},
                        "",
                        "9999")
    
    room[11] = Room(11,
                        "You are in a room. There is a table and a chair. There is a door to your left.",
                        "last",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"screwdriver", "door":"<blue doorlock>", "chair":"", "desk":"newspaper"},
                        "",
                        "----")
    

                   





    return room
    


'''
rooms = {
    1: ["1", "You are in a room. There is a table and a chair. There is a door to your left.", "table,chair,door" , {"table":"key"}, "inventory", "key", "", ""],
    2: ["2", "table,computer,chair", {}, "code", "print,Hello,World", "Hello World", ""],
}

'''