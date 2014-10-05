#Adopted from http://stackoverflow.com/questions/22684730/heat-world-map-with-matplotlib

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import shapely.geometry as sgeom
import numpy as np
import os
import json
import csv
import cartopy.feature as cfeature
from mpl_toolkits.basemap import Basemap

#import your output from pubmed search (country/count)
os.chdir('<set your directory>')

def import_file(filename):
    f = open(filename, 'rU')
    dict_count = json.load(f)
    f.close()
    return dict_count


def create_count(dict_count):
"""Convert dictionary to two seperate lists; change country names"""
    my_count = []
    my_country = []
    for v in dict_count.values():
        my_count.append(v)
    for k in dict_count.keys():
        my_country.append(str(k))
    for n,i in enumerate(my_country):
        if i=='UK':
            my_country[n]='United Kingdom'
        if i=='USA':
            my_country[n]='United States'
    return my_count, my_country


def create_list(my_country, my_count):
"""create unique sets to import into your mapping function"""
    merged = zip(my_country, my_count)
    count_list = sorted(merged) 
    unique_count = []
    unique_country = []
    for item in count_list:
        unique_country.append(item[0])
        unique_count.append(item[1])
    unique_country = sorted(set(unique_country))
    unique_country = list(unique_country)
    maxi = str(max(unique_count)) 
    return unique_count, unique_country, maxi


def create_geo_shp_country(shapename):
"""fixed a bug with encoding"""
    countries_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename)
    geo_shp_list = []
    geo = []
    countries_shp_list = []
    for item in shpreader.Reader(countries_shp).records():
        geo_shp_list.append(item.geometry)
        countries_shp_list.append(str(item.attributes['name_long']))
    for item in geo_shp_list:
        geo.append(item)
    for n,i in enumerate(countries_shp_list):
        if i=="C\xf4te d'Ivoire":
            countries_shp_list[n]=str('d Ivoire') 
    geo_country_shp = zip(countries_shp_list, geo)
    return geo_country_shp


def mapping(outfile):
    cmap = mpl.cm.Blues
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


def call_functions(shapename, filename, outfile):
""" this function ties everything together """
    dict_count = import_file(filename)
    my_count, my_country= create_count(dict_count)
    unique_count, unique_country, maxi = create_list(my_country, my_count)
    geo_shp_country = create_geo_shp_country(shapename)
    mapping(outfile)
    
call_functions('admin_0_countries', '<add dict with counts>','<name your output>')