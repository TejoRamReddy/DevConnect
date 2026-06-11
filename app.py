import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')
)
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ── Models ──────────────────────────────────────────────────────────────────

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)   # longer for hash


class Project(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(100))
    description   = db.Column(db.Text)
    skills        = db.Column(db.String(200))
    owner         = db.Column(db.String(80))
    workspace_url = db.Column(db.String(200), default="https://github.com")


class JoinRequest(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    project_id    = db.Column(db.Integer)
    project_title = db.Column(db.String(100))
    sender        = db.Column(db.String(80))
    owner         = db.Column(db.String(80))
    status        = db.Column(db.String(20), default='Pending')


with app.app_context():
    db.create_all()


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username'].strip()
        pwd   = request.form['password']

        # Basic validation
        if len(uname) < 3 or len(uname) > 80:
            flash("Username must be 3–80 characters.")
            return redirect(url_for('register'))
        if len(pwd) < 6:
            flash("Password must be at least 6 characters.")
            return redirect(url_for('register'))

        if User.query.filter_by(username=uname).first():
            flash("Username already exists!")
            return redirect(url_for('register'))

        hashed = generate_password_hash(pwd)
        db.session.add(User(username=uname, password=hashed))
        db.session.commit()
        flash("Account created! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username'].strip()
        pwd   = request.form['password']
        user  = User.query.filter_by(username=uname).first()

        if user and check_password_hash(user.password, pwd):
            session['user'] = user.username
            return redirect(url_for('dashboard'))

        flash("Invalid credentials. Please try again.")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    projects     = Project.query.all()
    incoming     = JoinRequest.query.filter_by(owner=session['user'], status='Pending').all()
    accepted     = JoinRequest.query.filter_by(status='Accepted').all()
    my_requests  = JoinRequest.query.filter_by(sender=session['user']).all()

    return render_template(
        'dashboard.html',
        user=session['user'],
        projects=projects,
        incoming=incoming,
        all_accepted=accepted,
        my_requests=my_requests
    )


@app.route('/post_project', methods=['POST'])
def post_project():
    if 'user' not in session:
        return redirect(url_for('login'))

    title       = request.form['title'].strip()[:100]
    description = request.form['description'].strip()[:2000]
    skills      = request.form['skills'].strip()[:200]

    if not title or not description or not skills:
        flash("All fields are required.")
        return redirect(url_for('dashboard'))

    db.session.add(Project(
        title=title,
        description=description,
        skills=skills,
        owner=session['user']
    ))
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/join/<int:pid>/<owner>/<title>')
def join_project(pid, owner, title):
    if 'user' not in session:
        return redirect(url_for('login'))

    # Can't join your own project
    if owner == session['user']:
        return redirect(url_for('dashboard'))

    already = JoinRequest.query.filter_by(project_id=pid, sender=session['user']).first()
    if not already:
        db.session.add(JoinRequest(
            project_id=pid,
            project_title=title[:100],
            sender=session['user'],
            owner=owner
        ))
        db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/handle/<int:rid>/<action>')
def handle_request(rid, action):
    if 'user' not in session:
        return redirect(url_for('login'))

    req = db.session.get(JoinRequest, rid)

    # Only the owner of that project can act on requests
    if req and req.owner == session['user']:
        if action == 'accept':
            req.status = 'Accepted'
        elif action == 'decline':
            req.status = 'Declined'
        db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/delete_project/<int:pid>', methods=['POST'])
def delete_project(pid):
    if 'user' not in session:
        return redirect(url_for('login'))

    project = db.session.get(Project, pid)
    if project and project.owner == session['user']:
        # Also remove related join requests
        JoinRequest.query.filter_by(project_id=pid).delete()
        db.session.delete(project)
        db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)