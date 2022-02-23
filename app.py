from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from datetime import timedelta

from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://lewigolski:Rlawogur123!@cluster0.1vcre.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dblewigolski

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=30)

# 로그인페이지
@app.route("/")
def introduction():
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    return render_template("login.html")


@app.route("/register")
def registration():
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    return render_template("register.html")

@app.route("/registration", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    doc={
        "name": name,
        "email": email,
        "password": password,
        "mbti": ""
    }
    db.login.insert_one(doc)
    session["register"] = email
    return jsonify({'msg': "1차 회원가입 완료!"})

@app.route("/register/mbti")
def mbti():
    if "register" in session and "register_mbti" not in session:
        return render_template("mbti.html")
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    else:
        return redirect(url_for("registration"))

@app.route("/postmbti", methods=["POST"])
def postmbti():
    session["register_mbti"] = request.form["mbti"]
    register_mbti = session["register_mbti"]
    register_user = session["register"]
    db.login.update_one({"email": register_user},{'$set':{"mbti": register_mbti }})
    return redirect(url_for("user"))

@app.route("/login")
def login():
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    return render_template("login.html")

@app.route("/authentication", methods=["POST"])
def authentication():
    inputemail = request.form["email"]
    inputuser = db.login.find_one({"email": inputemail})
    if inputuser is not None:
        inputpassword = inputuser["password"]
        return jsonify({'msg': inputpassword})
    if inputuser is None:
        return jsonify({'msg': "not"})

@app.route("/loginsuccess", methods=["POST"])
def loginsuccess():
    user = request.form["email"]
    session["user"] = user
    return redirect(url_for("user"))

@app.route("/user")
def user():
    if "register" in session and "register_mbti" in session:
        mbti = session["register_mbti"]
        username = session["register"]
        return render_template("user.html", user=username, mbti=mbti)
    if "user" in session:
        username = session["user"]
        userdb = db.login.find_one({"email": username})
        usermbti = userdb["mbti"]
        return render_template("user.html", user=username, mbti=usermbti)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("register", None)
    session.pop("register_mbti", None)
    return redirect(url_for("login"))


# 여기서부터가 웹스크레핑 

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

