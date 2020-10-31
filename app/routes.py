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
from app.db_integration.search_result_set import search_suggestion, search_result_data_fetch3, cus_name_fetch
from app.db_integration.network_generation import network_json_gen
import re
import ast

"""
Defining global variabels
"""
customer_search = ''


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



"""
Verifying if the user is authenticated.
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

"""
Search list
This method is used for getting the search suggestions for the user by fetching the values from database.
Returns:
    renders page for showing the suggestions.
"""
@app.route('/searchlist', methods=['GET', 'POST'])
def searchlist():
    global customer_search
    search_value = request.args.get('autocomplete')
    customer_search = search_value
    search_result = get_search_list(search_value)
    if search_result[0].status_code == 200:
        search_list_response = search_result[0].json
        search_list = search_list_response.split(":")[1]
        search_list = re.sub("[\[\]']", "", search_list)
        search_list = search_list.split(", ")
        return Response(json.dumps(search_list), mimetype='application/json')
    else:
        """
        error message or page to be diplayed here
        """
        pass

"""
API end point for search suggestions
This method loads the suggestions for API where first 15 records are found.

parameters:
values to be searched in the UI

Returns:
    returns json for data from the backend for search parameter passed.
"""
@app.route('/api/getsearchresult/<param>', methods=['GET'])
def get_search_list(param):
    names_list = []
    names_list = search_suggestion(param)
    if names_list:
        return make_response(jsonify("names_list:" + str(names_list))), 200
    else:
        return make_response(jsonify("error:No records found making the search")), 404



"""
Search list
This method is used for getting the table populated for the given search parameter.
Returns:
    renders page for showing the result table.
"""
@app.route("/search", methods=['GET', 'POST'])
def search():
    result_set = []
    result_set.clear()
    global customer_search
    customer_search = request.form['autocomplete']
    result_set = get_search_result(customer_search)

    if result_set[0].status_code == 200:
        result_set = result_set[0].json[10:]
        result_set = ast.literal_eval(result_set)
        if result_set != []:
            return render_template("index.html", resulted_dict=result_set, customer_search=customer_search)
        else:
            return render_template("index.html", customer_search=customer_search)
    else:
        """
        error message or page to be diplayed here
        """
        pass


"""
API end point for search suggestions
This method loads the suggestions for API where first 15 records are found.

parameters:
values to be searched in the UI

Returns:
    returns json for data from the backend for search parameter passed.
"""
@app.route('/api/getsearchresultset/<param>', methods=['GET'])
def get_search_result(param):
    result_set = search_result_data_fetch3(param)
    if result_set:
        result_set = json.dumps(result_set)
        return make_response(jsonify("dict_list:" + str(result_set))), 200
    else:
        return make_response(jsonify("error:No records found for given value")), 404


"""
Method to generate the network graph in UI
parameters:
Customer ID as parameter for generating the graph data

Returns:
    renders page for graph generations
"""
@app.route("/graph_generation/<customer_id>")
def graph_generation(customer_id):
    customer_search = cus_name_fetch(customer_id)
    json_data_net = str(network_json_gen(customer_id)).replace('"', "'")
    return render_template("net_graph.html", data=json_data_net, customer_search=customer_search)


"""
API end point for getting data of graph generations

parameters:
Customer ID as parameter for generating the graph data

Returns:
    returns the json data of graphs generation
"""
@app.route("/api/graph_generation/<customer_id>")
def get_graph_data(customer_id):
    json_data_net = str(network_json_gen(customer_id)).replace('"', "'")
    if json_data_net:
        return make_response(jsonify("graph_data:" + json_data_net)), 200
    else:
        return make_response(jsonify("error:No records found for given value")), 404
