from flask import Flask, render_template, request, redirect, flash, session
from cs50 import SQL
import os
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

db = SQL("sqlite:///main.db")
app.config.update(SECRET_KEY=os.urandom(24))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rapor_all")
def rapor():
    rapors = db.execute("SELECT * FROM rapor")
    return render_template("rapor-all.html", rapors=rapors)

@app.route("/input", methods=['POST', 'GET'])
def input():
    if request.method == "POST":
        nis = request.form.get("nis")
        nama = request.form.get("nama")
        mat = request.form.get("mat")
        bindo = request.form.get("bindo")
        big = request.form.get("big")
        pjok = request.form.get("pjok")
        ipas = request.form.get("ipas")
        rpl = request.form.get("rpl")

        db.execute("INSERT INTO rapor (nis, nama, nilai_mat, nilai_bindo, nilai_big, nilai_pjok, nilai_ipas, nilai_rpl) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", nis, nama, mat, bindo, big, pjok, ipas, rpl)
        return redirect("/input")
    else:
        return render_template("input.html")

@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    db.execute("delete from rapor where id = ?", id)
    return redirect("/rapor-all")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        data = db.execute("SELECT * FROM rapor WHERE id = ?", id)[0]
        print(data)
        return render_template("edit.html", data=data)
    elif request.method == "POST":
        nis = request.form.get("nis")
        nama = request.form.get("nama")
        mat = request.form.get("nilai_mat")
        bindo = request.form.get("nilai_bindo")
        big = request.form.get("nilai_big")
        pjok = request.form.get("nilai_pjok")
        ipas = request.form.get("nilai_ipas")
        rpl = request.form.get("nilai_rpl")
        db.execute('UPDATE rapor set nis = ?, nama = ?, nilai_mat = ?, nilai_bindo = ?, nilai_big = ?, nilai_pjok = ?, nilai_ipas = ?, nilai_rpl = ? where id = ?', nis, nama, mat, bindo, big, pjok, ipas, rpl, id)
        return redirect("/")
    
@app.route("/rapor_single/<id>", methods=["GET"])
def single(id):
    data = db.execute("SELECT * FROM rapor WHERE id = ?", id)[0]
    print(data)
    return render_template("rapor-single.html", data=data)

@app.route("/register", methods=['POST', 'GET'])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"
        rows = db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))

        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        rpassword = request.form.get("rpassword")

        hash = generate_password_hash(password)
        if len(rows) == 1:
            return "username already taken"
        if password == rpassword:
            db.execute("INSERT INTO user (username, name, password) VALUES(?, ?, ?)", username, name, hash)

            registered_user = db.execute("select * from user where username = ?", username)
            session["id"] = registered_user[0]["id"]
            flash("you were sucessfully registered")
            return redirect("/")
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return "Isikan username"
        elif not request.form.get("password"):
            return "Isikan password"
        rows = db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return "username atau password yang anda masukan salah"
        
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()
    return redirect("/")