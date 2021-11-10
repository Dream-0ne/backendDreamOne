import psycopg2
# from .connector import connection # Pip install mysql connector.py
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
  connection = psycopg2.connect(
    'postgres://wyrrcvebqcqwgc:0dfe7409d50bb77c0fa6b482391b50a527c2f3a7d18ae052bae3624ebcd6dd74@ec2-54-224-142-15.compute-1.amazonaws.com:5432/d2jp9osap146v'
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
  cursor.execute(f"CREATE table if not exists occasions ( name text)")
  for i in range(5):
    sql = f"INSERT INTO occasions(name) VALUES ({occasions[i]});"
    cursor.execute(sql)
  connection.commit()

def createOccasionsFilters():
  #cursor.execute(f"CREATE table if not exists occasionsfilters ( occasionid integer, filter text)")
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
  cursor.execute("SELECT name FROM occasions")
  results= cursor.fetchall()
  return [result[0] for result in results]

def getFilters(occasion):
  output = {}
  query = f"SELECT f.id, f.filter from occasionsfilters f, occasions o where o.id=f.occasionid and o.name=\'{occasion}\'"
  cursor.execute(query)
  filters= cursor.fetchall()
  for filter in filters:
    id,name = filter
    output[name] = getTags(id)
  return output

def getTags(filter):
  cursor.execute(f"SELECT tag from filterTags where filterid='{filter}'")
  results=cursor.fetchall()
  return [result[0] for result in results]


def closeConnection():
  connection.close()