from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from datetime import timedelta

from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://lewigolski:Rlawogur123!@cluster0.1vcre.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dblewigolski

app = Flask(__name__)

# 세션을 사용하려면 시크릿 키가 필요하다 (기본세팅)
app.secret_key = "hello"
# 세션이 유저의 브라우저에 저장되는 시간, 이후 자동 로그아웃이 된다 
app.permanent_session_lifetime = timedelta(minutes=30)

# 현재 기본 페이지를 로그인 페이지로 설정함 
# 이후 따로 로그인전 앱을 소개하는 페이지로 대체하고자함 
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

# 로그인 페이지 
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

# 로그인시 데이터베이스에서 확인하는 기능 
@app.route("/authentication", methods=["POST"])
def authentication():
    inputemail = request.form["email"]
    inputuser = db.login.find_one({"email": inputemail})
    if inputuser is not None:
        inputpassword = inputuser["password"]
        return jsonify({'msg': inputpassword})
    if inputuser is None:
        return jsonify({'msg': "not"})

# 로그인 성공시 세션을 만들고, 이 세션 키 (user)로 홈페이지 (/user) 로 접속가능하게 한다 
@app.route("/loginsuccess", methods=["POST"])
def loginsuccess():
    user = request.form["email"]
    session["user"] = user
    return redirect(url_for("user"))


# 회원가입 페이지 
@app.route("/registration")
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

# 회원가입 기능 (1차)
@app.route("/register", methods=["POST"])
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

# 2차 회원가입 MBTI 선택할수 있는 페이지 
@app.route("/registration/mbti")
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

# 2차 회원가입 페이지에서 MBTI를 정하면 데이터베이스에 저장되는 기능 
# 바로 홈페이지 (/user)로 이동하게 된다 (즉, 새로 로그인 안해도 된다) 
@app.route("/postmbti", methods=["POST"])
def postmbti():
    session["register_mbti"] = request.form["mbti"]
    register_mbti = session["register_mbti"]
    register_user = session["register"]
    db.login.update_one({"email": register_user},{'$set':{"mbti": register_mbti }})
    return redirect(url_for("user"))



# 홈페이지: 로그인 또는 회원가입을 완료했을때만 접속이 가능하다 
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

# 로그아웃 기능: 모든 세션을 지운다 
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("register", None)
    session.pop("register_mbti", None)
    return redirect(url_for("login"))


# 여기서부터가 웹스크레핑 





# 포트는 5000으로 설정했다 
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

