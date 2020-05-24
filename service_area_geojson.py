# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:51:44 2020

@author: anees
"""

import pandas as pd
import numpy as np
import requests
import json
import topojson
import time

data = pd.read_csv("clinic_areas_1.csv")
data = data.drop(columns = ['index', 'hour_simplified'])

identifier = []
service_area_geometries = []

API_Key = "5b3ce3597851110001cf6248255645d2de73474fb133bc9084349782"
for index, row in data.iterrows():
    identifier.append('clinic_' + str(index))
    
    body = {"locations":[[row['Longitude'], row['Latitude']]],
                "range":[3600],
                "range_type":"time",
                "smoothing":50}
    
    headers = {'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
                'Authorization': API_Key}
    
    call = requests.post('https://api.openrouteservice.org/v2/isochrones/driving-car', json=body, headers=headers)
    service_area = json.loads(call.text)["features"][0]
    
    service_area_geometries.append(json.dumps(service_area))
    
    if ((index%4) == 0):
        print(str(index / 4) + "% complete" )
    time.sleep(3)
    
data['hour_simplified'] = service_area_geometries
data['index'] = identifier
columns = ['index', 'Name', 'Longitude', 'Latitude', 'hour_simplified', 'population']

data = data[columns]

data.to_csv('clinic_service_areas_geojson.csv', index=False)
