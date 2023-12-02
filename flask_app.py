from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from database import connector, check_login, register_user, get_user_data, Room, init_rooms, update_user, store, get
from process import process
import sqlite3


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SESSION_TYPE'] = 'filesystem'

db = connector()
print(db)

rooms = init_rooms()
        
@app.route('/', methods=['GET', 'POST'])
def home():
    global rooms

    if 'user' not in session:
            return redirect(url_for('login'))
    
    username, score, level, inventory, objects, door_status = get()

    if score == 100:
        session['new'] = True
    else:
        session['new'] = False

    print("=== in home route ===")
    print()
    print(f"*** Inventory: {inventory}")
    print(f"*** Level: {level}")
    print(f"*** Score: {score}")
    print(f"*** Username: {username}")
    print()

    user_level = level
    room_data = rooms[level]
    rtype = room_data.type
    print(f"Room data: {room_data}")

    msg = rooms[level].description

    
    if request.method == 'POST':
        command = request.form['command']
        score -= 1
        if score == 100:
            session['new'] = True
        else:
            session['new'] = False
        msg = process(command, inventory, rooms[level], rooms, level, objects)
        print()
        print(f"msg: {msg}")
        print(f"rooms[level].type: {rooms[level].type}")
        rtype = rooms[level].type
        if msg == "You exit the room":
            print("Redirecting to next level")
            return redirect(url_for('next_level'))

    return render_template('home.html', msg=msg, inventory=inventory, user_level=user_level, room_data=room_data, username=username,rtype=rtype, score=score)


@app.route('/next_level', methods=['GET', 'POST'])
def next_level():

    print("*** Entering NEXT LEVEL route ***")
    if 'user' not in session:
            return redirect(url_for('login'))
    
    username = session['user']
    level = session['level']
    inventory = session['inventory']
    score = session['score']
    objects = session['objects']
    session['door_status'] = "locked"

    print("=== in next_level route ===")
    print()
    print(f"*** Inventory: {inventory}")
    print(f"*** Level: {level}")
    print(f"*** Score: {score}")
    print(f"*** Username: {username}")
    print()
    
    if request.method == 'POST':
        level = level + 1
        score += 100
        objects = rooms[level].objects
        store(username, score, level, inventory, objects)
        update_user(username, inventory, level, score)
        print('Redirecting to home')
        return redirect(url_for('home'))
    
    # we want to put the leveling up here, so it doesn't run twice !


    user_level = level + 1

    return render_template('next_level.html', user_level=user_level, username=username)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid

        if check_login(username, password):
            msg = 'Username already exists'
            return render_template('register.html', msg=msg)

        # Register the user
        register_user(name, email, username, password, 1, 100, "")

        return redirect(url_for('login'))

    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global rooms
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid

        if check_login(username, password):
            session['user'] = username
            print("user logged in")
            level = get_user_data(username)[0][4]
            score = get_user_data(username)[0][5]
            inventory = []
            inventory_string = get_user_data(username)[0][6]
            if inventory_string != "":
                inventory = inventory_string.split(",")

            session['level'] = level
            session['score'] = score
            session['inventory'] = inventory
            session['objects'] = rooms[level].objects
            session['door_status'] = "locked"
            session['new'] = True
            print(f"session['new']: {session['new']}")

            return redirect(url_for('home'))
        else:
            msg = "Invalid login"
            print(f"Invalid login: {username}, {password}")
            

    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# dump all the data in the database to the screen
@app.route('/dump1', methods=['GET', 'POST'])
def dump1():
    if 'user' not in session:
            return redirect(url_for('login'))

    if session['user'] != 'admin':
        return redirect(url_for('home'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.close()

    lines = []

    for row in data:
        lines.append(row)

    return render_template('dump.html', lines=lines)



# -------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
