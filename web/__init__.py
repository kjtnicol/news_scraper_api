import logging
from flask import Flask
from flask_appbuilder import AppBuilder
from flask_appbuilder.security.mongoengine.manager import SecurityManager
from flask_mongoengine import MongoEngine

logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
dbmongo = MongoEngine(app)
# The Flask-AppBuilder init
appbuilder = AppBuilder(app, security_manager_class=SecurityManager)

from web import models, views