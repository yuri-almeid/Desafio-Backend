from app import celery
import requests
from .location import Location
from datetime import datetime
from app import APP_ID  
from bson import ObjectId

@celery.task(name='update')
def updateWeather():
  db = Location()
  collection = db.collectionLocations()
  
  documents = collection.find({}, {'name': 1, 'lat': 1, 'lon': 1, "weather.dt":1})
  locations = [{item: data[item] for item in data} for data in documents]

  for location in locations:
    lastTimestamp = location["weather"][-1]["dt"]

    weather = requests.get("https://api.openweathermap.org/data/2.5/onecall", 
                                    params={
                                      "lat":location['lat'], 
                                      "lon":location['lon'],
                                      "exclude":'current,hourly,minutely,alerts',
                                      "units":'metric',
                                      "appid":APP_ID
                                    }).json()

    for day in weather['daily']:
      if day['dt'] > lastTimestamp:
        collection.update_one({"_id": location["_id"]},{"$push": {"weather": {
          "dt": day["dt"], 
          "dt_txt":datetime.fromtimestamp(day["dt"]).strftime('%d-%m-%Y'), 
          "sunrise": day["sunrise"], 
          "wind_speed": day["wind_speed"], 
          "temp_min": day["temp"]["min"], 
          "temp_max": day["temp"]["max"] 
        }}})


