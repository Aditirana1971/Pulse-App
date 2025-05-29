from flask import Flask, render_template, request
import sqlite3
from datetime import date

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS checkins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    checkin_date TEXT,
                    mood TEXT,
                    workout TEXT
                )""")
    conn.commit()
    conn.close()

def suggest_workout(mood):
    workouts = {
        "energized": "HIIT Blast – 20 mins",
        "okay": "Cardio Core – 15 mins",
        "meh": "Stretch + Breath – 10 mins",
        "tired": "Mindful Walk or Light Yoga – 5 mins"
    }
    return workouts.get(mood, "Gentle Stretch – 5 mins")

@app.route("/", methods=["GET", "POST"])
def index():
    today = date.today().isoformat()
    if request.method == "POST":
        mood = request.form.get("mood")
        workout = suggest_workout(mood)
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO checkins (checkin_date, mood, workout) VALUES (?, ?, ?)",
                  (today, mood, workout))
        conn.commit()
        conn.close()
        return render_template("index.html", submitted=True, mood=mood, workout=workout)
    return render_template("index.html", submitted=False)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
