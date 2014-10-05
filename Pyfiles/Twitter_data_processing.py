import time
import json
import pandas as pd


def create_filenames(number, tweet_loc):
    """ create a list which holds all the names of your created txt files"""
	filenames = []
	for i in range(number): #adjust range number depending on your twitter search 
    	filename = tweet_loc +str(i) + '.txt'
    	filenames.append(filename)
    return filenames


def combine_files(filenames):
    """ combine out json files; name your outfile list """
    data = []
    for name in filenames:
        f = open(name, 'r')
        temp_list = json.load(f)
        for item in temp_list:
            data.append(item)
        f.close()
    print len(data) # to check that everything worked nicely
    return data


def get_info(data):
    """ filter out text, user, time from all tweets """
    text = []
    user_id = []
    time = []
    for item in output:
        text.append(item['text'])
        user_id.append(item['id'])
        time.append(item['created_at'])
    return user_id, text, time


def get_coordinates(output):
    """ get entries with coordinates """
    coordinates = []
    locations = []
    user_id = []
    time = []
    for item in output:
        if item['coordinates'] != None:
            locations.append(item['coordinates'])
            user_id.append(item['id'])
            time.append(item['created_at'])
    for entry in locations:
        coordinates.append(entry['coordinates'])
    return user_id, coordinates, time
    

def split_coordinates(tweets):
    """ split columns in lat and long """
    temp_list = tweets[1]
    longitude = []
    latitude = []
    for entry in temp_list:
        longitude.append(entry[0])
        latitude.append(entry[1])
    return latitude, longitude
    

def export_coordinates(lat, lon, outfile):
    """ export data to use in next script """
    data = zip(lat, lon)
    output = open(outfile, 'w')
    json.dump(data, output)
    output.close()


def create_df_info(info):
    id_tweets = info[0]
    text_tweets = info[1]
    time_tweets = info[2]
    time = pd.to_datetime(time_tweets) #converting to timestamp
    date_tweets = list(time.map(lambda x: x.strftime('%d-%m-%Y'))) #extracting date
    data = zip(id_tweets, text_tweets, date_tweets)
    df = pd.DataFrame(data = data, columns=['ID', 'text', 'time'])
    return df


def create_df_coordinates(tweets):
    """ extract info for dataframe with coordinates, id, time """
    id_tweets = tweets[0]
    coordinates_tweets = tweets[1]
    time_tweets = tweets[2]
    time = pd.to_datetime(time_tweets) #converting to timestamp
    date = list(time.map(lambda x: x.strftime('%m-%d-%Y'))) #extracting date
    data = zip(id_tweets, coordinates_tweets, date)
    df = pd.DataFrame(data = data, columns=['ID', 'coordinates', 'time'])
    return df


def call_functions(number, tweet_loc, outfile): 
    """ call all your functions"""
    filenames = create_filenames(number, tweet_loc)
    data = combine_files(filenames)
    tweets = get_coordinates(data)
    lat, lon = split_coordinates(tweets)
    export_coordinates(lat, lon, outfile)
    info = get_info(data)
    df_coordinates = create_df_coordinates(tweets)
    df_all = create_df_info(info)
    return df_all, df_coordinates

df_all, df_coordinates = call_functions(<'add number of output files'>, <'name of files'>)


######----------------visualization EXAMPLES
def group_by(golf, bike, tennis):  
""" grouped by date """  
    golf_all_time = golf.groupby('time')
    bike_all_time = bike.groupby('time')
    tennis_all_time = tennis.groupby('time')
    return golf_all_time, bike_all_time, tennis_all_time


def plot_bydate(golf, bike, tennis):
	golf.size().plot(kind='area', colors='g', title='golf tweets')
    bike.size().plot(kind='area', colors='b', title='bike tweets')
	tennis.size().plot(kind='area', colors='r', title='tennis tweets')
	plt.xticks(rotation=90)
    legend(loc = 'best')
    ylabel('Number of tweets')

def create_plot(golf, bike, tennis):
    golf_all_time, bike_all_time, tennis_all_time = group_by(golf, bike, tennis)
    plot_bydate(golf_all_time, bike_all_time, tennis_all_time)


create_plot(df_all_golf, df_all_bike, df_all_tennis)





