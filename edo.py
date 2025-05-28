from flask import Flask, render_template_string, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'aws:servicecatalog:applicationName'

# In-memory "database"
users = {}
posts = []

home_template = """
<!doctype html>
<title>EDOBOLT</title>
<h1>Welcome to EDOBOLT</h1>
<p>Your platform, your game updates</p>
{% if 'username' in session %}
        <p>Logged in as {{ session['username'] }} | <a href="{{ url_for('logout') }}">Logout</a></p>
        <form method="post" action="{{ url_for('post') }}">
        <textarea name="content" placeholder="Share your game update..." required></textarea><br>
        <button type="submit">Post</button>
    </form>
{% else %}
    <a href="{{ url_for('login') }}">Login</a> | <a href="{{ url_for('register') }}">Register</a>
{% endif %}
<hr>
<h2>Posts</h2>
{% for post in posts %}
    <div>
        <b>{{ post['user'] }}</b>: {{ post['content'] }}
    </div>
{% else %}
    <p>No posts yet.</p>
{% endfor %}
"""

auth_template = """
<!doctype html>
<title>{{ title }}</title>
<h1>{{ title }}</h1>
<form method="post">
    Username: <input name="username" required><br>
    Password: <input name="password" type="password" required><br>
    <button type="submit">{{ title }}</button>
</form>
<a href="{{ url_for('home') }}">Back</a>
"""

@app.route('/')
def home():
        return render_template_string(home_template, posts=reversed(posts))

@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if username in users:
                        return "Username already exists. <a href='/register'>Try again</a>"
                users[username] = password
                session['username'] = username
                return redirect(url_for('home'))
        return render_template_string(auth_template, title="Register")

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if users.get(username) == password:
                        session['username'] = username
                        return redirect(url_for('home'))
                return "Invalid credentials. <a href='/login'>Try again</a>"
        return render_template_string(auth_template, title="Login")

@app.route('/logout')
def logout():
        session.pop('username', None)
        return redirect(url_for('home'))

@app.route('/post', methods=['POST'])
def post():
        if 'username' not in session:
                return redirect(url_for('login'))
        content = request.form['content']
        posts.append({'user': session['username'], 'content': content})
        return redirect(url_for('home'))

if __name__ == '__main__':
        app.run(debug=True)