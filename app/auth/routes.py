# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from app.auth.forms import SignUpForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user
from app.extensions import db, bcrypt
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='../templates',
                    static_folder='../static')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('core_bp.dashboard'))
    
    from app import db, bcrypt  # Import here to avoid circular import
    
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You may now log in.', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template('signup.html', title='Sign Up', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core_bp.dashboard'))
    
    from app import db, bcrypt  # Import here to avoid circular import
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('core_bp.dashboard'))
        else:
            flash('Login failed. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))
