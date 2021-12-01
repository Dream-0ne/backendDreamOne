import requests
import json
from requests.api import request
import psycopg2

def scraper():
    connection = psycopg2.connect('postgres://ocgorhxfhtqouz:0b5ab52acd79bde38474f47067a4b7b91c48e21298e5592ced499cd391f423d0@ec2-34-202-66-20.compute-1.amazonaws.com:5432/d381s47af7e19t')
    cursor = connection.cursor()
    data = []
    businessData = []
    mainDict = [{"Filter" : "Food" , "Tags": ["Mexican","Indian","Chinese","Vegan","Arabic"], "Query": ["Mexican Food", "Indian Food", "Chinese Food", "Vegan Food",'Arabic Food']}, 
    {"Filter" : "Shopping" , "Tags": ["Shoes","Clothes","Home Decor","Grocery","Electronics","Woodwork"], "Query": ["Shoes Store", "Clothes Store", "Home Decor Store" , "Grocery Store","Electronics Store", "Woodwork store"]},
    {"Filter" : "Gaming" , "Tags": ["Theme Park","Arcade","Gaming Stores","Go karts","Trampoline Park","Horseback Riding", "Gaming Bars"], "Query": ["Theme Park","Arcade","Gaming Stores","Go karts","Trampoline Park","Horseback Riding", "Gaming Bars"]},
    {"Filter" : "Travel" , "Tags": ["Tourist Visa", "Car rental", "Motel"], "Query": ["Tourist Visa", "Car rental", "Motel"]},
    {"Filter" : "Arts and Craft" , "Tags": ["Pottery", "Stationary", "Art Studio", "Face Painting"], "Query": ["Pottery Store", "Stationary Store", "Art Studio", "Face Painting"]},
    {"Filter": "Theatres", "Tags": ["Musical", "Movies"], "Query":["Musical", "Movies"]},
    {"Filter": "Tours", "Tags": ["Tours"], "Query":["Local Guided Tours"]},
    {"Filter": "Sightseeing", "Tags": ["Local"], "Query":["Local Attractions"]}]
    for category in mainDict:
        for i in range(len(category["Tags"])):
            tagList = []
            response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+category["Query"][i]+"&location=43.070134,-89.390165&key=AIzaSyB2DhfwGMnFlb3US679PZirAsZyQeLoUiU&")
            data = response.json()['results']
            currList = []
            tag_entry = {}
            tag_entry["filter_tag"] = [category['Filter'],category["Tags"][i]]
            for val in data:
                try:
                    entry = {}
                    entry["name"] = val["name"]
                    entry["photo"] = val["photos"][0]["photo_reference"]
                    entry["latitude"] = val["geometry"]["location"]["lat"]
                    entry["longtitude"] = val["geometry"]["location"]["lng"]
                    entry["address"] = val["formatted_address"]
                    currList.append(entry)
                    if entry['name'] == "QDOBA Mexican Eats":
                        print(entry)
                except:
                    continue
            tag_entry["bus"] = currList
            businessData.append(tag_entry)
    print(businessData)
    return businessData

    
def combine_data(data):
    combined = dict()
    for entry in data:
        filter_tag = entry['filter_tag']
        for bus in entry['bus']:
            if bus['name'] in combined:
                combined[bus['name']]['filter_tag'].append(filter_tag)
            else:
                combined[bus['name']] = bus
                combined[bus['name']]['filter_tag'] = [filter_tag]
    return combined

def push_to_db(data):
    connection = psycopg2.connect('postgres://ocgorhxfhtqouz:0b5ab52acd79bde38474f47067a4b7b91c48e21298e5592ced499cd391f423d0@ec2-34-202-66-20.compute-1.amazonaws.com:5432/d381s47af7e19t')
    cursor = connection.cursor()
    cursor.execute('Create table businesses (name text, photo_ref text, latitude text, longtitude text, address text, filter_tag text[][2])')
    connection.commit()
    for bus_name in data:
        bus = data[bus_name]
        postgres_insert_query = """ INSERT INTO businesses (name, photo_ref, latitude, longtitude, address, filter_tag) VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (bus['name'],bus['photo'], bus['latitude'], bus['longtitude'], bus['address'], bus['filter_tag'] )
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

if __name__ == "__main__":
    push_to_db((combine_data(scraper())))