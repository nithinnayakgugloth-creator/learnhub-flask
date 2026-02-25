from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- TEMP USER STORAGE ----------------
users = []

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

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
        users.append({
            "username": request.form["username"],
            "password": request.form["password"]
        })
        return redirect("/login")
    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # ADMIN LOGIN
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")

        # USER LOGIN
        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                return redirect("/dashboard")

        return "Invalid Login"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html")
    return redirect("/login")

# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
def admin():
    if "admin" in session:
        return render_template("admin.html", users=users)
    return redirect("/login")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- COURSES ----------------
@app.route("/python")
def python_course():
    return render_template("python.html")

@app.route("/java")
def java_course():
    return render_template("java.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
