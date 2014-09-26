### Twitter search (adapted from Joe Bob Hester)

### search is output as pkl file

def twitter_search(keyword):
    my_list=[]
    f = open('outfile.pkl', 'w')
    pickle.dump(my_list, f)
    f.close()
    for i in range(1):
        url = url1
        req = oauth2.Request(method="GET", url=url, parameters=params) 
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, consumer, token)
        headers = req.to_header()
        url = req.to_url()
    statuses = []    
    for i in range(100):
        params["q"] = keyword
        params["count"] = 100 #INSERT INTEGER FROM 1 TO 100
        response = urllib2.Request(url)
        data = json.load(urllib2.urlopen(response))
        if data["statuses"] == []:
            print "end of data"
            break
        else:
            #print data["statuses"]
            statuses.append(data['statuses'])
        f = open('outfile.pkl', 'r')
        my_list = pickle.load(f)
        f.close()
        my_list.append(statuses)
        f = open('outfile.pkl', 'w')
        pickle.dump(my_list, f)
        f.close()
        time.sleep(300) #to prevent excess of calls allowed to Twitter API
    return statuses