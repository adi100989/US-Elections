
# coding: utf-8

# In[5]:

import sys
import string
get_ipython().system(u'pip install simplejson')
import simplejson
get_ipython().system(u'pip install twython')
from twython import Twython
import pandas as pd


# In[23]:

APP_KEY = 'wKVES4GoW6nJMO958exMYzKNn'
APP_SECRET = '3n5mY2K2jflCFBCRX34ELIa5LXjStSe0Vpuhl048WxJ3HUr0YM'
OAUTH_TOKEN = '2366732576-3v1uEedyyXD2HxKm7z72NoHnQfo3L1JRnlAbBl2'
OAUTH_TOKEN_SECRET = '06tsmmcQfIv0vM1KP2wIU31S5yjh50ZdIXcZCBaa3CMzM'

APP_KEY_arjun = 'pkgmF5NroKlD81NBdqs01daYD'
APP_SECRET_arjun = '6tNHiFpXpFBUX5rbFE11qEQ7fllkOXFWGGUH5ZJGZB7FpzmHaZ'
OAUTH_TOKEN_arjun = '499679470-qtSr2iNOwg5nJqdMTxuWwtTFvaNLzKYI48ZFMtUY'
OAUTH_TOKEN_SECRET_arjun = 'LY4INo7ngMS9YkIpCd6LS3kOVA1Y3F22a9uAuNFbybpFo'


t = Twython(app_key=APP_KEY, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET,
    oauth_token=OAUTH_TOKEN,
    oauth_token_secret=OAUTH_TOKEN_SECRET)

t_arjun = Twython(app_key=APP_KEY_arjun, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_arjun,
    oauth_token=OAUTH_TOKEN_arjun,
    oauth_token_secret=OAUTH_TOKEN_SECRET_arjun)


# In[38]:

cols = ['id_str','from_user','text','time','user_followers_count','user_friends_count','geo_coordinates']

twitter = pd.read_csv("00_TwitterData/NYPrimaries_29April.csv",
                      usecols = cols, low_memory=False)


c = 1080
for i in range(c,c+170):
    c += 1
    #if c%100 == 0:
    '''
    t_arjun = Twython(app_key=APP_KEY_arjun, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_arjun,
    oauth_token=OAUTH_TOKEN_arjun,
    oauth_token_secret=OAUTH_TOKEN_SECRET_arjun)
    
    t = Twython(app_key=APP_KEY, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET,
    oauth_token=OAUTH_TOKEN,
    oauth_token_secret=OAUTH_TOKEN_SECRET)
    '''
    
    users = t_arjun.lookup_user(screen_name = str(twitter['from_user'][i]).strip())
    for entry in users:
    #CREATE EMPTY DICTIONARY

    #ASSIGN VALUE OF 'ID' FIELD IN JSON TO 'ID' FIELD IN OUR DICTIONARY
    #r['id'] = entry['id']
    #SAME WITH 'SCREEN_NAME' HERE, AND FOR REST OF THE VARIABLES
    #r['screen_name'] = entry['screen_name']
    #r['location'] = entry['location']
        print c,",",entry['id'],",",entry['screen_name'],",", entry['location']   

