from flask import Blueprint, Response, json
from .location import Location
from datetime import datetime

blueprint = Blueprint("routes", __name__)

db = Location()

@blueprint.route('/')
def index():
  return Response(response=json.dumps({"Status": "Ok"}),
                  status=200,
                  mimetype='application/json')
  
@blueprint.route('/locations', methods=["GET"])
def getLocations():
  locations = db.readLocations()
  
  response = []
  for location in locations:
    response.append(location['name'])
  
  return Response(response=json.dumps(response),
                  status=200,
                  mimetype='application/json')

@blueprint.route('/temperature/<location>', methods=["GET"])
def getTemperature(location):
  temperatures = db.readTemperatures(location)
  
  response = []
  for temperature in temperatures:
    response.append({
    "date": temperature["weather"]["dt_txt"],
    "temp_max": temperature["weather"]["temp_min"],
    "temp_min": temperature["weather"]["temp_max"]
  })
  
  return Response(response=json.dumps(response),
                  status=200,
                  mimetype='application/json')

@blueprint.route('/rank/sunrise/<date>', methods=["GET"])
def getSunrise(date):
  
  try:
    isDateFormated = bool(datetime.strptime(date, "%d-%m-%Y"))
  except ValueError:
    isDateFormated = False
  
  if isDateFormated:
    sunriseRank = db.readSunrises(date)

    response = []
    for location in sunriseRank:
      response.append({
        "name": location['name'],
        "sunrise": location["weather"]["sunrise"],
        "sunrise_txt": datetime.fromtimestamp(location["weather"]["sunrise"]).strftime('%d-%m-%Y, %H:%M:%S')
      })

    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
  else:
    return Response(response=json.dumps({"error": "A data deve estar formatada em dd-mm-aaaa"}),
                    status=400,
                    mimetype='application/json')

@blueprint.route('/rank/wind', methods=["GET"])
def getWind():
  windSpeedRank = db.readWindSpeed()
  
  response = []
  for location in windSpeedRank:
    response.append({
    'name': location['_id'],
    'wind_speed_avg': location['wind_speed_avg']
    })
    
  return Response(response=json.dumps(response),
                  status=200,
                  mimetype='application/json')