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
import pandas as pd

# optional: set directory
os.chdir('<set your working directory>')

#import population data
def import_pops(infile, outfile): 
    with open(infile, mode='rU') as infile:
        reader = csv.reader(infile)
        with open(outfile, mode='w') as outfile:
            writer = csv.writer(outfile)
            mydict = {rows[0]:rows[1] for rows in reader}
    return mydict


def create_pop_list(my_dict):
    pop_list = []
    values = mydict.values()
    keys = mydict.keys()
    merged = sorted(zip(keys, values))
    for row in merged:
        pop_list.append(float(row[1]))
    return pop_list


#import data of interest (containing coordinates)
def open_file(filename):
	coordinates = []
	f = open(filename, 'rU')
	coordinates = json.load(f)
	f.close()
	return coordinates


#retrieve information for USA located coordinates
def FIPS_lookup(USA):
    data = []
    county = []
    state = []
    codes = []
    for row in USA:
        data.append(json.load(urllib2.urlopen('http://data.fcc.gov/api/block/find?format=json&latitude=%s&longitude=%s&showall=true' % (row[0], row[1]))))
    for row in data:
        county.append(row['County']['FIPS'])
        state.append(str(row['State']['name']))
        codes.append(str(row['State']['code']))
    return zip(codes, state, county)


#remove entries which are outside the US:
def remove_none(FIPS):
    USstate = []
    for entry in FIPS:
        if entry[0] != 'None':
            USstate.append(entry[1])
    return USstate


#remove territories 
def remove_US_territories(USstate):
    my_list = []
    for entry in USstate:
        if entry != 'Guam':
            if entry != 'Puerto Rico':
                if entry != 'American Samoa':
                    my_list.append(entry)
    return my_list


def count_USstate(USstate):
    from collections import Counter
    count_US = [[x,USstate.count(x)] for x in set(USstate)]
    US = sorted(count_US)
    states = []
    unique_counts = []
    for row in US:
        states.append(str(row[0]))
        unique_counts.append(float(row[1]))
    unique_states = sorted(set(states))
    unique_states = list(unique_states)
    return unique_states, unique_counts


# calculate numbers of tweets per citizen in a given state
def tweet_per_capita(unique_counts, pop_list):
    freq = []
    count_pop_list = zip(unique_counts, pop_list)
    for row in count_pop_list:
        freq.append(float(row[0]/row[1]))
    maxi = str(max(freq))
    return freq, maxi

### create shp_list
def create_shp_list(shapename_state):
    #shapename_state = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename_state)
    states_shp_list = []
    geo_state_list = []
    geo_state = []
    for item in shpreader.Reader(states_shp).records():
        states_shp_list.append(str(item.attributes['name']))
        geo_state_list.append(item.geometry)
    for item in geo_state_list:
        geo_state.append(item)
    geo_state_shp = zip(states_shp_list, geo_state)
    return geo_state_shp
    

def create_map(geo_state_shp,output_file):
    cmap = mpl.cm.Purples
    shapename_state = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename_state)
    ax = plt.axes([0, 0, 1, 1],projection=ccrs.LambertConformal())
    ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())
    for item in geo_state_shp:
        name = item[0]
        if name in unique_states:
            i = unique_states.index(name)
            number = freq[i]
            ax.add_geometries(item[1], ccrs.PlateCarree(),
                              facecolor=cmap(number/float(maxi), 1),
                              label=name)
        else: 
            ax.add_geometries(item[1], ccrs.PlateCarree(),facecolor='#FAFAFA',label=name)
    plt.draw()
    plt.savefig(output_file)


### call plot function
def call_functions(filename, output_file):
    mydict = import_pops('USpop.csv', 'USpop_new.csv')
    pop_list = create_pop_list(my_dict)
    coordinates = open_file(filename)
    FIPS = FIPS_lookup(coordinates)
    USstate = remove_none(FIPS)
    my_list = remove_US_territories(USstate)
    unique_states, unique_counts = count_USstate(my_list)
    freq, maxi = tweet_per_capita(unique_counts, pop_list)
    geo_state_shp = create_shp_list('admin_1_states_provinces_lakes_shp')
    create_map(geo_state_shp, output_file)
    
call_functions('<add file name with coordinates>', '<name your output>')
