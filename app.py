from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "supersecret"

# DATABASE CONNECTION
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/")
def home():
    return render_template("index.html")
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

if __name__ == "__main__":
    app.run(debug=True)

