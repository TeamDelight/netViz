"""************************************************************************************************
                                        Team Delight - NetViz
Author: Team Delight
Description: Module for web pages

Modification History:
Date        Changed by              Description
04-10-2020  Marish_Varadaraj        Flask based UI, with initial pages.
                                    index; login; logout methods created.

29-10-2020  Koushik Chakraborty     Completed integration with all backend functions
************************************************************************************************"""

import os
from flask import Flask, flash, render_template, redirect, url_for, make_response, request, Response, jsonify
from app import app
from app.main.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models.models import User
from werkzeug.urls import url_parse
import json
from app.db_integration.search_result_set import search_suggestion, search_result_data_fetch3
from app.db_integration.network_generation import write_file_path
import re



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
data_dict = []
customer_search = ''


@app.route('/searchlist', methods=['GET', 'POST'])
def searchlist():
    """
    search_value = request.form.getlist('autocomplete')[0]
    search_list_response = get_search_list(search_value).json[0]
    search_list = search_list_response.split(":")[1]
    search_list = re.sub("[\[\]']", "", search_list)
    search_list = search_list.split(",")
    return Response(json.dumps(search_list), mimetype='application/json')
    """
    
    search_value = request.form['autocomplete']
    search_list = get_search_list(search_value)
            
    return Response(json.dumps(search_list), mimetype='application/json')
    
    
@app.route('/getsearchresult/<param>',methods=['GET'])
def get_search_list(param):
    names_list = []
    names_list.clear   
    names_list = search_suggestion(param)
    
    """return make_response(jsonify("names_list:" + str(names_list), 200))"""
    return names_list


@app.route("/search", methods=['GET', 'POST'])
def search():
    print("search")   
    data_dict = [] 
    data_dict.clear()
    customer_search = request.form['autocomplete']
    data_dict = get_search_result(customer_search)
    """
    if customer_search in names_list:
        data_dict = get_search_result()
        return render_template("index.html", resulted_dict=data_dict)
    else:
        return render_template("index.html", customer_search=customer_search)
    """
    if data_dict != []:
        return render_template("index.html", resulted_dict=data_dict)
    else:
        return render_template("index.html", customer_search=customer_search)
   


@app.route('/getsearchresult/<param>',methods=['GET'])
def get_search_result(param):
    result_dict = search_result_data_fetch3(param)
    
    """
    result_dict = []
    for data in data_dict:
        if data['name'] == customer_search:
            result_dict.append(data)
    return result_dict
    """
    
    return result_dict


@app.route("/graph_generation/<customer_id>")
def graph_generation(customer_id):    
    write_file_path(customer_id)
    file_location = os.getcwd().replace("\\", "/") + "/graph_gen_sample.json"
    
    return render_template("net_graph.html", data=jsonData(file_location),customer_search = customer_search)


def jsonData(filePath):
    with open(filePath) as graph_data:
        data = json.load(graph_data)
        
        return str(data)
