from flask import request, render_template, redirect, url_for
import pymysql
from app import app
from dbconfig import mysql
import sys

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear', methods=['POST'])
def add_task():
    conn = None
    cursor = None
    try:
        task = request.form['task']
        description = request.form['description']
        if task and description:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "INSERT INTO Tareas(task, description) VALUES(%s, %s)"
            cursor.execute(sql, (task, description))
            conn.commit()
            return redirect(url_for('task_added', task=task, description=description))
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
    return render_template('tarea_creada.html', task=task, description=description)

@app.route('/tareas')
def get_tasks():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Tareas")
        tasks = cursor.fetchall()
        return render_template('tareas.html', tareas=tasks)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/eliminar/<int:id>')
def delete_task(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM Tareas WHERE id = %s", (id,))
        conn.commit()
        return redirect(url_for('get_tasks'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            task = request.form['task']
            description = request.form['description']
            if task and description:
                cursor.execute("UPDATE Tareas SET task = %s, description = %s WHERE id = %s", (task, description, id))
                conn.commit()
                return redirect(url_for('get_tasks'))
            else:
                return 'Hubo un error al actualizar la tarea. No se pudo obtener la tarea o la descripción.'
        else:
            cursor.execute("SELECT * FROM Tareas WHERE id = %s", (id,))
            row = cursor.fetchone()
            return render_template('editar_tarea.html', tarea=row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    args = sys.argv
    # ejecutar en modo debug
    debug_on = False
    if "-debug" in args:
        debug_on = True
        args.remove("-debug")
    
    app.run(debug=debug_on)