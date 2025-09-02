from flask import Flask, request, render_template, redirect
from models import db, User
from werkzeug.security import check_password_hash, generate_password_hash, check_password_hash



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("home.html")
    
@app.route('/secret')
def secret():
    return render_template("secret.html")

@app.route('/irgendwas')
def iw():
    return render_template("irgendwas.html")

@app.route('/About')
def about():
    return render_template("About.html")

@app.route('/login')
def l_i():
    return render_template("login.html")

@app.route('/signup')
def s_u():
    return render_template("signup.html")

@app.route("/userpage")
def userpage():
    return render_template("userpage.html")

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # すでにユーザー名が存在するか確認
        if User.query.filter_by(username=username).first():
            return render_template("signup.html", error="このユーザー名は既に使われています")

        # パスワードをハッシュ化して保存
        hashed_password = generate_password_hash(password)

        # 新しいユーザーを追加
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")  # サインアップ後ログインページへ

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Go to userpage.html instead of redirecting to "/"
            return render_template("userpage.html", username=username)
        else:
            error = "username or password are wrong"
            return render_template("login.html", error=error)
    return render_template("login.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0")
