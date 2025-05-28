from flask import Flask, session, redirect, url_for, render_template_string
from edo import ADMIN_USERNAME, users, posts

app = Flask(__name__)
app.secret_key = 'adminpanel_secret_key'

admin_panel_template = """
<!doctype html>
<title>Admin Panel</title>
<h1>Admin Panel</h1>
{% if is_admin %}
    <p>Welcome, {{ admin_username }}! You have administrator access.</p>
    <h2>Registered Users</h2>
    <ul>
    {% for user in users %}
        <li>{{ user }}</li>
    {% endfor %}
    </ul>
    <h2>Posts</h2>
    <ul>
    {% for post in posts %}
        <li><b>{{ post['user'] }}</b>: {{ post['content'] }}</li>
    {% endfor %}
    </ul>
{% else %}
    <p>Access denied. You are not the administrator.</p>
{% endif %}
<a href="/">Back to Home</a>
"""

@app.route('/admin')
def admin_panel():
    is_admin = session.get('username') == ADMIN_USERNAME
    return render_template_string(
        admin_panel_template,
        is_admin=is_admin,
        admin_username=ADMIN_USERNAME,
        users=users.keys(),
        posts=posts
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
