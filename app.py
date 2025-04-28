
from flask import Flask, render_template_string, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# In-memory user store (for demo purposes)
users = {}

# Shared CSS styles
styles = """
<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(to right, #3f87a6, #153559);
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}
.container {
    background: rgba(255, 255, 255, 0.1);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    text-align: center;
}
input {
    display: block;
    margin: 10px auto;
    padding: 10px;
    width: 80%;
    border: none;
    border-radius: 5px;
}
button {
    background: #1e3c72;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.circle-gradient {
    position: absolute;
    top: -60px;
    left: -60px;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: radial-gradient(circle, #3f87a6, #153559);
}
.square-gradient {
    position: absolute;
    bottom: -60px;
    right: -60px;
    width: 100px;
    height: 100px;
    border-radius: 10px;
    background: linear-gradient(45deg, #1e3c72, #2a5298);
}
.lock-icon {
    font-size: 30px;
    margin-bottom: 10px;
}
</style>
"""

# Home Route
@app.route('/')
def home():
    if 'username' in session:
        return render_template_string(styles + """
        <div class="container">
            <div class="lock-icon">🔒</div>
            <h2>Welcome, {{username}}</h2>
            <p>This is a protected page.</p>
            <a href="{{ url_for('logout') }}"><button>Logout</button></a>
        </div>
        <div class="circle-gradient"></div>
        <div class="square-gradient"></div>
        """, username=session['username'])
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = generate_password_hash(request.form['password'])
        users[uname] = pwd
        return redirect(url_for('login'))
    return render_template_string(styles + """
    <div class="container">
        <div class="lock-icon">🔐</div>
        <h2>Register</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
        <p>Already have an account? <a href="/login">Login</a></p>
    </div>
    <div class="circle-gradient"></div>
    <div class="square-gradient"></div>
    """)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user_pwd_hash = users.get(uname)
        if user_pwd_hash and check_password_hash(user_pwd_hash, pwd):
            session['username'] = uname
            return redirect(url_for('home'))
        else:
            return render_template_string(styles + """
            <div class="container">
                <h2>Login Failed</h2>
                <p>Invalid credentials.</p>
                <a href="/login"><button>Try Again</button></a>
            </div>
            """)
    return render_template_string(styles + """
    <div class="container">
        <div class="lock-icon">🔒</div>
        <h2>Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="/register">Register</a></p>
    </div>
    <div class="circle-gradient"></div>
    <div class="square-gradient"></div>
    """)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
