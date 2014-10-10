import json
import csv
import pandas as pd
import pylab
import matplotlib.pyplot as plt
import os

""" set working file directory"""
os.chdir('<add your working directory')


def create_main_df(filename):
    my_csv= pd.read_csv(filename)
    csv_dict = my_csv.to_dict()
    DayOfWeek = csv_dict['DayOfWeek']
    district = csv_dict['PdDistrict']
    Time = csv_dict['Time']
    coordinates = csv_dict['Location']
    crime_type = csv_dict['Category']
    my_df = pd.DataFrame(my_csv, columns = ['ata', 'Category','Descript', 'DayOfWeek', 'Date', 'Time', 'PdDistrict', 'Resolution', 'Address', 'X','Y', 'Location'])
    return my_df, my_csv

def crimes_by_time(my_df):
""" create plot showing crimes per time"""
    idf = my_df.set_index(['PdDistrict'])
    idf.Category.value_counts().plot(kind='bar', title= ' # crimes per type')
    ylabel('Number of crimes')
    xlabel('District')
    plt.xticks(rotation=90)
    pylab.ylim([0,10000])

def create_by_day(my_df):
#Plot crimes per day
    idf = my_df.set_index(['PdDistrict'])
    idf.DayOfWeek.value_counts().plot(kind='bar', title= ' # crimes per day of week')
    ylabel('Number of crimes')
    xlabel('District')
    plt.xticks(rotation=90)
    pylab.ylim([0,6000])

def convert_time(my_csv):
    csv_dict = my_csv.to_dict()
    Time = list(csv_dict['Time'].values())
    time = pd.to_datetime(Time) #converting to timestamp
    Time_c = list(time.map(lambda x: x.strftime('%H:%M')))
    count_times = [(x,Time_c.count(x)) for x in set(Time_c)]
    return count_times

def create_count_time(count_times):
    count_times.sort()
    time = []
    count_t = []
    for entry in count_times:
        time.append(entry[0])
        count_t.append(entry[1])
    return time, count_t

def create_time_nobins(count_t, time):
    time_series = pd.Series(count_t, index = time)
    time_series.plot(title = 'Number of crimes per daytime')
    ylabel('Number of crimes')
    xlabel('Daytime')
    plt.xticks(rotation=45)

def add_time_range(count_times):
	""" append tuples with time range"""
    temp_list = []
    for entry in count_times:
        if entry[0] > '00:00' and entry[0] <= '03:00':
            entry += ('0:01 - 3:00',)
            temp_list.append(entry)
        else:
            if entry[0] > '03:00' and entry[0] <= '06:00':
                entry += ('3:01 - 6:00',)
                temp_list.append(entry)
            else:
                if entry[0] > '06:01' and entry[0] <= '09:00':
                    entry += ('6:01 - 9:00',)
                    temp_list.append(entry)
                else:
                    if entry[0] > '09:01' and entry[0] <= '12:00':
                        entry += ('9:01 - 12:00',)
                        temp_list.append(entry)
                    else:
                        if entry[0] > '12:01' and entry[0] <= '15:00':
                            entry += ('12:01 - 15:00',)
                            temp_list.append(entry)
                        else:
                            if entry[0] > '15:01' and entry[0] <= '18:00':
                                entry += ('15:01 - 18:00',)
                                temp_list.append(entry)
                            else:
                                if entry[0] > '18:01' and entry[0] <= '21:00':
                                    entry += ('18:01 - 21:00',)
                                    temp_list.append(entry)
                                else:
                                    if entry[0] > '21:01':
                                        entry+= ('21:01 - 00:00',)
                                        temp_list.append(entry)
    return temp_list

def create_by_time_bins(temp_list):
    temp_list.sort()
    times_df = pd.DataFrame(temp_list,columns = ['Time', '# number of crimes', 'time_range'])
    times_df.groupby('time_range', sort=False).sum().plot(title = '# number of crimes by time')
    ylabel(' # number of crimes')
    xlabel('Time')
    plt.xticks(rotation=90)
    pylab.ylim([0,7000])

def create_car_theft(my_df):
    car_theft = my_df[my_df.Category == 'VEHICLE THEFT']
    car_theft.PdDistrict.value_counts().plot(kind='bar', title=' # of VEHICLE THEFTS per district')
    ylabel('Number of crimes: VEHICLE THEFT')
    xlabel('District')

#numbers of VEHICLE THEFTS per district
def create_crime_type_per_district(my_df, crime, crime_name, plot_title):
	""" function to depict the number of a specific crime type for each district"""
    crime = my_df[my_df.Category == crime_name]
    crime.PdDistrict.value_counts().plot(kind='bar', title= plot_title)
    ylabel('Number of crimes:' +crime_name)
    xlabel('District')
    return crime

def combine_crime_types_per_district(crime1, crime2, crime3, crime4, label1, label2, label3, label4, ttl):
	""" plot different crime types per district"""
    crime1.PdDistrict.value_counts().plot(label = label1, title = ttl)
    crime2.PdDistrict.value_counts().plot(label= label2)
    crime3.PdDistrict.value_counts().plot(label = label3)
    crime4.PdDistrict.value_counts().plot(label = label4)
    ylabel('Number of crimes')
    xlabel('District')
    plt.xticks(rotation=90)
    plt.legend(prop={'size':12})

def create_district_data(my_df):
	""" other option to plot crime_types per distirct"""
    richmond = my_df[my_df.PdDistrict == 'RICHMOND']
    park = my_df[my_df.PdDistrict == 'PARK']
    southern = my_df[my_df.PdDistrict == 'SOUTHERN']
    northern = my_df[my_df.PdDistrict == 'NORTHERN']
    central = my_df[my_df.PdDistrict == 'CENTRAL']
    bayview = my_df[my_df.PdDistrict == 'BAYVIEW']
    taraval = my_df[my_df.PdDistrict == 'TARAVAL']
    ingleside = my_df[my_df.PdDistrict == 'INGLESIDE']
    mission = my_df[my_df.PdDistrict == 'MISSION']
    tenderloin = my_df[my_df.PdDistrict == 'TENDERLOIN']
    data = {'Richmond' : richmond.Category.value_counts(), 'Park' : park.Category.value_counts(),
        'Southern' : southern.Category.value_counts(),'Northern' : northern.Category.value_counts(),
        'Central' : central.Category.value_counts(),'Bayview' : bayview.Category.value_counts(),
        'Taraval' : taraval.Category.value_counts(),'Ingleside' : ingleside.Category.value_counts(),
        'Mission' :mission.Category.value_counts(),'Tenderloin' : tenderloin.Category.value_counts()}
    return data

def create_all_crimes(my_csv):
    csv_dict = my_csv.to_dict()
    all_crimes = list(csv_dict['Category'].values())
    list_crimes = []
    for entry in all_crimes:
        if not entry in list_crimes:
            list_crimes.append(entry)
    return list_crimes

def plot_all_crimes(data, list_crimes):
    df = pd.DataFrame(data, index = list_crimes)
    df.plot(title = '# crimes per district')
    ylabel('Number of crimes')
    xlabel('Crime type')
    plt.xticks(rotation=90)
    plt.legend(loc = 2, prop={'size':9})


""" different functions to tie together above listed functions"""
def call_function_crimes_by_(filename):
	""" by time, by date, by district"""
	my_df, my_csv = create_main_df(filename)
	crimes_by_time(my_df)
	create_by_day(my_df)
	create_car_theft(my_df)

def call_bin_times(filename):
	my_df, my_csv = create_main_df(filename)
	count_times = convert_time(my_csv)
	time, count_t = create_count_time(count_times)
	create_time_nobins(count_t, time)
	temp_list = add_time_range(count_times)
	create_by_time_bins(temp_list)

def call_function_crimes_by_district(filename, crime, crime_name, plot_title):
	my_df, my_csv = create_main_df(filename)
	create_crime_type_per_district(my_df, crime, crime_name, plot_title)
	
def call_function_to_create_plot_all_crimes(filename):
	my_df, my_csv = create_main_df(filename)
	data = create_district_data(my_df)
	list_crimes = create_all_crimes(my_csv)   
	plot_all_crimes(data, list_crimes)
