from flask import Flask, render_template, request, redirect, url_for, flash
from flask.globals import request
import sqlite3


conexion =sqlite3.connect("AlcesDatabase.db")
cursor = conexion.cursor()
cursor.execute('SELECT * FROM usuarios WHERE id_usuario=?', (1,))
data=cursor.fetchall()
for x in data:
    print(x)
conexion.commit()

import pandas as pd

app = Flask(__name__,
            static_url_path='',
            static_folder='templates',
            template_folder='templates')
user_list = pd.DataFrame({'nombre': ['diego', 'ethan', 'carolina', 'yendi', 'nellys'],
                          'email': ['diego@email.com', 'ethan@email.com', 'carolina@email.com', 'yendi@email.com',
                                    'nellys@email.com'], 'contraseña': ['123', '234', '456', '789', '246']})
publicaciones = pd.DataFrame({'nombre': ['diego', 'ethan', 'carolina', 'yendi', 'nellys'],
                              'publicacion': ['asdfkljas', 'sdf', 'wer', 'dsfasf', '435']})


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
        conexion =sqlite3.connect("AlcesDatabase.db")
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email=? and contraseña=?', (email,contraseña,))
        data=cursor.fetchall()
        for x in data:
            if len(x)>0:
            
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
        # conexion = connect("pwd.db")
        # cursor = conexion.cursor()
        # cursor.execute('SELECT contraseña FROM TABLA WHERE email = ?', email))
        return render_template('passwordRecovery.html', tables=[user_list.to_html(classes='data')],titles = user_list.columns.values)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        conexion = sqlite3.connect("AlcesDatabase.db")
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, email, contraseña) VALUES (?, ?, ?)',(nombre, email, contraseña,))
        
        cursor.execute('SELECT * FROM usuarios')
        data=cursor.fetchall()
        for x in data:
            print(x)
        conexion.commit()
        return redirect(url_for('login'))
    else:
        return render_template('Signup.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        email = request.form['email']

        if email in user_list.values:
            list = ['removido','removido','removido']
            # conexion = connect("pwd.db")
            # cursor = conexion.cursor()
            # cursor.execute('DELETE * FROM TABLA WHERE VALUES (?, ?, ?)', (nombre, email, contraseña,))
            user_list.loc[user_list['email'] == email] = list
            
            return redirect(url_for('login'))

    return render_template('admin.html')


# Eliminar un registro con el ingreso de un parametro id proveniente desde index.html
@app.route('/publicacion', methods=['GET', 'POST'])
def publicacion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        publicacion = request.form['publicacion']
        if publicacion not in publicaciones.values:
            print(publicaciones)
            try:
                request.form['agregar']

                list = [nombre, publicacion]
                # conexion = connect("pwd.db")
                # cursor = conexion.cursor()
                # cursor.execute('INSERT INTO TABLA VALUES (?, ?, ?)', (nombre, email, contraseña,))
                publicaciones.loc[len(user_list)] = list

                print(publicaciones)
            except:
                print('no se encontro publicacion')
        elif publicacion in publicaciones.values:
            try:

                request.form['remover']
                list = ['removido','removido']
                # conexion = connect("pwd.db")
                # cursor = conexion.cursor()
                # cursor.execute('DELETE * FROM TABLA WHERE VALUES (?, ?, ?)', (nombre, email, contraseña,))
                publicaciones.loc[publicaciones['publicacion'] == publicacion]= list
                print(publicaciones)
                return redirect(url_for('login'))
            except:
                request.form['agregar']

                list = [nombre, publicacion]
                # conexion = connect("pwd.db")
                # cursor = conexion.cursor()
                # cursor.execute('INSERT INTO TABLA VALUES (?, ?, ?)', (nombre, email, contraseña,))
                publicaciones.loc[len(user_list)] = list

                print(publicaciones)

    return render_template('PubDetallada.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
