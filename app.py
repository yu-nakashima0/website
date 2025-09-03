from flask import Flask, request, render_template, redirect, session, redirect, url_for
from models import db, User, Video, Comment
from werkzeug.security import check_password_hash, generate_password_hash, check_password_hash
import base64
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
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
    username = session.get("username")
    if not username:
        return redirect("/login")

    user = db.session.query(User).filter_by(username=username).first()
    if user:
        return render_template("userpage.html", username=user.username)
    else:
        return redirect("/login")

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

        # check, ob der username schon benutzt oder nicht.
        if User.query.filter_by(username=username).first():
            return render_template("signup.html", error="このユーザー名は既に使われています")

        # hash generieren for password
        hashed_password = generate_password_hash(password)

        # add new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")  # go to login page

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            print("Hello")
            session["username"] = username  
            return redirect("/userpage")  
        else:
            print("Invalid credentials")
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/yutube", methods=["GET", "POST"])
def yutube():
    if request.method == "POST":
        file = request.files.get("video")
        if file:
            vid = Video(filename=file.filename, data=file.read())
            db.session.add(vid)
            db.session.commit()
        return redirect("/yutube")
    videos = Video.query.all()
    vids = [{
        "id": v.id,
        "filename": v.filename,
        "data_url": "data:video/mp4;base64," + base64.b64encode(v.data).decode()
    } for v in videos]
    comms = Comment.query.all()
    print(comms)
    return render_template("yutube.html", videos=vids, comments=comms)

@app.route("/add_comment/<int:video_id>", methods=["POST"])
def add_comment(video_id):
    comment_text = request.form.get("comment")
    print(f"Received comment for video_id {video_id}: {comment_text}")
    if video_id and comment_text:
        comment = Comment(video_id=video_id, comment_text=comment_text)
        db.session.add(comment)
        db.session.commit()
    return redirect("/yutube")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
