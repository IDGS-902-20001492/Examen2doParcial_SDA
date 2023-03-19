from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user,login_required, current_user
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User 
from . import db, UserDataStore

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #Consultamos si existe un usuario ya registrado con el email
    user = User.query.filter_by(email=email).first()

    #Verificamos si el usuario existe y comprobamos el password
        
    if not user or not check_password_hash(user.password, password):
        flash('El usuario y/o contraseña son incorrectos')
        return redirect(url_for('auth.login')) #Retomamos al login
    
    #Si llegamos aqui los datos son correctos
    #Creamos una sesion y logearemos 
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    #Consultamos si existe un usuario ya registrado con el email
    user = User.query.filter_by(email=email).first()

    if user:
        flash("El correo electronico ya está en uso")
        return redirect(url_for('auth.signup'))
    
    #Creamos un nuevo usuario
    UserDataStore.create_user(name=name,
                               email=email, password=generate_password_hash(password,method='sha256'))
    
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
        #Cerramos la sesion
        logout_user()
        return redirect(url_for('main.index'))