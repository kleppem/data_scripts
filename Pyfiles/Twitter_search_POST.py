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




"""
This loop stores every 100 tweets in a seperate txt file:
keyword: add your query term
id_start: add your id to start your search
n: how many loops to do
count: how many tweets per loop
lang: language
outfile: name of your file to store tweets
"""
def twitter_search(keyword, id_start, n, count, lang, outfile):
    prev_id = int(id_start)
    for i in range(start, end):
        params["max_id"] = str(prev_id)
        url = url1
        req = oauth2.Request(method="GET", url=url, parameters=params) 
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, consumer, token)
        headers = req.to_header()
        url = req.to_url()
        print url #checkpoint 
        print headers
        params["q"] = keyword 
        params["count"] = count 
        params["lang"] = lang
        response = urllib2.Request(url)
        data = json.load(urllib2.urlopen(response))
        if data["statuses"] == []:
            print "end of data"
            break
        else:
       	    prev_id = int(data["statuses"][-1]["id"]) - 1
            print prev_id, i  
        f = open(outfile +str(i) +'.txt', 'w')
        json.dump(data['statuses'], f)
        f.close()
        time.sleep(5) 

twitter_search(keyword, id_start, start, end, count, lang, outfile)
