from flask import Blueprint, render_template, flash, redirect, url_for
from sqlalchemy import func
from models import User
from app import db
from users.forms import RegisterForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    max_id = db.session.query(func.max(User.id)).scalar()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        new_user = User(id=max_id + 1, email=form.email.data, password=form.password.data, first_name=form.firstname.data,  role=user)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login')
def login():
    return render_template('login.html')