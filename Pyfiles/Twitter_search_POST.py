import oauth2
import time
import urllib2
import json
import pandas as pd

url1 ="https://api.twitter.com/1.1/search/tweets.json"
params = {"oauth_version":"1.0","oauth_nonce": oauth2.generate_nonce(),"oauth_timestamp":int(time.time())}

consumer = oauth2.Consumer(key='<add your key>', secret='<add your secret>')
token = oauth2.Token(key='<add your token>',secret='<add your token_secret>')

params["oauth_consumer_key"] = consumer.key
params["oauth_token_key"] = token.key


prev_id = int('<add your start id>')

### this loop stores every 100 tweets in a seperate txt file
for i in range(100):
	params["max_id"] = str(prev_id)
    url = url1
    req = oauth2.Request(method="GET", url=url, parameters=params) 
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, token)
    headers = req.to_header()
    url = req.to_url()
    print url #checkpoint 
    print headers
    params["q"] = keyword #add your personal keyword for which you want to get tweets
    params["count"] = 100 #INSERT INTEGER FROM 1 TO 100
    params["lang"] = "en"
    response = urllib2.Request(url)
    data = json.load(urllib2.urlopen(response))
    if data["statuses"] == []:
        print "end of data"
        break
    else:
       	prev_id = int(data["statuses"][-1]["id"]) - 1
        print prev_id, i  #checkpoint to make sure prev_id changes
    f = open('<add your filename of choice>' +str(i) +'.txt', 'w')
    #Example f = open('raw_vegan_' +str(i) +'.txt', 'w')
    json.dump(data['statuses'], f)
    f.close()
    time.sleep(5) #to prevent excess of calls allowed to Twitter API
