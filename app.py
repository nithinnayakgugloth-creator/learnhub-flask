from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ================= DATABASE CONNECTION =================

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# ================= CREATE TABLES (TEMPORARY) =================

@app.route("/create_tables")
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        role VARCHAR(20) DEFAULT 'user'
    );
    """)

    # COURSES TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT
    );
    """)

    # ENROLLMENTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

    return "Tables created!"

# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")

# ================= SIGNUP =================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, password)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")

# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, role FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[1]
            return redirect("/dashboard")

        return "Invalid login"

    return render_template("login.html")

# ================= LOGOUT =================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= COURSES =================

@app.route("/courses")
def courses():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM courses")
    all_courses = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("courses.html", courses=all_courses)

# ================= ENROLL =================

@app.route("/enroll/<int:course_id>")
def enroll(course_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()

    # Prevent duplicate enrollment
    cur.execute("""
        SELECT * FROM enrollments
        WHERE user_id=%s AND course_id=%s
    """, (session["user_id"], course_id))

    existing = cur.fetchone()

    if not existing:
        cur.execute(
            "INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)",
            (session["user_id"], course_id)
        )
        conn.commit()

    cur.close()
    conn.close()

    return redirect("/dashboard")

# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT courses.id, courses.title, courses.description
        FROM courses
        JOIN enrollments ON courses.id = enrollments.course_id
        WHERE enrollments.user_id = %s
    """, (session["user_id"],))

    enrolled_courses = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("dashboard.html", courses=enrolled_courses)

# ================= ADMIN ADD COURSE =================

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "role" not in session or session["role"] != "admin":
        return "Access Denied"

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO courses (title, description) VALUES (%s, %s)",
            (title, description)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/courses")

    return render_template("admin.html")
@app.route("/create_tables")
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

    return "Tables created!"
# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)


