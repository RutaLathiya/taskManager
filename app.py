from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    # Save task
    if request.method == "POST":

        task = request.form["task"]
        priority = request.form["priority"]

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO tasks (title, priority) VALUES (?, ?)",
            (task, priority)
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

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
        
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))

        conn.commit()
        conn.close()

        return redirect("/")
    
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == "POST":
        task = request.form["task"]
        priority = request.form["priority"]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE tasks SET title=?, priority=? WHERE id=?", (task, priority, task_id))
        conn.commit()
        conn.close()
        return redirect("/")

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = cursor.fetchone()

    conn.close()
    return render_template("edit.html", task=task)

@app.route("/complete/<int:task_id>")
def toggle_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT completed FROM tasks WHERE id=?", (task_id,))
    completed = cursor.fetchone()[0]

    new_status = 0 if completed else 1

    cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (new_status, task_id))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)