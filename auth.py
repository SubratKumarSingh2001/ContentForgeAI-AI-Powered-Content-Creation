from flask import render_template, url_for, request, flash, redirect, session
from models import db, User 

def signIn() :
    if 'user_id' in session :
        return redirect(url_for('dashboard')) 
    
    if request.method == 'POST' :
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first() #find the first matching data based on email
        if user and user.check_password(password) :
            session['user_id'] = user.id
            session['name'] = user.username
            return redirect(url_for('dashboard'))
        
        flash("Username or Password Incorrect", "error")
        return redirect(url_for("signin"))

    return render_template('signIn.html')

def signUp() :
    if 'user_id' in session :
        return redirect(url_for('dashboard'))

    if request.method == 'POST' :
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password :
            flash("Password Doesn't Match")
            return redirect(url_for('signup'))
        
        user = User(username=username, email=email)
        user.set_password(password) #store the hashed password

        db.session.add(user)
        db.session.commit()

        flash("Signup Successfully", "success")
        return redirect(url_for("signin"))
            
    return render_template('signUp.html')