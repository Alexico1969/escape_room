from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from database import connector, check_login, register_user, rooms

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SESSION_TYPE'] = 'filesystem'

db = connector()
print(db)

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
            return redirect(url_for('login'))
    
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid

        if check_login(username, password):
            flash('Username already exists')
            return redirect(url_for('register'))

        # Register the user
        register_user(name, email, username, password, 1, 0, "")

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid

        if check_login(username, password):
            session['user'] = username
            return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# -------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
