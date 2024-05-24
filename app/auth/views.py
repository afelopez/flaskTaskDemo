from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash,  check_password_hash
from app.forms import LoginForm
from . import auth

from app.firestore_service import get_user, put_user
from app.models import UserModel, UserDTO

@auth.route('/login', methods=["GET", "POST"])
def login():

    login_form = LoginForm()

    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        user_doc = get_user(username)
        
        if user_doc.to_dict() is not None:
            password_doc = user_doc.to_dict()['password']            
            
            if check_password_hash(password_doc, password):
                user_dto = UserDTO(username, password)
                user = UserModel(userdto=user_dto)
                
                login_user(user=user)
                
                flash ('Bienvenido', 'info')
                
                redirect(url_for('hello'))
            else:
                flash('la chingaste en el usuario o en el pass?', 'danger')
        
        else:
            flash('la chingaste en el usuario o en el pass?', 'danger')

        return redirect(url_for('index', _external=True))

    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    
    flash('Hasta la vista gonorrea', "danger")
    
    return redirect(url_for('auth.login'))


@auth.route('signup', methods= ['GET', 'POST'])
def signup():
    signup_form = LoginForm()

    context = {
        'signup_form': signup_form
    }
    
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        
        user_doc = get_user(username)
        
        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password=password)
            user_dto = UserDTO(username, password_hash)
            
            put_user(user_dto=user_dto)
            
            user = UserModel(userdto=user_dto)
            
            login_user(user)
            
            flash('Buena, welcome mi amistad', 'info')
            
            return redirect(url_for('index'))

        else:
            flash('No me jodas, ya estas registrado', 'danger')      

    return render_template('signup.html', **context)
