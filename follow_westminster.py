'''Tweet Streaming API consumer'''
import twitter
import csv

# == OAuth Authentication ==
consumer_key="bfnYWWRII9b89MyA48fRL9vAS"
consumer_secret="MFL3X6QHDJnYpyzUru02h5XAB5XHengFSgZF7qjCAPdnURP2J9"
access_token="2745374669-RkZQwSKaLUBMynGVRktnw6DDnz69gcXVNsQ63hP"
access_token_secret="NYDPU0INK92YSCKbX7JOpWzE9c8VHUmItLHb6DyeCcdFq"


AUTH = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
TWITTER_API = twitter.Twitter(auth=AUTH)

# == Put results in csv file ==

csvfile = open('Westmnister.csv', 'w')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['created_at',
                    'user-screen_name',
                    'text',
                    'coordinates lng',
                    'coordinates lat',
                    'place',
                    'user-location',
                    'user-geo_enabled',
                    'user-lang',
                    'user-time_zone',
                    'user-statuses_count',
                    'user-followers_count',
                    'user-friends_count',
                    'user-created_at',
                    'user-source'])

# == Query terms ==

q = "Westminster"
print 'Filtering the public timeline for keyword="%s"' % (q)
twitter_stream = twitter.TwitterStream(auth=TWITTER_API.auth)
stream = twitter_stream.statuses.filter(track=q)


''' helper functions, clean data, unpack dictionaries '''
def getVal(val):
    clean = ""
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return val
    if val:
        clean = val.encode('utf-8')
    return clean

def getLng(val):
    if isinstance(val, dict):
        return val['coordinates'][0]

def getLat(val):
    if isinstance(val, dict):
        return val['coordinates'][1]

def getPlace(val):
    if isinstance(val, dict):
        return val['full_name'].encode('utf-8')


# main loop
for tweet in stream:
    try:
        csvwriter.writerow([tweet['created_at'],                        # write lots of data!!
                            getVal(tweet['user']['screen_name']),
                            getVal(tweet['text']),
                            getLng(tweet['coordinates']),
                            getLat(tweet['coordinates']),
                            getPlace(tweet['place']),
                            getVal(tweet['user']['location']),
                            getVal(tweet['user']['geo_enabled']),
                            getVal(tweet['user']['lang']),
                            getVal(tweet['user']['time_zone']),
                            getVal(tweet['user']['statuses_count']),
                            getVal(tweet['user']['followers_count']),
                            getVal(tweet['user']['friends_count']),
                            getVal(tweet['user']['created_at']),
                            getVal(tweet['source'])
                            ])
        csvfile.flush()
        print getVal(tweet['user']['screen_name']), getVal(tweet['text']), tweet['coordinates'], getPlace(tweet['place'])
    except Exception as e:
        print e.message
