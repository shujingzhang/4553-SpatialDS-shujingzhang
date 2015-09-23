import sys
sys.path.append('E:/pythonIDE/Lib/site-packages/')
import pyqtree
import csv
from math import *
import numpy as np
import time

def loadCities():
    citys = []
    with open('citylist.csv', 'r') as csvfile:  # need open csv in text mode (not binary!)
        citysCsv = csv.reader(csvfile, delimiter=',', quotechar='"')
        for city in citysCsv:
            #print(city)
            citys.append({"Name":city[0],"Country":city[1],"lat":city[2],"lon":city[3]})
    return citys


def displace(lat,lng,theta, distance,unit="miles"):
    """
    Displace a LatLng theta degrees clockwise and some feet in that direction.
    Notes:
        http://www.movable-type.co.uk/scripts/latlong.html
        0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
    Args:
        theta:    A number in degrees where:
                  0   = North
                  90  = East
                  180 = South
                  270 = West
        distance: A number in specified unit.
        unit:     enum("miles","kilometers")
    Returns:
        A new LatLng.
    """
    theta = np.float32(theta)
    radiusInMiles = 3959
    radiusInKilometers = 6371
    
    if unit == "miles":
        radius = radiusInMiles
    else:
        radius = radiusInKilometers

    delta = np.divide(np.float32(distance), np.float32(radius))

    theta = deg2rad(theta)
    lat1 = deg2rad(lat)
    lng1 = deg2rad(lng)

    lat2 = np.arcsin( np.sin(lat1) * np.cos(delta) +
                      np.cos(lat1) * np.sin(delta) * np.cos(theta) )

    lng2 = lng1 + np.arctan2( np.sin(theta) * np.sin(delta) * np.cos(lat1),
                              np.cos(delta) - np.sin(lat1) * np.sin(lat2))

    lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

    return [rad2deg(lat2), rad2deg(lng2)]

def deg2rad(theta):
        return np.divide(np.dot(theta, np.pi), np.float32(180.0))

def rad2deg(theta):
        return np.divide(np.dot(theta, np.float32(180.0)), np.pi)

def lat2canvas(lat):
    """
    Turn a latitude in the form [-90 , 90] to the form [0 , 180]
    """
    return float(lat) % 180

def lon2canvas(lon):
    """
    Turn a longitude in the form [-180 , 180] to the form [0 , 360]
    """
    return float(lon) % 360
    
def canvas2lat(lat): 
    """
    Turn a latitutude in the form [0 , 180] to the form [-90 , 90]
    """
    return ((float(lat)+90) % 180) - 90
    
def canvas2lon(lon):
    """
    Turn a longitude in the form [0 , 360] to the form [-180 , 180]
    """
    return ((float(lon)+180) % 360) - 180

def main():
    res = open('output.dat', 'w')
    res.write("Name: shujing zhang\n")
    res.write("Date: 9/21/2015\n")
    res.write("Program 1 - Intro to Quadtrees\n")
    res.write("============================================================================================\n")
     
    time1 = time.time()
    spindex = pyqtree.Index(bbox=[0,0,360,180])
    cities = loadCities()

    for c in cities:
        #{'lat': '-18.01274', 'Country': 'Zimbabwe', 'lon': '31.07555', 'Name': 'Chitungwiza'}
        item = c['Name']
        #bbox =[float(c['lat']),float(c['lon']),float(c['lat']),float(c['lon'])]
        #First! Need converse form of latitude and longitude from [-90, 90] and [-180, 180] to [0, 180] and [0, 360], respectively
        canvaslat, canvaslon= lat2canvas(float(c['lat'])), lon2canvas(c['lon'])
        bbox = [canvaslat, canvaslon, canvaslat, canvaslon]
        spindex.insert(item=item, bbox=bbox)   
    
    slat, slon, elat, elon = 45.011419, -111.071777 , 40.996484, -104.040527
    res.write("1. All cities within the bounding box: "+str([slat,slon, elat, elon])+"\n\n")
    rangebbox = (lat2canvas(slat), lon2canvas(slon), lat2canvas(elat), lon2canvas(elon))
    mat = spindex.intersect(rangebbox)
    for city in mat:
        res.write(city+"\n")
        
    #overlapbbox = (51,51,86,86)
    #matches = spindex.intersect(overlapbbox)
    #print(matches)
    res.write("============================================================================================\n")

    miles = 500
    lat, lon = 23.805450, -78.156738
    res.write("2. All cities within "+str(miles)+" miles of this point: "+str((lat, lon))+":\n\n")
    slat, dummy = displace(lat, lon, 180, 500) # start latitude
    elat, dummy = displace(lat, lon, 0, 500) # end latitude
    dummy, slon = displace(lat, lon, 270, 500) # start longitude
    dummy, elon = displace(lat, lon, 90, 500) # end longitude
    #print(slat, slon, elat, elon)
    mat = spindex.intersect((lat2canvas(slat), lon2canvas(slon), lat2canvas(elat), lon2canvas(elon)))
    for city in mat:
        res.write(city+"\n")
    #lat1 = 33.912523
    #lon1 = -98.497925
    #print(displace(lat1,lon1,270,300))
    res.write("============================================================================================\n")
    time2 = time.time()
    res.write("Program run in: %.2f seconds."%(time2-time1))
    res.close()

if __name__ == '__main__':
    main()
