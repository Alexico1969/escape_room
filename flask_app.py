from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from database import connector, check_login, register_user, get_user_data, rooms
from process import process


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SESSION_TYPE'] = 'filesystem'

db = connector()
print(db)


level = 1

class Room:
    def __init__(self="", description="", door_status="", furniture="", objects="", expected_words="", expected_output=""):
        self.description = description
        self.door_status = door_status
        self.furniture = furniture
        self.objects = objects
        self.expected_words = expected_words
        self.expected_output = expected_output

room = Room()

def set_up_room():

    global room, level
    room_data = rooms[level]
    room.description = room_data[1]
    room.door_status = "locked"
    room.furniture = room_data[2]
    room.objects = room_data[3]
    room.expected_words = room_data[4]
    room.expected_output = room_data[5]

set_up_room()

        
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
            return redirect(url_for('login'))
    
    username = session['user']
    user_data = get_user_data(username)

    inventory = room.objects
    user_level = level
    room_data = room
    print(f"Room data: {room_data}")

    msg = room.description

    
    if request.method == 'POST':
        command = request.form['command']
        msg = process(command, inventory, room)
            
    return render_template('home.html', msg=msg, inventory=inventory, user_level=user_level, room_data=room_data, username=username)


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
            return redirect(url_for('register'))

        # Register the user
        register_user(name, email, username, password, 1, 0, "")

        return redirect(url_for('login'))

    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid

        if check_login(username, password):
            session['user'] = username
            print("user logged in")
            return redirect(url_for('home'))
        else:
            msg = "Invalid login"
            print(f"Invalid login: {username}, {password}")
            

    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# -------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
