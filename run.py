from app import config
import app
from app.functions import createDatabase
from app.location import Location

if __name__ == "__main__":
  
  db = Location()
  
  if db.isDatabase():
    print("> Database already set")
  else:
    createDatabase()
  
  app = config.create_app(celery=app.celery)
  app.run( host='0.0.0.0', port=5000 )