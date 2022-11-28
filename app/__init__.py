from celery import Celery
from celery.schedules import crontab
import os

APP_ID = os.getenv("APP_ID")

def make_celery(app_name=__name__):
  backend = "redis://celery-broker:6379/0"
  broker = backend.replace("0", "1")
  
  celery = Celery(app_name, 
                  backend=backend, 
                  broker=broker, 
                  include=['app.tasks']
                  )
  
  celery.conf.beat_schedule = {
    "run-everyday-at-3am": {
      "task": "update",
      "schedule": crontab(hour=3, minute=0)
      }
    }
  
  return celery

celery = make_celery()