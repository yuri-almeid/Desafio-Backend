from pymongo import MongoClient
from datetime import datetime

class Location:
  def __init__(self):
    self.client = MongoClient('mongodb://application-database:27017')
    cursor = self.client['DB']
    self.collection = cursor['locations']
    
  def collectionLocations(self):
    return self.collection
  
  def isDatabase(self):
    databases = self.client.list_database_names()
    if 'DB' in databases:
      return True
    else:
      return False
  
  def readLocations(self):
    documents = self.collection.find({}, {'name': 1})
    data = [{item: data[item] for item in data if item != '_id'} for data in documents]
    return data
  
  def readLocationsDetail(self):
    documents = self.collection.find({}, {'name': 1, 'lat': 1, 'lon': 1})
    data = [{item: data[item] for item in data} for data in documents]
    return data
  
  def readTemperatures(self, name):
    currentTimestamp = datetime.now().timestamp()
    documents = self.collection.aggregate([
            { '$match': { 'name': name } },
            { '$unwind': '$weather' },
            { '$match': { 'weather.dt': { "$gte": currentTimestamp - 86400} }},
            { '$limit': 5 }
        ])
    data = [{item: data[item] for item in data if item != "_id"} for data in documents]
    return data
  
  def readSunrises(self, date):
    documents = self.collection.aggregate([
        { '$unwind': '$weather' },
        { '$match': { 'weather.dt_txt': date }},
        { '$project': {'name':1, 'weather.sunrise':1}},
        { '$sort': {'weather.sunrise': 1}},
        { '$limit': 10 }
    ])
    data = [{item: data[item] for item in data if item != "_id"} for data in documents]
    return data
  
  def readWindSpeed(self):
    currentTimestamp = datetime.now().timestamp()
    documents = self.collection.aggregate([
        { '$unwind': '$weather' },
        { '$match': { 'weather.dt': { 
          '$gte': currentTimestamp - 86400, 
          '$lte': currentTimestamp + 345600} 
        }},
        { '$group': {
          '_id':  '$name',
          'wind_speed_avg' : {'$avg' : "$weather.wind_speed"}
        }},
        { '$sort': {'wind_speed_avg': 1}},
        { '$limit': 10}
    ])
    data = [{item: data[item] for item in data} for data in documents]
    return data