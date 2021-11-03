import psycopg2
# from .connector import connection # Pip install mysql connector.py
STRING_LENGTH = 100
PHONE_NUMBER_LENGTH = 15
ID_SIZE = 11
connection = None
cursor = None
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
  cursor.execute(f"CREATE table if not exists occasions (id integer, name text, PRIMARY KEY(id))")
  for i in range(5):
    sql = "INSERT INTO occasions (id, name) VALUES (%s, %s)"
    val = (i,str(occasions[i]))
    cursor.execute(sql,val)
  connection.commit()
def createOccasionsFilters():
  cursor.execute(f"CREATE table if not exists occasionsfilters (id integer, occasionid integer, filter text, PRIMARY KEY(id))")
  connection.commit()
def createFiltersTags():
  cursor.execute(f"CREATE table if not exists filterTags (filterid integer, tag text, PRIMARY KEY(filterid,tag))")
  connection.commit()
def createBuisness():
  cursor.execute(f"CREATE table if not exists buisness (id integer, name text, phone text, address TEXT, PRIMARY KEY(id))")
  connection.commit()
def createBuisnessTags():
  cursor.execute(f"CREATE table if not exists buisness (buisnessid integer, filter text, tag text, PRIMARY KEY(buisnessid,filter,tag))")
  connection.commit()
def getOccasions():
  cursor.execute("SELECT name FROM occasions")
  results= cursor.fetchall()
  return results
def closeConnection():
  connection.close()