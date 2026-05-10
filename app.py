import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "devconnect_2026_key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    skills = db.Column(db.String(100))
    owner = db.Column(db.String(80))
    workspace_url = db.Column(db.String(200), default="https://github.com")

class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer)
    project_title = db.Column(db.String(100))
    sender = db.Column(db.String(80))
    owner = db.Column(db.String(80))
    status = db.Column(db.String(20), default='Pending')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if User.query.filter_by(username=uname).first():
            flash("Username already exists!")
            return redirect(url_for('register'))
        new_user = User(username=uname, password=pwd)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user = User.query.filter_by(username=uname, password=pwd).first()
        if user:
            session['user'] = uname
            return redirect(url_for('dashboard'))
        flash("Invalid Credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    projects = Project.query.all()
    incoming = JoinRequest.query.filter_by(owner=session['user']).all()
    accepted = JoinRequest.query.filter_by(status='Accepted').all()
    return render_template('dashboard.html', user=session['user'], projects=projects, incoming=incoming, all_accepted=accepted)

@app.route('/post_project', methods=['POST'])
def post_project():
    new_p = Project(
        title=request.form['title'],
        description=request.form['description'],
        skills=request.form['skills'],
        owner=session['user']
    )
    db.session.add(new_p)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/join/<int:pid>/<owner>/<title>')
def join_project(pid, owner, title):
    if not JoinRequest.query.filter_by(project_id=pid, sender=session['user']).first():
        db.session.add(JoinRequest(project_id=pid, project_title=title, sender=session['user'], owner=owner))
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/handle/<int:rid>/<action>')
def handle_request(rid, action):
    req = JoinRequest.query.get(rid)
    req.status = 'Accepted' if action == 'accept' else 'Rejected'
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)