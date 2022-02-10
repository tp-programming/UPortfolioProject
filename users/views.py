from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from sqlalchemy import func
from models import User
from app import db, index
from users.forms import RegisterForm, LoginForm
from flask_login import current_user, login_required

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        max_id = db.session.query(func.max(User.id)).scalar()
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        new_user = User(id=max_id + 1, email=form.email.data, password=form.password.data, first_name=form.firstname.data,  role=user)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not user.password == form.password.data:
            flash('Wrong details')
            return render_template('login.html', form=form)

        login_user(user)
        user.current_logged_in = datetime.now()
        user.last_logged_in = user.current_logged_in
        db.session.add(user)
        db.session.commit()

        return index()

    return render_template('login.html', form=form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))