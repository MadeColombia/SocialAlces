from types import MethodDescriptorType
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.globals import request
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method=='POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        flash('contacto agregado satisfactoriamente')
        return redirect(url_for('Main'))
    return 'add contact'


@app.route('/login')
def login(id):
   
    return render_template('login.html')



@app.route('/admin/<id>')
def admin(id):
   
    return render_template('admin.html')

@app.route('/feed/<id>')
def feed(id):
   
    return render_template('feed.html')


#Actualizando contactos provenientes del formulario de edit_contact
@app.route('/poster/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
      
        flash ('contacto actualizado')
        return redirect(url_for('Main'))


#Eliminar un registro con el ingreso de un parametro id proveniente desde index.html
@app.route('/PubDetallada/<string:id>')
def delete_contact(id):
   
    flash('Usuario eliminado')
    return redirect(url_for('home'))

    
if __name__=='__main__':
    app.run(port = 3000,debug = True)