import requests
import json

from requests.api import request
count =0
def jprint(obj):
    text = json.loads(obj)
    return text
data = []
businessData = []
print("new run")
mainDict = [{"Fitler" : "Food" , "Tags": ["Mexican","Indian","Chinese","Vegan","Arabic"], "Query": ["Mexican Food", "Indian Food", "Chinese Food", "Vegan Food",'Arabic Food']}, 
{"Fitler" : "Shopping" , "Tags": ["Shoes","Clothes","Home Decor","Grocery","Electronics","Woodwork"], "Query": ["Shoes Store", "Clothes Store", "Home Decor Store" , "Grocery Store","Electronics Store", "Woodwork store"]}]
print(mainDict)

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
print(businessData[0]['bus'][0])
 
       

# for key in mainDict:
#     entry = {}
#     for val in mainDict[key]:
#         print(val)
#         entry["tag"] = val
#         entry["business"] = []        
#         print(val + "+"+key)
#         searchString = val + "+" + key
#         response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+searchString+"&location=43.070134,-89.390165&key=AIzaSyB2DhfwGMnFlb3US679PZirAsZyQeLoUiU&")
        
#         print(searchString)
#         print("--------------------------------------")

#         for value in response.json()["results"]:
#             try:
#                 curr = {}
#                 curr["name"] = value["name"]
#                 curr["address"] = value["formatted_address"]
#                 entry["business"].append(curr)
#             except:
#                 continue
#         data.append(entry)       

        

# for c in data:
#     print (c["tag"])
