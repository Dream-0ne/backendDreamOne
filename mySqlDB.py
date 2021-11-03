import mysql.connector
from mysql.connector import connection # Pip install mysql connector.py

STRING_LENGTH = 100
PHONE_NUMBER_LENGTH = 15
ID_SIZE = 11
connection = None
cursor = None

def connect():
  global connection
  global cursor
  connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Meerxn3342!",
  )
  cursor = connection.cursor()


def createTables():
  cursor.execute("CREATE DATABASE if not exists DreamOneDB ")
  cursor.execute("USE DreamOneDB")
  createOccasions()
  createOccasionsFilters()
  createFiltersTags()
  createBuisness()
  createBuisnessTags()

def createOccasions():
  occasions = ["Birthday","Nightout","Party","Date","Exploring"]
  cursor.execute(f"CREATE table if not exists occasions (id int({ID_SIZE}), name varchar({STRING_LENGTH}), PRIMARY KEY(id))")
  for i in range(5):
    sql = "REPLACE INTO occasions (id, name) VALUES (%s, %s)"
    val = (i,str(occasions[i]))
    cursor.execute(sql,val)
  connection.commit()

def createOccasionsFilters():
  cursor.execute(f"CREATE table if not exists occasionsfilters (id int({ID_SIZE}), occasionid int({ID_SIZE}), filter varchar({STRING_LENGTH}), PRIMARY KEY(id))")
  connection.commit()

def createFiltersTags():
  cursor.execute(f"CREATE table if not exists filterTags (filterid int({ID_SIZE}), tag varchar({STRING_LENGTH}), PRIMARY KEY(filterid,tag))")
  connection.commit()

def createBuisness():
  cursor.execute(f"CREATE table if not exists buisness (id int({ID_SIZE}), name varchar({STRING_LENGTH}), phone varchar({PHONE_NUMBER_LENGTH}), address TEXT, PRIMARY KEY(id))")
  connection.commit()

def createBuisnessTags():
  cursor.execute(f"CREATE table if not exists buisness (buisnessid int({ID_SIZE}), filter varchar({STRING_LENGTH}), tag varchar({STRING_LENGTH}), PRIMARY KEY(buisnessid,filter,tag))")
  connection.commit()

def getOccasions():
  cursor.execute("SELECT name FROM occasions")
  results= cursor.fetchall()
  return results

def closeConnection():
  connection.close()
