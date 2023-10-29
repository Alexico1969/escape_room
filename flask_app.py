from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from database import connector, check_login, register_user, get_user_data, Room, init_rooms, update_user
from process import process
import sqlite3


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SESSION_TYPE'] = 'filesystem'

db = connector()
print(db)


level = 1
score = 100
inventory = []

room = init_rooms() # Initialize the rooms: see database.py for details
        
@app.route('/', methods=['GET', 'POST'])
def home():
    global level, room, inventory, score

    if 'user' not in session:
            return redirect(url_for('login'))
    
    username = session['user']
    user_data = get_user_data(username)


    user_level = level
    room_data = room[level]
    rtype = room_data.type
    print(f"Room data: {room_data}")

    msg = room[level].description

    
    if request.method == 'POST':
        command = request.form['command']
        score -= 1
        msg = process(command, inventory, room[level], room, level)
        print()
        print(f"msg: {msg}")
        print(f"room[level].type: {room[level].type}")
        rtype = room[level].type
        if msg == "You exit the room":
            level += 1
            score += 100
            print("Redirecting to next level")
            return redirect(url_for('next_level'))

    return render_template('home.html', msg=msg, inventory=inventory, user_level=user_level, room_data=room_data, username=username,rtype=rtype, score=score, user_data=user_data)


@app.route('/next_level', methods=['GET', 'POST'])
def next_level():

    print("*** Entering NEXT LEVEL route ***")

    global level, room, inventory, score
    if 'user' not in session:
            return redirect(url_for('login'))
    
    username = session['user']
    user_data = get_user_data(username)

    user_level = level

    update_user(username, inventory, level, score)

    if request.method == 'POST':
        print('Redirecting to home')
        return redirect(url_for('home'))

    return render_template('next_level.html', user_level=user_level, username=username)

@app.route('/prev_level', methods=['GET', 'POST'])
def prev_level():

    print("*** Entering PREVIOUS LEVEL route ***")

    global level, room, inventory, score
    if 'user' not in session:
            return redirect(url_for('login'))
    
    username = session['user']
    user_data = get_user_data(username)

    level = level - 1
    user_level = level

    update_user(username, inventory, level, score)

    if request.method == 'POST':
        print('Redirecting to home')
        return redirect(url_for('home'))

    return render_template('prev_level.html', user_level=user_level, username=username)

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
    global level, score, inventory
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
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

# dump all the session data, and global variables to the screen
@app.route('/dump2', methods=['GET', 'POST'])
def dump2():
    return jsonify(session, level, score, inventory, room)



# -------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
