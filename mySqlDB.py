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
  cursor.execute(f"CREATE table if not exists occasions ( name text)")
  for i in range(5):
    sql = f"INSERT INTO occasions(name) VALUES ({occasions[i]});"
    cursor.execute(sql)
  connection.commit()
def createOccasionsFilters():
  cursor.execute(f"CREATE table if not exists occasionsfilters ( occasionid integer, filter text)")
  filters = ["Food,Shopping","Events"]
  for i in range(5):
    sql = f"INSERT INTO occasions(occasionid,filter) VALUES ({0,occasions[i]});"
    cursor.execute(sql)
  connection.commit()
def createFiltersTags():
  cursor.execute(f"CREATE table if not exists filterTags (filterid integer, tag text)")
  connection.commit()
def createBuisness():
  cursor.execute(f"CREATE table if not exists buisness ( name text, phone text, address TEXT)")
  connection.commit()
def createBuisnessTags():
  cursor.execute(f"CREATE table if not exists buisness (buisnessid integer, filter text, tag text)")
  connection.commit()
def getOccasions():
  cursor.execute("SELECT name FROM occasions")
  results= cursor.fetchall()
  return [result[0] for result in results]
def closeConnection():
  connection.close()