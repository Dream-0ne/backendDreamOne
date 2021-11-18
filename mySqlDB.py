import psycopg2
# from .connector import connection # Pip install mysql connector.py

occasion_to_filters = {
  'Birthday': ['Food', 'Shopping', 'Adventures', 'Travel', 'Volunteering', 'Art and Craft'],
  'Date Night': ['Food', 'Movies', 'Adventures', 'Travel'],
  'Brunch': ['Food' 'Theatres', 'Pet-Friendly', 'Party'],
  'Graduation': ['Food', 'Shopping', 'Travel', 'Theatres', 'Volunteering'],
  'Traveling': ['Food', 'Shopping', 'Theatres',  'Tours', 'Sightseeing'],
  'Wedding': [ 'Art and Craft', 'Bakery', 'Food', 'Shopping'],
  'Anniversary': ['Party Halls', 'Party Planners', 'Food', 'Bakery', 'Art and Craft'],
  'Moving': ['Movers', 'Car Rental', 'Art and Craft', 'Interior Decorator'],
  'Holiday': ['Food', 'Shopping', 'Theatres', 'Adventures', 'Tours']
}

filters_to_tags = {
  'Food' : ['Mexican', 'Indian', 'Chinese', 'Vegan', 'Arab', 'Minority-Owned','Pet-Friendly', 'No Preference'],
  'Shopping' : ['Shoes', 'Clothes', 'Home Decor', 'Grocery', 'Electronics','Minority-Owned','Pet-Friendly', 'No Preference'],
  'Gaming' : ['Theme Parks', 'Arcade', 'Gaming Stores', 'Go-Karts', 'Sport Stadiums','Pet-Friendly','Minority-Owned', 'Trampoline Park', 'Horseback Riding', 'Sports Bars', 'No Preference'],
  'Travel' : ['Tourist Visa', 'Car Rental', 'Motel','Minority-Owned','Pet-Friendly', 'No Preference'],
  'Arts and Craft' : ['Stationery', 'Pottery', 'Art Studio', 'Face Painting','Pet-Friendly','Minority-Owned', 'No Preference'],
  'Theatres' : ['Movies', 'Musicals','Minority-Owned','Pet-Friendly', 'No Preference'],
  'Tours' :  ['Guided', 'Minority-Owned', 'No Preference'],
  'Sightseeing' : ['Minority-Owned', 'Local', 'No Preference'],
  }


STRING_LENGTH = 100
PHONE_NUMBER_LENGTH = 15
ID_SIZE = 11
connection = None
cursor = None

def drop_create():
  global cursor
  tables = ['occasions','occasionfilters','filtertags','buisness','buisnesstags']
  for table in tables:
    cursor.execute(f"Drop table if exists {table}")
  createTables()

def connect():
  global connection
  global cursor
  connection = psycopg2.connect('postgres://ocgorhxfhtqouz:0b5ab52acd79bde38474f47067a4b7b91c48e21298e5592ced499cd391f423d0@ec2-34-202-66-20.compute-1.amazonaws.com:5432/d381s47af7e19t'
  )
  cursor = connection.cursor()

def createTables():
  createOccasions()
  createOccasionsFilters()
  createFiltersTags()
  createBuisness()
  createBuisnessTags()

def createOccasions():
  occasions = ["Birthday","Nightout","Party","Date","Exploring"]
  cursor.execute(f"CREATE table if not exists occasions (id int, name text)")
  for i in range(5):
    sql = f"INSERT INTO occasions(id,name) VALUES ({i},'{occasions[i]}');"
    cursor.execute(sql)
  connection.commit()

def createOccasionsFilters():
  filters = ['Shopping','Events']
  idCount = 3
  for i in range(len(filters)):
    postgres_insert_query = """ INSERT INTO occasionsfilters (filter, id, occasionid) VALUES (%s,%s,%s)"""
    record_to_insert = (filters[i], idCount, 1)
    cursor.execute(postgres_insert_query, record_to_insert)
    idCount+=1
  connection.commit()

def createFiltersTags():
  cursor.execute(f"CREATE table if not exists filterTags (filterid integer, tag text)")
  connection.commit()

def createBuisness():
  cursor.execute(f"CREATE table if not exists buisness ( name text, phone text, address TEXT)")
  connection.commit()

def createBuisnessTags():
  cursor.execute(f"CREATE table if not exists buisnesstags (buisnessid integer, filter text, tag text)")
  connection.commit()

def getOccasions():
  return list(occasion_to_filters.keys())

def getFilters(occasion):
  filters = {}
  for filter in occasion_to_filters[occasion]:
    filters[filter] = filters_to_tags.get(filter,[])
  return filters

# def getTags(filter):
#   cursor.execute(f"SELECT tag from filterTags where filterid='{filter}'")
#   results=cursor.fetchall()
#   return [result[0] for result in results]


def closeConnection():
  connection.close()