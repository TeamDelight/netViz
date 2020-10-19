"""************************************************************************************************
                                        Team Delight - NetViz
Author: Team Delight
Description: Module for app launch

Modification History:
Date        Changed by              Description
04-10-2020  Marish_Varadaraj        Created app configuration page.
************************************************************************************************"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from config.web_config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
bootstrap = Bootstrap(app)
login.login_view = 'login'

from app import routes, models