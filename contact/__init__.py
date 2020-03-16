from flask import Flask
from contact.config import *


def create_app(config):
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(__name__)
    application.config.from_object(config)
    config.init_app(application)
    return application


def register(application):
    from contact import views
    return application


app = create_app(config)
app = register(app)
