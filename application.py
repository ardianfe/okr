from flask import Flask, render_template, request, session, redirect, g, url_for
from datetime import datetime
import os
from models import *


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") #export DATABASE_URL=postgresql://localhost/okr
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        session.pop('email', None)
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if password == user.password:
            session['email'] = email
            return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if g.user:
        user = User.query.filter_by(email=g.user).first()
        user_id = user.id
        user_name = user.name
        okrs = Okr.query.filter_by(user_id=user.id)
        kresults = KeyResult.query.all()
        progress_krs = ProgressKr.query.all()
        return render_template("dashboard.html", okrs=okrs, kresults=kresults, user_id=user_id, user_name=user_name, progress_krs=progress_krs)
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    if 'email' in session:
        g.user = session['email']

@app.route("/register", methods=['GET','POST'])
def add_team():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        user = User(email=email, password=password, name=name)
        db.session.add(user)
        db.session.commit()
        return render_template("success.html")
    return render_template("register.html")


@app.route("/user/<int:user_id>/okr", methods=['POST'])
def okr(user_id):
    if request.method == 'POST':
        objective = request.form.get("okr")
        user_id = user_id
        save_okr = Okr(objective=objective, user_id=user_id)
        db.session.add(save_okr)
        db.session.commit()
        return redirect(url_for('dashboard'))
    
@app.route("/addkr/<int:okr_id>", methods=['POST'])
def add_kr(okr_id):
    okr = Okr.query.get(okr_id)
    key_result = request.form.get("key_result")
    save_kr = KeyResult(indicator = key_result, okr_id = okr_id)
    db.session.add(save_kr)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/detailkr/<int:okr_id>")
def input_progress_kr(okr_id):
    okr = Okr.query.get(okr_id)
    k_results = KeyResult.query.filter_by(okr_id=okr.id)
    return render_template('teams.html', okr=okr, k_results=k_results)

@app.route("/progresskr/<int:kr_id>", methods=['POST'])
def progress_kr(kr_id):
    if request.method == 'POST':
        kr_id = kr_id
        create_at = datetime.now()
        progress = request.form.get("progress")
        save_progress = ProgressKr(create_at=create_at, progress=progress, kr_id=kr_id)
        db.session.add(save_progress)
        db.session.commit()
        return render_template ('success.html')



