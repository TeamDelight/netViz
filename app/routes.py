"""************************************************************************************************
                                        Team Delight - NetViz
Author: Team Delight
Description: Module for web pages

Modification History:
Date        Changed by              Description
04-10-2020  Marish_Varadaraj        Flask based UI, with initial pages.
                                    index; login; logout methods created.

************************************************************************************************"""

from flask import Flask, flash,render_template, redirect, url_for, request
from app import app
from app.main.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models.models import User
from werkzeug.urls import url_parse


"""Initial login page for the netviz application
Description: main page of netviz application

Returns:
    Index page for rendering in flask
"""
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")


"""Verifying if the user is authenticated.
Description: This function authenticates if the current user is authenticated.
for the complete session of execution.
Returns:
    pages that are rendered based on the activity
    """
@app.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=login_form)


"""
Logout the user from the application.
    Description: This function authenticates if the current user is authenticated.
    for the complete session of execution.
Returns:
    logout page for rendering in flask
    """
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))