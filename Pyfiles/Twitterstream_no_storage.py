# Twitter stream without saving tweets

CONSUMER_KEY = '<fill in your consumer key>'
CONSUMER_SECRET ='<fill in your consumer secret>'
OAUTH_TOKEN = '<fill in your oauth token>'
OAUTH_TOKEN_SECRET = '<fill in your oauth token secret>'


config = { 'oauth_token': OAUTH_TOKEN ,'oauth_token_secret': OAUTH_TOKEN_SECRET,
          'key': CONSUMER_KEY, 'secret': CONSUMER_SECRET}

ts = TwitterStream(
                    auth=OAuth(
                        config['oauth_token'],
                        config['oauth_token_secret'],
                        config['key'],
                        config['secret']
                        )
                 )

#http://darkmattersheep.net/2013/09/using-twitter-api-with-python/
def twitter_stream(words):
    screen_name = []
    time = []
    text = []
    location = []
    stop = datetime.now() + timedelta(hours=0.5)
    openstream = ts.statuses.filter(track=words)
    for item in openstream:
        if item['coordinates'] != None:
            screen_name.append(item['user']['screen_name'])
            time.append(datetime.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            text.append(item['text'])
            location.append(item['coordinates'])
        if datetime.now() > stop:
            print datetime.now().isoformat()
            break
    print screen_name, time, text, location

twitter_stream('<add your keyword>')




