import sqlite3
from flask import session

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

def get():
    #get values from Session
    username = session['user']
    score = session['score']
    level = session['level']
    inventory = session['inventory']
    objects = session['objects']
    door_status = session['door_status']

    return username, score, level, inventory, objects, door_status

def store(username, score, level, inventory, objects):
    #store in Session
    session['user'] = username
    session['score'] = score
    session['level'] = level
    session['inventory'] = inventory
    session['objects'] = objects
    

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
    rooms = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    #level 1
    rooms[0] = Room()
    rooms[1] = Room(1, 
                   "You are in a room. There is a table, a small cabinet and a chair. There is a door to your left.", 
                   "inventory",
                   True,
                   "table,chair,door,cabinet" , 
                   {"table":"key", "door":"<doorlock>", "chair":"", "cabinet":"<spider>"}, 
                   "", 
                   "")
    rooms[2] = Room(2,
                     "You are in a room. There is a table, a cabinet and 2 chairs. There is a door to your left.", 
                     "code",
                     True,
                     "table,chair,door,cabinet" , 
                     {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<fly>", "doorlock":"<sophisticated piece of technology>"}, 
                     "", 
                     "321321")
    
    rooms[3] = Room(3,
                     "You are in a room. There is a table, a small cabinet, a plant and a chair. There is a door to your left.", 
                     "code",
                     True,
                     "table,chair,door,cabinet,plant" , 
                     {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<spider>", "plant":"<leaf>", "doorlock":"<sophisticated piece of technology>"}, 
                     "", 
                     "1051")
    
    rooms[4] = Room(4,
                        "You are in a room. There is a table and 2 chairs. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":"<cushen>", "cabinet":"<pencil>", "doorlock":"<sophisticated piece of technology>"},
                        "",
                        "1821")
    
    rooms[5] = Room(5,
                        "You are in a room. There is a table, a small cabinet, a painting and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet,painting" ,
                        {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<spider>", "painting":"<price-tag: $20>", "doorlock":"<sophisticated piece of technology>"},
                        "",
                        "8888")
    
    rooms[6] = Room(6,
                        "You are in a room. There is a table, a small cabinet and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"", "doorlock":"<sophisticated piece of technology>"},
                        "",
                        "1324")
    
    rooms[7] = Room(7,
                        "You are in a room. There is a table, a small cabinet and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<spider>", "painting":"<price-tag: $20>", "doorlock":"<sophisticated piece of technology>"},
                        "",
                        "379379")
    
    rooms[8] = Room(8,
                        "You are in a room. There is a table, a small cabinet, a poster and a chair. There is a door to your left.",
                        "code",
                        True,
                        "table,chair,door,cabinet,poster" ,
                        {"table":"computer", "door":"<doorlock>", "chair":"", "cabinet":"<spider>", "poster":"<picture of David Malan>", "doorlock":"<sophisticated piece of technology>"},
                        "",
                        "1331")
    
    rooms[9] = Room(9,
                        "You are in a room. There is a table and a small cabinet. There is a door to your left.",
                        "code",
                        True,
                        "table,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "cabinet":"", "doorlock":"<sophisticated piece of technology>"},
                        "",
                        "2748")
    
    rooms[10] = Room(10,
                        "You are in a room. There is a table and a small cabinet. There is a door to your left.",
                        "code",
                        True,
                        "table,door,cabinet" ,
                        {"table":"computer", "door":"<doorlock>", "cabinet":"", "doorlock":"<sophisticated piece of technology>"},
                        "",
                        "9999")
    
    rooms[11] = Room(11,
                        "Do you like binge-watching? I'm at season 2, episode 4. Check out the poster !",
                        "code",
                        True,
                        "table,chair,door,cabinet,poster" ,
                        {"table":"computer", "door":"<doorlock>", "cabinet":"","poster":"<picture of 'The OA'>"},
                        "",
                        "yyy")
    
    rooms[12] = Room(12,
                        "Life is beautiful",
                        "code",
                        True,
                        "table,chair,door,cabinet,poster" ,
                        {"table":"computer", "door":"<doorlock>", "cabinet":"","poster":"<picture of 'La Vita e Bella'>"},
                        "",
                        "silence")
    
    rooms[13] = Room(13,
                        "The choice is yours.... ",
                        "code",
                        True,
                        "table,chair,door,cabinet,poster" ,
                        {"table":"computer", "door":"<doorlock>", "cabinet":"","poster":"<picture of 'the Matrix'>"},
                        "",
                        "red pill")


    rooms[14] = Room(14,
                        "You are in.. yet another room... you hear a noise...",
                        "person",
                        True,
                        "door,cabinet" ,
                        {"table":"", "door":"", "cabinet":""},
                        "",
                        "----")


    rooms[15] = Room(14,
                        "This is the last level for now.",
                        "last",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"screwdriver", "door":"<blue doorlock>", "chair":"", "desk":"newspaper"},
                        "",
                        "----")
    
    '''

    rooms[11] = Room(11,
                        "This is the last level for now.",
                        "last",
                        True,
                        "table,chair,door,cabinet" ,
                        {"table":"screwdriver", "door":"<blue doorlock>", "chair":"", "desk":"newspaper"},
                        "",
                        "----")
    
    
    '''
                   





    return rooms
    


'''
rooms = {
    1: ["1", "You are in a room. There is a table and a chair. There is a door to your left.", "table,chair,door" , {"table":"key"}, "inventory", "key", "", ""],
    2: ["2", "table,computer,chair", {}, "code", "print,Hello,World", "Hello World", ""],
}

'''