from flask import Flask, render_template, request, redirect, url_for, flash
from flask.globals import request
import sqlite3
import re




app = Flask(__name__,
            static_url_path='',
            static_folder='templates',
            template_folder='templates')



@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':

        return render_template('Main.html')
    elif request.method == 'POST':
        if 'register' in request.form:

            return redirect(url_for('signup'))
        elif 'login' in request.form:
            return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form["mail"]
        contraseña = request.form["contraseña"]
        conexion = sqlite3.connect("AlcesDatabase.db")
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email=? and contraseña=?', (email, contraseña,))
        data = cursor.fetchall()
        for x in data:
            if len(x) > 0:

                return redirect(url_for('feed'))
            else:
                return render_template('login.html')

    return render_template('login.html')


@app.route('/feed', methods=['POST', 'GET'])
def feed():
    nombre = request.form.get("nombre")
    contraseña = request.form.get('contraseña')
    return render_template('Feed.html')


@app.route('/passwordRecovery')
def recovery():
    if request.method == 'POST':
        mail = request.form['mail']
        conexion = sqlite3.connect("AlcesDatabase.db")
        cursor = conexion.cursor()
        cursor.execute('SELECT contraseña FROM usuarios WHERE email = ?', mail,)
        data = cursor.fetchall()
        for i in data:
            x = i
            return render_template('passwordRecovery.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        while True:
            nombre = request.form['nombre']
            email = request.form['email']
            contraseña = request.form['contraseña']
            if len(contraseña) < 8:
                render_template('Signup.html')
            elif re.search('[0-9]', contraseña) is None:
                render_template('Signup.html')
            elif re.search('[A-Z]', contraseña) is None:
                render_template('Signup.html')
            else:
                break
        conexion = sqlite3.connect("AlcesDatabase.db")
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, email, contraseña) VALUES (?, ?, ?)',
                       (nombre, email, contraseña,))
        conexion.commit()
        return redirect(url_for('login'))
    else:
        return render_template('Signup.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        email = request.form['email']

        conexion = sqlite3.connect("AlcesDatabase.db")
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', email)
        data = cursor.fetchall()
        for x in data:
            if len(x) > 0:

                cursor.execute('DELETE FROM usuarios WHERE email = ?', email)
                conexion.commit()
                return redirect(url_for('feed'))

            return redirect(url_for('login'))

    return render_template('admin.html')



@app.route('/publicacion', methods=['GET', 'POST'])
def publicacion():
    if request.method == 'POST':
        #nombre = request.form['nombre']
        publicacion = request.form['publicacion']
        conexion = sqlite3.connect("AlcesDatabase.db")
        cursor = conexion.cursor()
        cursor.execute('SELECT count(*) FROM comentarios WHERE texto = ?', publicacion)
        for i in cursor.fetchall():
            print(i)

            if i[0]!=0:



                try:
                    request.form['agregar']
                    conexion = sqlite3.connect("AlcesDatabase.db")
                    cursor = conexion.cursor()
                    cursor.execute('INSERT INTO comentarios (texto) VALUES ?;', (publicacion,))
                    conexion.commit()

                except:
                    print('no se encontro publicacion')
            else:
                try:

                    request.form['remover']

                    conexion = sqlite3.connect("AlcesDatabase.db")
                    cursor = conexion.cursor()
                    cursor.execute('DELETE FROM comentarios (texto) WHERE VALUES (?)', (publicacion,))
                    conexion.commit()
                    return redirect(url_for('login'))
                except:
                    print('ok')

    return render_template('PubDetallada.html')



if __name__ == '__main__':
    app.run(port=3000, debug=True)
