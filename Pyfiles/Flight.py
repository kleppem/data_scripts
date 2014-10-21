import os
import json
import csv
import pandas as pd
import pylab
import matplotlib.pyplot as plt

def open_file(filename):
    csv= pd.read_csv(filename)
    csv_d = csv.to_dict()
    k = csv_d.keys()
    df = pd.DataFrame(csv_d, columns =[k])
    return csv, csv_d, k, df

def flight_frequency(df):
    grouped = df.groupby('airport').arr_flights.sum().order()
    grouped[-10:].plot(kind='barh', color = 'g', title = 'Top10 Airports: Number of Arriving Flights') 
    xlabel('# Number of arriving flights')
    ylabel('Airports')
    plt.grid(False)
    Top10 = dict(grouped[-10:])
    return Top10

def overview(df):
    tot_all = df.arr_flights.sum()
    tot_dl = df.arr_del15.sum()
    late = (float(tot_dl)/tot_all)*100
    on_time = 100-late
    d = {'On_time': on_time, 'Delayed': late}
    labels = ('Delayed', 'On Time')
    cmap = plt.cm.prism
    fig = plt.figure(figsize=[10, 10])
    colors = cmap(np.linspace(0., 1., len(d)))
    mpl.rcParams['font.size'] = 12.0
    plt.pie(d.values(), autopct='%1.1f%%', colors = colors, labels = labels, startangle = 90, shadow = False,pctdistance=0.6, labeldistance=1.1,)
    plt.title('Flight Delays in the U.S.')
    figure(figsize=(8,8))
    plt.show()

def delays(df):
    tot_aircraft = df.late_aircraft_ct.sum()
    tot_carrier = df.carrier_ct.sum()
    tot_security = df.security_ct.sum()
    tot_nas = df.nas_ct.sum()
    tot_weather = df.weather_ct.sum()
    tot_d = {'Late Aircraft Delay': tot_aircraft, 'Carrier Delay': tot_carrier, 'Security Delay': tot_security, 'Nas Delay': tot_nas, 'Weather Delay': tot_weather}
    labels = tot_d.keys()
    cmap = plt.cm.prism
    fig = plt.figure(figsize=[10, 10])
    colors = cmap(np.linspace(0., 1., len(tot_d)))
    mpl.rcParams['font.size'] = 12.0
    plt.pie(tot_d.values(), autopct='%1.1f%%', labels = labels, startangle = 90, colors = colors, pctdistance=0.6)
    plt.title('US Delay Cause Impact on the Airline on Time of Arrival, Total Delay Count')
    plt.show()

def stats_airline(df, name):
	airline = df[df.carrier == name]
	stats = airline.describe()
	return stats

def top10_destinations(df, name):
	""" Top10 US Destinations of a given airline """
    idf = df.set_index(['carrier','airport']).ix[name]
    idf[0:11].arr_flights.order().plot(kind='bar', title = 'Top10 U.S. Destinations of Airline:' +name)
    xlabel('Airport')
    ylabel('# number of flights')

def top10_delay(df, name):
	""" Top10 Airports with most # numbers of delayed flights by airline"""
    idf = df.set_index(['carrier','airport'])
    c_ix = idf.ix[name].arr_del15.order()
    c_ix[-10:].plot(kind='bar', title = 'Top10 Desitnations of Airline:' +name)
    xlabel('Airport')
    ylabel('# Number of flights ')

def top10_airports_dest(df):
	""" Top10 Airports by number of cancelled flights """
    grouped = df.groupby('airport').arr_cancelled.sum().order()
    grouped[-10:].plot(kind='bar', title = 'Top10 U.S. Destinations by Number of Cancelled Flights')
    xlabel('Airport')
    ylabel('# Number of flights')

def weather_delay_by_airport(df):
	""" Top10 Airports by minutes of delay due to weather""" 
    grouped = df.groupby('airport').weather_delay.sum().order()
    grouped[-10:].plot()
    xlabel('Airport')
    ylabel('Delay [min]')
    title = 'Total Delay due to Weather'
    xticks(rotation=90)

def popular_airports(df):
	""" Number of airlines landing at a given airport """
    grouped = df.groupby('airport').size().order()
    grouped[-30:].plot(kind='bar',title = 'Diversity of Airlines')
    ylabel('# Number of Airlines')
    xlabel('Airport')

def MyFn(tuples):
    return tuples[-1]

def perc_delay_share(csv_d, k):
	""" Top 10 Airlines with most percentage of flight delays """
    df = pd.DataFrame(csv_d, columns =[k])
    grouped = df.groupby('carrier')
    arr_del_carrier = (grouped.arr_del15.sum()).tolist()
    arr_by_carrier = (grouped.arr_flights.sum()).tolist()
    z = zip(arr_by_carrier, arr_del_carrier)
    v = []
    for c in z:
        temp = float(c[1])/c[0]
        v.append(temp)
    kc = sorted(set(list(csv_d['carrier'].values())))
    perc = sorted(zip(kc, v), key=MyFn, reverse = True)
    return perc

def plot_perc_airlines(perc):
    df = pd.DataFrame(perc, columns = ['Airline', 'Percentage Delayed'])
    df.set_index('Airline', inplace=True)
    df[0:11].plot(kind='bar', title = 'Top10 Airlines by Percentage of Delay Share', legend = False)
    xlabel('Airline')
    ylabel('Percentage of Flights Delayed')
    plt.xticks(rotation=90)

def perc_delay_airport(csv_d, k):
	""" Top 10 Airports with highest percentage of flight delays """
    df = pd.DataFrame(csv_d, columns =[k])
    grouped = df.groupby('airport')
    arr_del_carrier = (grouped.arr_del15.sum()).tolist()
    arr_by_carrier = (grouped.arr_flights.sum()).tolist()
    z = zip(arr_by_carrier, arr_del_carrier)
    v = []
    for c in z:
        temp = float(c[1])/c[0]
        v.append(temp)
    kc = sorted(set(list(csv_d['airport'].values())))
    perc = sorted(zip(kc, v), key=MyFn, reverse = True)
    return perc

def plot_perc_airport(perc):
    df = pd.DataFrame(perc, columns = ['Airport', 'Percentage Delayed'])
    df.set_index('Airport', inplace=True)
    df[0:11].plot(kind='barh', title = 'Top10 Airports by Percentage of Delay', legend= False, color = 'r')
    xlabel('Percentage of Delayed Flights')
    ylabel('Airports')
    plt.grid(False)
    plt.xticks(rotation=0)

def routes_map(lat,lon, a):
    fig = plt.figure(figsize=(10,5))
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    m.drawcoastlines()
    m.drawstates(color='black')
    m.drawmapboundary(fill_color='w')
    x, y = m(lon,lat)
    m.scatter(x,y,50,marker='x',color='r')
    plt.title("Airport hubs")
    plt.show()

##	lat/lon searched online and manually generated