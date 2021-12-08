from flask import Flask
from flask_cors import CORS
from flask import request, jsonify, make_response,after_this_request
import mySqlDB
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
change = False
my_cache = {}
mySqlDB.connect()
    

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
@app.route('/business/<lat>/<long>/<filterlist>', methods=['GET'])
def businessList(filterlist,lat,long):
    if filterlist+lat+long in my_cache:
        print("cached")
        exit(1)
        return my_cache[(filterlist,lat,long)]
    filterlist = filterlist.lower()
    filterMap = {}
    chosenFilters = filterlist.split(":")
    for i in range(len(chosenFilters)//2):
        if chosenFilters[i * 2] in filterMap:
            filterMap[chosenFilters[i*2]].append(chosenFilters[i*2 + 1])
        else:
            filterMap[chosenFilters[i*2]] = [chosenFilters[i*2 + 1]]
    # Cross origin issues work around for front-end fetch API calls
    @after_this_request 
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    result = jsonify(mySqlDB.getBusiness(filterMap,lat,long))
    print("keys:" + str(my_cache.keys()))
    print("value: " + filterlist+lat+long)

    my_cache[filterlist+lat+long] = result
    return result

@app.route('/businessinfo/<name>', methods=['GET'])
def businessinfo(name):
    return jsonify(mySqlDB.get_business_info(name))

if __name__ == "__main__":
    app.run(host="localhost",port=5000)
