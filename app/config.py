from flask import Flask
from app.routes import blueprint
from .celery_config import init_celery
import os

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

def create_app(app_name=PKG_NAME, **kwargs):
  app = Flask(app_name)
  
  if kwargs.get("celery"):
    init_celery(kwargs.get("celery"), app)  
  
  app.register_blueprint(blueprint)
  return app