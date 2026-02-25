from flask import Flask, render_template, request, redirect, session


app = Flask(__name__)
app.secret_key = "secret123"
users = []



# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- COURSES ----------------
@app.route("/courses")
def courses():
    return render_template("courses.html")

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
        for user in users:
            if (
                user["username"] == request.form["username"]
                and user["password"] == request.form["password"]
            ):
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

