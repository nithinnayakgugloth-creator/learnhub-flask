from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- MYSQL CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2005",   
    database="learnhub"
)

cursor = db.cursor(dictionary=True)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- COURSES ----------------
@app.route("/courses")
def courses():
    return render_template("courses.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()
            return redirect("/login")
        except:
            return "Username already exists"

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            session["user"] = user["username"]
            return redirect("/dashboard")

        return "Invalid Login"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", username=session["user"])
    return redirect("/login")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ---------------- PYTHON COURSE ----------------
@app.route("/python")
def python_course():
    return render_template("python.html")

# ---------------- JAVA COURSE ----------------
@app.route("/java")
def java_course():
    return render_template("java.html")

# ---------------- QUIZ ----------------
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)