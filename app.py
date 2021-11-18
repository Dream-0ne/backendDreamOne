from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request, jsonify, make_response,after_this_request
import mySqlDB
import json
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
change = False

mySqlDB.connect()
#mySqlDB.createTables()
    

@app.route('/occasions', methods=['GET'])
def occasionList():
    occasionlist = mySqlDB.getOccasions()
    # Cross origin issues work around for front-end fetch API calls
    @after_this_request 
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return jsonify(occasionlist)

@app.route('/filters/<occasion>', methods=['GET'])
def filtersList(occasion):
    print(occasion)
    occasionlist = mySqlDB.getFilters(occasion)
    # Cross origin issues work around for front-end fetch API calls
    @after_this_request 
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return jsonify(occasionlist)
'''
This method takes in a filterlist parameter which consist of filter and chosen requirments
Based on the passed in parameters it will pass in businesses that fit that criteria

Filterlist parameter format -  Filter1:requirement1,filter2,requirement2
For example: if the users chooses food and shopping and adds requirements it becomes Food:Mexican,Shopping:thriftstore for filterlist
'''
@app.route('/business/<filterlist>', methods=['GET'])
def businessList(filterlist):
    print(filterlist)
    filterMap = {}
    chosenFilters = filterlist.split(",")
    for i in range (len(chosenFilters)):
        val = chosenFilters[i].split(":")
        filterMap[val[0]] = val[1:]
    # Cross origin issues work around for front-end fetch API calls
    @after_this_request 
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return jsonify(mySqlDB.getBusiness(filterMap))

if __name__ == "__main__":
    app.run(host="localhost",port=5000)
