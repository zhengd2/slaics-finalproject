from os import abort
from flask import app, Flask, render_template, current_app, abort, request, flash, redirect, url_for, Blueprint, send_file, send_from_directory
from logic import read_sql
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, flash
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__) 
data = read_sql("data/data.db","data_1")
#conn = sqlite3.connect("data/data.sqlite3")
app.secret_key = os.getenv("SECRET_KEY")
users = read_sql("data/data.db" ,"users")


def get_db_connection():
    conn = sqlite3.connect("data/data.db")
    conn.row_factory = sqlite3.Row  # So we can access results like dicts
    return conn

@app.route("/")
def index():
    majors = sorted(set(record["Level and Field of Highest Degree"] for record in data))
    return render_template("index.html",data=data, majors=majors)
    
@app.route("/table")
def show_table():
    return render_template("table_view.html",data=data)

'''
@app.post("")
def submit_form():
    return render_template("", data=data)
'''

@app.post("/")
def college_by_name():
    min = 0
    max = 10000000000
    data2 = []
    if request.form["min_job_salary"]:
        min = int(request.form["min_job_salary"])
    if request.form["max_job_salary"]:
        max = int(request.form["max_job_salary"])

    for record in data:
        if request.form["college_major"]:
            if str(record["Median Salary"]).isdigit():
                if request.form["type"] == "All":
                    if (record["Level and Field of Highest Degree"] == request.form["college_major"] and  max >= int(record["Median Salary"]) and min <= int(record["Median Salary"])): data2.append(record)
                else:
                    if (record["Level and Field of Highest Degree"] == request.form["college_major"] and record["Type"] == request.form["type"] and max >= int(record["Median Salary"]) and min <= int(record["Median Salary"])): data2.append(record)
            else:
                if request.form["type"] == "All":
                    if (record["Level and Field of Highest Degree"] == request.form["college_major"]): data2.append(record)
                else:
                    if (record["Level and Field of Highest Degree"] == request.form["college_major"] and record["Type"] == request.form["type"]): data2.append(record)
                record["Median Salary"] = "N/A"
        else:
            if str(record["Median Salary"]).isdigit():
                if request.form["type"] == "All":
                    if (max >= int(record["Median Salary"]) and min <= int(record["Median Salary"])): data2.append(record)
                else:
                    if (record["Type"] == request.form["type"] and max >= int(record["Median Salary"]) and min <= int(record["Median Salary"])): data2.append(record)
            else:
                if request.form["type"] == "All":
                    record["Median Salary"] = "N/A"
                    data2.append(record)
                else:
                    if (record["Type"] == request.form["type"]): 
                        record["Median Salary"] = "N/A"
                        data2.append(record)

    if data2:
        major_name = request.form["college_major"]
        if max == 10000000000:
            max = "Infinite"
        if min == 0:
            min = "0"
        if request.form["college_major"] == False:
            major_name = "All Majors"
        return render_template("table_view.html", data=(data2), major_name=major_name, max=str(max), min=str(min), type =request.form["type"])
    return render_template("noresults.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("abort.html")


'''

@app.post("/login")
def logged_in():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash(f"Welcome, {user.name}")
        return redirect(url_for("main.index"))
    return render_template("login.html", form=form)

'''



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists.")
            conn.close()
            return redirect(url_for("signup"))

        conn.close()
        flash("Signup successful! You can now log in.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.context_processor
def username_in_all_html():
    return dict(username=session.get("username"), current_path=request.path)



#@app.route("/college_majors")
#def return_majors():
#read_csv("data/data_for_final.csv"




