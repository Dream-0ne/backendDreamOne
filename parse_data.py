def combine(data):#{tag: {name: "", tag="", address='',long=0.0,lat=0.0,photo_ref=""}}
    businesses = {} # {'name':{address="",tags=[], long = 0.0, lat = 0.0}}
    for tag in data:
        for business in data[tag]:
            if business['name'] in businesses:
                businesses[business['name']]['tags'].append(tag)
            else:
                business['tags'] = [business['tag']]
                del business['tag']
                businesses[business['name']] = business
    return business
