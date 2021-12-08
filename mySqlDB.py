from flask.json import tag
import psycopg2
import requests

occasion_to_filters = {
  'Birthday': ['Food', 'Shopping', 'Adventures', 'Travel', 'Arts and Craft'],
  'Date Night': ['Food', 'Theatres', 'Adventures', 'Travel'],
  'Brunch': ['Food', 'Theatres', 'Shopping'],
  'Graduation': ['Food', 'Shopping', 'Travel', 'Theatres'],
  'Traveling': ['Food', 'Shopping', 'Theatres',  'Tours', 'Sightseeing'],
  'Wedding': [ 'Arts and Craft','Food', 'Shopping'],
  'Holiday': ['Food', 'Shopping', 'Theatres', 'Adventures', 'Tours']
}


filters_to_tags = {
  'Food' : ['Mexican', 'Indian', 'Chinese', 'Vegan', 'Arabic', 'Minority-Owned','Pet-Friendly'],
  'Shopping' : ['Shoes', 'Clothes', 'Home Decor', 'Grocery', 'Electronics','Minority-Owned','Pet-Friendly'],
  'Adventures' : ['Theme Parks', 'Arcade', 'Gaming Stores', 'Go-Karts', 'Sport Stadiums','Pet-Friendly','Minority-Owned', 'Trampoline Park', 'Horseback Riding', 'Sports Bars'],
  'Travel' : ['Tourist Visa', 'Car Rental', 'Motel','Minority-Owned','Pet-Friendly'],
  'Arts and Craft' : ['Stationery', 'Pottery', 'Art Studio', 'Face Painting','Pet-Friendly','Minority-Owned'],
  'Theatres' : ['Movies', 'Musicals','Minority-Owned','Pet-Friendly'],
  'Tours' :  ['Guided', 'Minority-Owned'],
  'Sightseeing' : ['Minority-Owned', 'Local'],
  }


STRING_LENGTH = 100
PHONE_NUMBER_LENGTH = 15
ID_SIZE = 11
connection = None
cursor = None


def connect():
  global connection
  global cursor
  connection = psycopg2.connect('postgres://ocgorhxfhtqouz:0b5ab52acd79bde38474f47067a4b7b91c48e21298e5592ced499cd391f423d0@ec2-34-202-66-20.compute-1.amazonaws.com:5432/d381s47af7e19t'
  )
  cursor = connection.cursor()


def getOccasions():
  return list(occasion_to_filters.keys())

def getFilters(occasion):
  filters = {}
  for filter in occasion_to_filters[occasion]:
    filters[filter] = filters_to_tags.get(filter,[])
  return filters

def getBusiness(chosen_filter_map, user_lat, user_long):
  filtered_results = []
  cursor.execute(f"SELECT * from businesses")
  results=cursor.fetchall()
  for result in results:
    filter_tag_list = result[5]
    filter_dict= {}
    for filter_tag in filter_tag_list:
      filter,tag = filter_tag[0].lower(), filter_tag[1].lower()

      if filter in chosen_filter_map and tag in chosen_filter_map[filter]:
        for f_t in filter_tag_list:
          if f_t[0] in filter_dict:
            if f_t[1] not in filter_dict[f_t[0]]:
              filter_dict[f_t[0]].append(f_t[1])
          else:
            filter_dict[f_t[0]] = ([f_t[1]])
        bus_reformat = {}
        bus_reformat['name'] = result[0]
        bus_reformat['photo_ref'] = get_image(result[1])
        bus_reformat['distance'] = get_distance(user_lat,user_long,result[2],result[3])
        bus_reformat['address'] = result[4]
        bus_reformat['tags'] = filter_dict
        filtered_results.append(bus_reformat)
        break

  return sorted(filtered_results,key=lambda x: x['distance'])

def get_business_info(name):
  bus = {}
  cursor.execute(f"SELECT * from businesses where businesses.name='{name}'")
  result=cursor.fetchone()
  tags = {}
  filter_tag_list = result[5]
  for filter_tag in filter_tag_list:
    if filter_tag[0] in tags and filter_tag[1] not in tags[filter_tag[0]]:
      tags[filter_tag[0]].append(filter_tag[1])
    else:
      tags[filter_tag[0]] = [filter_tag[1]]
  bus['name'] = result[0]
  bus['photo_ref'] = get_image(result[1])
  bus['distance'] = get_distance()
  bus['address'] = result[4]
  bus['tags'] = tags

  return bus

  

def get_distance(user_lat,user_long,bus_lat,bus_long):
  try:
    uri = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={bus_lat}%2C{bus_long}&origins={user_lat}%2C{user_long}&units=imperial&key=AIzaSyC41yIx7G6iH5bPOHebUOf1t1D4fB8Iinc"
    response_json = requests.get(uri).json()
    return response_json['rows'][0]['elements'][0]['distance']['text']
  except:
    return "Error"

def get_image(ref):
  return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=700&photo_reference={ref}&key=AIzaSyC41yIx7G6iH5bPOHebUOf1t1D4fB8Iinc"

def closeConnection():
  connection.close()