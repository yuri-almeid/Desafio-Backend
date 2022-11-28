import requests
from .location import Location
from datetime import datetime
from app import APP_ID

def createDatabase():  
  db = Location()
  collection = db.collectionLocations()
  
  print("> Aguarde o processo de criação e escrita no banco de dados")
  locationsName = requests.get("https://geoapi.pt/municipios?json=1").json()
  for location in locationsName:
    try:
      locationCoordinate = requests.get("http://api.openweathermap.org/geo/1.0/direct", 
                                        params={
                                          "q":location + ",PT", 
                                          "appid": APP_ID
                                        }).json()
      collection.insert_one({
        "name": locationCoordinate[0]['name'], 
        "lat": locationCoordinate[0]['lat'], 
        "lon":locationCoordinate[0]['lon'],
      })
    except Exception as error:
      print(f"Falha ao carregar dados de {location}", error)
      
  documents = collection.find({}, {'name': 1, 'lat': 1, 'lon': 1})
  locations = [{item: data[item] for item in data} for data in documents]
  
  for location in locations:
    locationWeather = requests.get("https://api.openweathermap.org/data/2.5/onecall", 
                                    params={
                                      "lat":location['lat'], 
                                      "lon":location['lon'],
                                      "exclude":'current,hourly,minutely,alerts',
                                      "units":'metric',
                                      "appid": APP_ID
                                    }).json()
    
    for day in locationWeather["daily"]:
      collection.update_one({"name": location["name"]},{"$push": {"weather": {
        "dt": day["dt"], 
        "dt_txt":datetime.fromtimestamp(day["dt"]).strftime('%d-%m-%Y'), 
        "sunrise": day["sunrise"], 
        "wind_speed": day["wind_speed"], 
        "temp_min": day["temp"]["min"], 
        "temp_max": day["temp"]["max"] 
      }}})

