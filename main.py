from flask import Flask, request, render_template_string
import sqlite3
import subprocess

app = Flask(__name__)

# --- Initialize SQLite DB ---
def init_db():
    conn = sqlite3.connect('vulnapp.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT,
            bio TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- Home Page ---
@app.route('/')
def home():
    return '''
        <h2>Welcome to Insecure App</h2>
        <ul>
            <li><a href="/register">Register</a></li>
            <li><a href="/login">Login</a></li>
            <li><a href="/user?id=1">User Info (SQLi)</a></li>
            <li><a href="/exec">Run OS Command (RCE)</a></li>
            <li><a href="/profile?username=admin">View Profile (XSS)</a></li>
        </ul>
    '''

# --- Register Route (SQLi) ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        email = request.form['email']
        bio = request.form['bio']

        conn = sqlite3.connect('vulnapp.db')
        cur = conn.cursor()
        # SQLi vulnerable query
        query = f"INSERT INTO users (username, password, email, bio) VALUES ('{uname}', '{passwd}', '{email}', '{bio}')"
        cur.execute(query)
        conn.commit()
        conn.close()
        return "Registration successful"
    
    return '''
        <h3>Register</h3>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            Email: <input name="email"><br>
            Bio: <textarea name="bio"></textarea><br>
            <input type="submit" value="Register">
        </form>
    '''

# --- Login Route (SQLi) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username')
        passwd = request.form.get('password')

        conn = sqlite3.connect('vulnapp.db')
        cur = conn.cursor()
        # SQL Injection vulnerability
        sql = f"SELECT * FROM users WHERE username = '{uname}' AND password = '{passwd}'"
        cur.execute(sql)
        user = cur.fetchone()
        conn.close()

        if user:
            return f"Welcome {uname}!"
        return "Login failed"

    return '''
        <h3>Login</h3>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# --- User Info (SQLi) ---
@app.route('/user')
def user_info():
    uid = request.args.get('id', '1')
    conn = sqlite3.connect('vulnapp.db')
    cur = conn.cursor()
    # SQLi again
    cur.execute(f"SELECT username, email FROM users WHERE id = {uid}")
    row = cur.fetchone()
    conn.close()

    if row:
        return f"<h3>User Info</h3><p>Username: {row[0]}<br>Email: {row[1]}</p>"
    return "User not found"

# --- Command Execution (RCE) ---
@app.route('/exec', methods=['GET', 'POST'])
def execute_command():
    if request.method == 'POST':
        cmd = request.form['cmd']
        try:
            # Remote Code Execution
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5)
            return f"<pre>{output.decode()}</pre>"
        except Exception as e:
            return f"<pre>Error: {e}</pre>"

    return '''
        <h3>Execute OS Command</h3>
        <form method="POST">
            Command: <input name="cmd"><br>
            <input type="submit" value="Run">
        </form>
    '''

# --- Profile Page (XSS) ---
@app.route('/profile')
def profile():
    username = request.args.get('username', '')
    conn = sqlite3.connect('vulnapp.db')
    cur = conn.cursor()
    cur.execute(f"SELECT bio FROM users WHERE username = '{username}'")
    row = cur.fetchone()
    conn.close()

    bio = row[0] if row else "No bio found"
    # XSS vulnerability: unsafe rendering
    return render_template_string(f"<h2>Profile: {username}</h2><p>Bio: {bio}</p>")

# --- Start App ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
