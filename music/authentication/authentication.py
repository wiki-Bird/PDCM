from flask import Blueprint, render_template, request, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import music.authentication.services as services

import music.adapters.repository as repo

""" This blueprint encapsulates interactions relating to user sessions and registration. """
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None

    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)

            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Your user name is already taken - please supply another'
    
    return render_template(
        'auth/credentials.html',
        title='Register',
        form=form,
        user_name_not_unique=user_name_not_unique,
        user_name_error_message=user_name_not_unique,
        password_error_message=None,
        handler_url=url_for('authentication_bp.register')
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None
    
    if form.validate_on_submit():
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))
        except services.UnknownUserException:
            user_name_not_recognised = 'Username not recognized - please supply another'
        except services.AuthenticationException:
            password_does_not_match_user_name = 'Password does not match supplied user name - please check and try again'

    return render_template(
        'auth/credentials.html',
        title='Login',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form,
    )

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Username required'),
        Length(min=3, message='Username too short (minimum 3 characters)')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        Length(min=8, message='Password too short (minimum 8 characters)')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [DataRequired(message='Username required')])
    password = PasswordField('Password', [DataRequired(message='Password required')])
    submit = SubmitField('Login')