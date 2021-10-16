from types import MethodDescriptorType
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.globals import request
from flask_mysqldb import MySQL
import pandas as pd

app = Flask(__name__,
            static_url_path='', 
            static_folder='templates',
            template_folder='templates')
user_list = pd.DataFrame({'nombre':['diego','ethan','carolina','yendi','nellys'], 'email':['diego@email.com','ethan@email.com','carolina@email.com','yendi@email.com','nellys@email.com'], 'contraseña': ['123','234','456','789','246']})


@app.route('/', methods = ['POST','GET'])

def home():
    if request.method=='GET':
 
        return render_template('Main.html')
    elif request.method == 'POST':
        if 'register' in request.form:
        
            
            return render_template('Signup.html')
        elif 'login' in request.form:
            return render_template('login.html')


    


  

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form["mail"]
        contraseña = request.form["contraseña"]
        if email and contraseña in user_list.values:
            print(email,contraseña)
            return redirect(url_for('feed'))
        else:
            return render_template('login.html')

    return render_template('login.html')
    

@app.route('/feed', methods = ['POST','GET'])
def feed():
    nombre = request.form.get("nombre")
    contraseña = request.form.get('contraseña')
    return render_template('Feed.html')

@app.route('/passwordRecovery')
def recovery():
    
    return render_template('passwordRecovery.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        list=[nombre,email,contraseña]
        user_list.loc[len(user_list)] = list
        return redirect(url_for('login'))
    else:
        return render_template('Signup.html')






@app.route('/admin')
def admin():
   
    return render_template('admin.html')





#Eliminar un registro con el ingreso de un parametro id proveniente desde index.html
@app.route('/PubDetallada')
def pubDetallada():
   
    
    return redirect(url_for('home'))

    
if __name__=='__main__':
    app.run(port = 3000,debug = True)