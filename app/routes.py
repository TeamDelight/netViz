"""************************************************************************************************
                                        Team Delight - NetViz
Author: Team Delight
Description: Module for web pages

Modification History:
Date        Changed by              Description
04-10-2020  Marish_Varadaraj        Flask based UI, with initial pages.
                                    index; login; logout methods created.

************************************************************************************************"""

import os
from flask import Flask, flash, render_template, redirect, url_for, request, Response, jsonify
from app import app
from app.main.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models.models import User
from werkzeug.urls import url_parse
import json


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


@app.route('/login', methods=["GET", "POST"])
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

names_list = []
data_dict =[]
customer_search = ''

@app.route('/searchlist', methods=['GET', 'POST'])
def searchlist():
    search_value = request.form.getlist('autocomplete')[0]
    search_list = get_search_list(search_value)
    return Response(json.dumps(search_list), mimetype='application/json')

@app.route('/getsearchresult/<param>',methods=['GET'])
def get_search_list(param):
    global names_list
    names_list.clear
    #Query to fill the search result to be updated by Shyamala and Koushik.
    #list of strings values of param
    #db(param) return top 10 results. Karthik

    #conn.execute("select * from table where param top 10")
    names_list = ["Sam", "Smile", "Kumar", "Kartik", "Happy",
              "Joy", "123 address", "15 dovetail", "angel"]
    return names_list

@app.route("/search", methods=['POST'])
def search():
    global data_dict, customer_search
    data_dict.clear()
    customer_search = request.form['autocomplete']
    if customer_search in names_list:
        data_dict = get_search_result()
        return render_template("index.html", resulted_dict=data_dict)
    else:
        return render_template("index.html", customer_search=customer_search)

def get_search_result():
    #Query to fill the search result to be updated by Shyamala and Koushik.
    #list of dictionary taking in values of customer search
    data_dict = [{"id": 1, "name": "Kartik", "phone": "123|321", "Address": "Victoria"},
                {"id": 2, "name": "Kartik", "phone": "5768797|855", "Address": "Melbourne|Sydney|Brisbane"},
                {"id": 1, "name": "Kartik", "phone": "123", "Address": "Victoria"},
                {"id": 2, "name": "Kartik", "phone": "5768797", "Address": "Melbourne"},
                {"id": 1, "name": "Kartik", "phone": "123", "Address": "Victoria"},
                {"id": 2, "name": "Kartik", "phone": "5768797", "Address": "Melbourne"},
                {"id": 1, "name": "Kartik", "phone": "123", "Address": "Victoria"},
                {"id": 2, "name": "Kartik", "phone": "5768797", "Address": "Melbourne"},
                {"id": 3, "name": "Kumar", "phone": "5768797", "Address": "Melbourne"}]
    result_dict = []
    for data in data_dict:
        if data['name'] == customer_search:
            result_dict.append(data)
    return result_dict

@app.route("/graph_generation/<customer_id>")
def graph_generation(customer_id):
    #Query to get the json for network generation to be provided by Shyamala and Koushik.
    #json values for the given customer id
    file_location = os.getcwd().replace("\\", "/") + "/graph_gen_sample.json"
    return render_template("net_graph.html", data=jsonData(file_location),customer_search = customer_search)

added multiline incase if data exists, @Koushik N this to be separated by | (pipe symbol)
def jsonData(filePath):
    with open(filePath) as graph_data:
        data = json.load(graph_data)
        return str(data)
