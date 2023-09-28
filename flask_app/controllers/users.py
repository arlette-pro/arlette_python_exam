from flask_app import app
from flask_bcrypt import Bcrypt  
from flask import render_template, redirect,request,session,flash
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route('/')
def auth():
    return render_template('login_regis.html')


@app.route('/login')
def login():
    return render_template('login_regis.html')

@app.route('/process', methods=["POST"])
def process():
   
    if not User.validate_user(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
        
    }
    id = User.save(data)
    print(id)
    session['user_id'] = id
    return redirect('/appointments')


@app.route('/process-login', methods =['POST'])
def login_user():
    data = {
        'email':request.form['email']
    }
    
    user = User.get_user_by_email(data)
    if not user:
        flash("Invalid credentials", 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid credentials", 'login')
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/appointments')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')