from pymongo import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from collections import Counter
import ast
import os
import json
from scipy.misc import imread
import matplotlib.cbook as cbook

os.chdir('/Users/kleppem/Documents/Python/Crime_SF_project')

def import_coordinates(x_file,y_file):
	y = []
	x = []
	fy = open(y_file, 'r')
	fx = open(x_file, 'r')
	temp_listy = json.load(fy)
	temp_listx = json.load(fx)
	for item in temp_listy:
    	y.append(float(item))
	fy.close()
	for item in temp_listx:
		x.append(float(item))
	fx.close()
	return x, y

def crime_map(x,y, outfile, title):
    fig = plt.figure(figsize=(10,5))
    m = Basemap(llcrnrlon=-122.5365,llcrnrlat=37.7081,urcrnrlon=-122.3274,urcrnrlat=37.8101,
                projection='merc',resolution='h')
    im = plt.imread('Background2.tif')
    m.imshow(im, interpolation='lanczos', origin='upper')
    m.drawmapboundary(fill_color='white')
    x1,y1=m(x,y)
    m.scatter(x1,y1,s=5,c='r',marker="o",cmap=cm.jet,alpha=1.0)
    plt.title(title)
    plt.draw
    plt.savefig(outfile)

def call_functions(x_file, y_file, outfile, title):
	x, y = import_coordinates(x_file, y_file)
	crime_map(x,y, outfile, title)
