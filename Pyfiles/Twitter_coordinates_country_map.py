import json
import urllib2
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import shapely.geometry as sgeom
import numpy as np
import os
import csv
import cartopy.feature as cfeature
from mpl_toolkits.basemap import Basemap
from collections import Counter


import os
os.chdir('<set your working directory>')

#thanks to http://blog.jverkamp.com/2012/10/25/determining-country-by-latitudelongitude/
def lookup(lat, lon):
    data = json.load(urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false' % (lat, lon)))
    for result in data['results']:
        for component in result['address_components']:
            if 'country' in component['types']:
                return component['long_name']
    return None


def open_file(filename):
	coordinates = []
	f = open(filename, 'rU')
	coordinates = json.load(f)
	f.close()
	return coordinates
	

def find_country(coordinates):
    output = []
    for row in coordinates:
        output.append(lookup(row[0], row[1]))
    return output


def create_merge(countries, coordinates):
    lat = []
    lon = []
    my_list = []
    for row in coordinates:
        lat.append(row[0])
        lon.append(row[1])
    for entry in countries:
        my_list.append(str(entry))
    return zip(my_list, lat, lon) 


""" count your countries """
def count_country(merged):
	count = [[x,merged[0].count(x)] for x in set(my_list[0])]
	sort = sorted(count)
	sn_count = sort[1:0]
	return sn_count


""" optional: replace The Netherlands with Netherlands and sort while associated with count!!!"""
def create_unique(count):
	country = []
	unique_count = []
	for row in count:
    	country.append(str(row[0]))
    	unique_count.append(float(row[1]))
    for n,i in enumerate(country):
    if i=='The Netherlands':
        country[n]=str('Netherlands')
	return sorted(zip(country, unique_count))


def create_unique(temp_list):
	unique_country = []
	unique_count = []
	for row in merge:
    	unique_country.append(str(row[0]))
    	unique_count.append(float(row[1]))
	unique_country = sorted(set(unique_country))
	unique_country = list(unique_country)
	return unique_count, unique_country


""" create world map """
def mapping(outfile):
    cmap = mpl.cm.Blues
    countries_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename)
    ax = plt.axes(projection=ccrs.Robinson())
    for item in geo_country_shp:
        name = item[0]
        if name in unique_country:
            i = unique_country.index(name)
            number = unique_count[i]
            ax.add_geometries(item[1], ccrs.PlateCarree(),
                              facecolor=cmap(number/float(maxi), 1),
                              label=name)
        else: 
            ax.add_geometries(item[1], ccrs.PlateCarree(),
                            facecolor='#FAFAFA',
                            label=name)
    plt.show()
    #if you want to save the picture add:
    plt.draw()
    plt.savefig(outfile)


""" calls all your functions and generates a world heat map """
def call_functions(filename, outfile):
	coordinates = open_file(filename)
	countries = find_country(coordinates)
	merged = create_merge(countries, coordinates)
	count = count_country(merged)
	temp_list = create_unique(count)
	unique_count, unqiue_country = create_unique(temp_list)
	mappnig(outfile)
	
	