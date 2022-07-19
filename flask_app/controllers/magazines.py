
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.magazine import Magazine



# All magazines
@app.route('/dashboard')
def success():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    user_data = User.get_user_by_id(data)
    all_magazines = Magazine.get_all_magazines()
    return render_template('dashboard.html', this_user = user_data, all_magazines = all_magazines)


# new magazine routes
@app.route('/magazine/new')
def magazine_new():
    if "user_id" not in session:
        return redirect('/')
    return render_template('add_one.html')

@app.route('/publish_new_magazine', methods=['POST'])
def publish_new_magazine():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        'title': request.form['title'],
        'description': request.form['description']
    }
    if not Magazine.new_magazine_validation(data):
        return redirect('/magazine/new')
    Magazine.save_magazine(data)
    return redirect('/dashboard')


# View Magazine
@app.route('/magazine/view/<int:id>')
def view_magazine(id):
    if "user_id" not in session:
        return redirect('/')

    magazine_data = {
        'id':id
    }

    user_data = {
        'id':session['user_id']
    }
    user = User.get_user_by_id(user_data)
    magazine = Magazine.get_magazine_by_id(magazine_data)
    return render_template('show_one.html', magazine=magazine, user=user)

@app.route('/magazine/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    Magazine.delete_magazine(data)
    return redirect('/dashboard')


@app.route('/user/account')
def account():
    if "user_id" not in session:
        return redirect('/')
    
    user_data = {
        "id":session['user_id']
    }
    magazine_data = {
        "user_id":user_data['id']
    }
    user = User.get_user_by_id(user_data)
    magazines = User.get_one_user_with_magazines(magazine_data)
    return render_template('update_user.html', user=user, magazines=magazines)

@app.route('/update_information', methods=['POST'])
def update_information():
    if "user_id" not in session:
        return redirect('/')
    updated_data = {
        "id":session['user_id'],
        'first_name': request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email']
    }
    if not User.update_user_validation(updated_data):
        return redirect('/user/account')
    User.update_user_info(updated_data)
    return redirect('/user/account')

