from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
#pip install nltk
#pip install twython
#consumer key, consumer secret, access token, access secret.
ckey="wKVES4GoW6nJMO958exMYzKNn"
csecret="3n5mY2K2jflCFBCRX34ELIa5LXjStSe0Vpuhl048WxJ3HUr0YM"
atoken="2366732576-3v1uEedyyXD2HxKm7z72NoHnQfo3L1JRnlAbBl2"
asecret="06tsmmcQfIv0vM1KP2wIU31S5yjh50ZdIXcZCBaa3CMzM"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"].encode('utf-8')
        sid = SentimentIntensityAnalyzer()
        #ss = sid.polarity_scores(tweet)
        #for k in sorted(ss):
        #    print('{0}: {1}, '.format(k, ss[k]))
        #    print()
        print(tweet)
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Donaldtrump"])