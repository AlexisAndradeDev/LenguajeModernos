from flask import request, render_template, redirect, url_for
import pymysql
from app import app
from dbconfig import mysql

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear', methods=['POST'])
def add_task():
    conn = None
    cursor = None
    try:
        _task = request.form['task']
        _description = request.form['description']
        if _task and _description:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "INSERT INTO Tareas(task, description) VALUES(%s, %s)"
            cursor.execute(sql, (_task, _description))
            conn.commit()
            return redirect(url_for('task_added', task=_task, description=_description))
        else:
            return 'Hubo un error al crear la tarea. No se pudo obtener la tarea o la descripción.'
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/creada')
def task_added():
    task = request.args.get('task')
    description = request.args.get('description')
    return render_template('task_added.html', task=task, description=description)

if __name__ == "__main__":
    app.run()

