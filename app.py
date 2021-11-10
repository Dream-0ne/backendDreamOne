from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request, jsonify, make_response,after_this_request
import mySqlDB
import json
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
change = False

mySqlDB.connect()
mySqlDB.drop_create()
    

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

if __name__ == "__main__":
    app.run(host="localhost",port=5000)
