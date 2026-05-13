from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    # Save task
    if request.method == "POST":

        task = request.form["task"]

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (task,)
        )

        conn.commit()
        conn.close()

    # Fetch tasks from database
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)