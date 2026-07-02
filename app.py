import sqlite3
import sys
import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
DB_FILE = os.environ.get("DB_FILE", "meals.db")
# Initializes the DB
def init_db():
    db_dir = os.path.dirname(DB_FILE)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_name TEXT NOT NULL,
            meal_date TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()

init_db()

# Runs the website
@app.route("/", methods=["GET", "POST"])
def index():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT id, meal_name, meal_date FROM meals")
    all_meals = cur.fetchall()
    
    cur.close()
    con.close()

    return render_template("index.html", meals=all_meals)
@app.route("/add_meal", methods=["POST"])
# Sends meal data to DB
def submit():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    meal_name_received = request.form.get("meal_name")
    meal_date_received = request.form.get("meal_date")
    if meal_name_received and meal_date_received:
        cur.execute("INSERT INTO meals (meal_name, meal_date) VALUES (?, ?)", (meal_name_received, meal_date_received))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for('index'))
    
    cur.close()
    con.close()
    return "Error: Missing form entries", 400
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
