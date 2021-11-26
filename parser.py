import requests
import json
from requests.api import request


def scraper():
    data = []
    businessData = []
    mainDict = [{"Fitler" : "Food" , "Tags": ["Mexican","Indian","Chinese","Vegan","Arabic"], "Query": ["Mexican Food", "Indian Food", "Chinese Food", "Vegan Food",'Arabic Food']}, 
    {"Fitler" : "Shopping" , "Tags": ["Shoes","Clothes","Home Decor","Grocery","Electronics","Woodwork"], "Query": ["Shoes Store", "Clothes Store", "Home Decor Store" , "Grocery Store","Electronics Store", "Woodwork store"]},
    {"Fitler" : "Gaming" , "Tags": ["Theme Park","Arcade","Gaming Stores","Go karts","Trampoline Park","Horseback Riding", "Gaming Bars"], "Query": ["Theme Park","Arcade","Gaming Stores","Go karts","Trampoline Park","Horseback Riding", "Gaming Bars"]},
    {"Fitler" : "Travel" , "Tags": ["Tourist Visa", "Car rental", "Motel"], "Query": ["Tourist Visa", "Car rental", "Motel"]},
    {"Fitler" : "Arts and Craft" , "Tags": ["Pottery", "Stationary", "Art Studio", "Face Painting"], "Query": ["Pottery Store", "Stationary Store", "Art Studio", "Face Painting"]},
    {"Filter": "Theatres", "Tags": ["Musical", "Movies"], "Query":["Musical", "Movies"]},
    {"Fitler": "Tours", "Tags": ["Tours"], "Query":["Local Guided Tours"]},
    {"Fitler": "Sightseeing", "Tags": ["Local"], "Query":["Local Attractions"]}]
    for category in mainDict:
        for i in range(len(category["Tags"])):
            tagList = []
            response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+category["Query"][i]+"&location=43.070134,-89.390165&key=AIzaSyB2DhfwGMnFlb3US679PZirAsZyQeLoUiU&")
            data = response.json()['results']
            currList = []
            tag_entry = {}
            tag_entry["tag"] = category["Tags"][i]
            for val in data:
                try:
                    entry = {}
                    entry["name"] = val["name"]
                    entry["photo"] = val["photos"][0]["photo_reference"]
                    entry["latitude"] = val["geometry"]["location"]["lat"]
                    entry["longtitude"] = val["geometry"]["location"]["lng"]
                    entry["address"] = val["formatted_address"]
                    currList.append(entry)
                except:
                    continue
            tag_entry["bus"] = currList
            businessData.append(tag_entry)
    return businessData
if __name__ == "main":
    scraper()