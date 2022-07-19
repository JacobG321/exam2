from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.magazine import Magazine

#login registration page
@app.route('/')
def index():
    return render_template('index.html')


# For new users
@app.route('/new_account', methods=['POST'])
def process():
    data = {
        'first_name': request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password']
    }
    if request.form['confirm_password'] != request.form['password']:
        flash('Password does not match')
        return redirect('/')
    if User.check_if_email_in_system(data) == True:
        flash('Email already taken!')
        return redirect('/')
    if not User.new_user_validation(data):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data['password'] = pw_hash
    session['user_id'] = User.save_user(data)
    return redirect('/dashboard')


# For existing users
@app.route('/signing_in', methods=['POST'])
def signing_in():
    data = {
        'email':request.form['email'],
    }
    user_in_db = User.get_user_by_email(data)
    
    if not user_in_db:
        flash('Invalid Email/Password', 'sign_in')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'sign_in')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')