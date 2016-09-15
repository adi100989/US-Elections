
# coding: utf-8

# In[84]:

#all imports for the project
#import os
#import codecs
import re
import pandas as pd
#import matplotlib.pyplot as plt
#import numpy as np
import sys
#import math
import string
#!pip install simplejson
import simplejson
#!pip install twython
from twython import Twython
#import sys
#reload(sys)


APP_KEY = 'wKVES4GoW6nJMO958exMYzKNn'
APP_SECRET = '3n5mY2K2jflCFBCRX34ELIa5LXjStSe0Vpuhl048WxJ3HUr0YM'
OAUTH_TOKEN = '2366732576-3v1uEedyyXD2HxKm7z72NoHnQfo3L1JRnlAbBl2'
OAUTH_TOKEN_SECRET = '06tsmmcQfIv0vM1KP2wIU31S5yjh50ZdIXcZCBaa3CMzM'

APP_KEY_arjun = 'pkgmF5NroKlD81NBdqs01daYD'
APP_SECRET_arjun = '6tNHiFpXpFBUX5rbFE11qEQ7fllkOXFWGGUH5ZJGZB7FpzmHaZ'
OAUTH_TOKEN_arjun = '499679470-qtSr2iNOwg5nJqdMTxuWwtTFvaNLzKYI48ZFMtUY'
OAUTH_TOKEN_SECRET_arjun = 'LY4INo7ngMS9YkIpCd6LS3kOVA1Y3F22a9uAuNFbybpFo'

APP_KEY_adiSBU = 'Bon5A3T7AZaW7kyusJI7pf5Ot'
APP_SECRET_adiSBU = 'PkP98aFuBFPtezCE1LDTseVT0ATGRfzoyVa4kIVTAo2Fs9QxSL'
OAUTH_TOKEN_adiSBU = '729509909100957696-D0ADym5fnBpzd0dJ6rFn9k5WSrflcrw'
OAUTH_TOKEN_SECRET_adiSBU = '2ouySib9DXNiQTZY5lqBvn6LYgqNvSwLCtvMg8dxf0L41'

APP_KEY_adiSBUCS = 'lLbD9ORBFfUIMeGsrwnBfZrGQ'
APP_SECRET_adiSBUCS = 'N7u8JSrmhKR85vqB6IZzyOKx9KJdfnvQu4ljFIDG2xBmwMi4Bj'
OAUTH_TOKEN_adiSBUCS = '729514377158787072-qnNihsb1WxQRFzRCLwb0ZC4I48APEVy'
OAUTH_TOKEN_SECRET_adiSBUCS = 'TAWcrgfWIbWTtcZiy9013yUlz0c3qDytcs2lmUWav2yKy'

APP_KEY_arjunSBUCS = 'W4zZeGIR0MR0tYii0Vu6SNlkF'
APP_SECRET_arjunSBUCS = '2LZAfZbPgs9D7O84gKVEDN7osuYKl3Ux86xXFWE5MjJvZt9Z4q'
OAUTH_TOKEN_arjunSBUCS = '729515080547749888-MCbzmxteqTiax3zDCWMMiQVoSeWUWwV'
OAUTH_TOKEN_SECRET_arjunSBUCS = 'ezrTiighFRURDZdDnyWBsxstKC2rJaEiBqUGRUVRFm1rz'

APP_KEY_arjunSBU = 'FGEzQJFIHzeJ39wYASL8Mf2xN'
APP_SECRET_arjunSBU = '1whiB251NN9Jxlhgr2SJ8wgQGSAlGq2rqsONjhlzMV3ATJa6AV'
OAUTH_TOKEN_arjunSBU = '729514160707489796-i9RXadwHBEp4Xf3Xj6aoB98v5lmMA5a'
OAUTH_TOKEN_SECRET_arjunSBU = 'f6gnueWxN3wUe1n5s0OdnK6VwLpIR0BCzUnzgTo0gTnw8'

APP_KEY_common = 'LQbUYYM2O5JlcBPyVXwoOqiCL'
APP_SECRET_common = 'oQxjfrAGcuWlvFMlEjHBJ8OUhBDXUNh2C2coPXdbbB1NWG4MiC'
OAUTH_TOKEN_common = '729562653841035264-7iweE7736S64CbvMFTYVg7RSzhg1ZNF'
OAUTH_TOKEN_SECRET_common = 'moXZtJSPB4oW4BiHxZoZ03lKv2n7Tz9RevK6rN7Gfu6ZY'

APP_KEY_upturn = 'gfUGBBM8an9t34x3wTFy4jjzx'
APP_SECRET_upturn = 'LCrC4bn8VPJDPSwYgtFy27n16MamVKwdOrNaMwgxDevOjsskqd'
OAUTH_TOKEN_upturn = '729564148879757312-NREZI2pCh4k4vZnBBFiTPQVi5fZdfAn'
OAUTH_TOKEN_SECRET_upturn = 'ebTaNgRryFCaEaH45HHgUVyruouUJLnPuFnhyMTN5WQEb'

t = Twython(app_key=APP_KEY, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET,
    oauth_token=OAUTH_TOKEN,
    oauth_token_secret=OAUTH_TOKEN_SECRET)

t_arjun = Twython(app_key=APP_KEY_arjun, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_arjun,
    oauth_token=OAUTH_TOKEN_arjun,
    oauth_token_secret=OAUTH_TOKEN_SECRET_arjun)

t_adiSBU = Twython(app_key=APP_KEY_adiSBU, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_adiSBU,
    oauth_token=OAUTH_TOKEN_adiSBU,
    oauth_token_secret=OAUTH_TOKEN_SECRET_adiSBU)

t_adiSBUCS = Twython(app_key=APP_KEY_adiSBUCS, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_adiSBUCS,
    oauth_token=OAUTH_TOKEN_adiSBUCS,
    oauth_token_secret=OAUTH_TOKEN_SECRET_adiSBUCS)

t_arjunSBUCS = Twython(app_key=APP_KEY_arjunSBUCS, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_arjunSBUCS,
    oauth_token=OAUTH_TOKEN_arjunSBUCS,
    oauth_token_secret=OAUTH_TOKEN_SECRET_arjunSBUCS)

t_arjunSBU = Twython(app_key=APP_KEY_arjunSBU, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_arjunSBU,
    oauth_token=OAUTH_TOKEN_arjunSBU,
    oauth_token_secret=OAUTH_TOKEN_SECRET_arjunSBU)

t_common = Twython(app_key=APP_KEY_common, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_common,
    oauth_token=OAUTH_TOKEN_common,
    oauth_token_secret=OAUTH_TOKEN_SECRET_common)

t_upturn = Twython(app_key=APP_KEY_upturn, #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret=APP_SECRET_upturn,
    oauth_token=OAUTH_TOKEN_upturn,
    oauth_token_secret=OAUTH_TOKEN_SECRET_upturn)


# In[92]:

#data load from csv to pandas dataframe
cols = ['id_str','from_user','text','time','user_followers_count','user_friends_count','geo_coordinates']

twitter = pd.read_csv("00_TwitterData/NYPrimaries_29April.csv",
                      usecols = cols, low_memory=False)

#twitter2 = pd.read_csv("D:/00-SUNYSBU/00-Courses/2-2016SPRING/Probability&Statistics/Project files/00_TwitterData/Trump_Cruz_elections_29April.csv",
#                      nrows = 2)


#ids = 'sstroh84,KathyBenjamin,DrJacaranda,mishayah'

#users = t.lookup_user(screen_name = ids)
c = 10768
for i in range(c,c+180):
    try:
        c += 1

        #users = t.lookup_user(id_str = str(twitter['id_str'][i]).strip())
        users = t_upturn.lookup_user(screen_name = str(twitter['from_user'][i]).strip())
        for entry in users:
        #CREATE EMPTY DICTIONARY

        #ASSIGN VALUE OF 'ID' FIELD IN JSON TO 'ID' FIELD IN OUR DICTIONARY
        #r['id'] = entry['id']
        #SAME WITH 'SCREEN_NAME' HERE, AND FOR REST OF THE VARIABLES
        #r['screen_name'] = entry['screen_name']
        #r['location'] = entry['location']
            print str(i),",",entry['id'],",",entry['screen_name'],",",entry['location']   
            #print entry['location']
    except :
        continue
    


# In[82]:

#twitter.columns
l = len(twitter)
i = 0
text_dict = {} 
for i in xrange(len(twitter)):
    topics = []
    
    topics = str(twitter['text'][i]).lower().strip().split(' ')
    #word_pattern=".*[\w|\W|0-9].*"
    pattern1 = "^@.*"
    pattern2 = "^https.*"
    #pattern = '/(^|\b)@\S*($|\b)/'
    replaced = []
    hashed = []
    for words in topics:
        if not (re.match("^#.*",words) or re.match(pattern1,words) or words == 'rt' or re.match(pattern2,words)):
            replaced.append(words)
        if re.match("^#.*",words):
            hashed.append(words)
    text_dict.update({i:[replaced,hashed]})       
    del(topics)
    del(replaced)
    del(hashed)


# In[83]:

donald = []
hillary = []
cruz = []
sanders = []

for i in xrange(len(twitter)):
    
    for h in  text_dict[i][1]:
        #print h
        h = h.strip().lower()
        #if h.find("donald") or h.find("trump"):
        #if re.match(pattern_d,h) and i not in donald:
        if "donald" in h or "trump" in h and not i in donald:  
            donald.append(i)
        #if re.match(pattern_c,h) or h == "#ted" and not h == "#ny" and i not in cruz:
        if "cruz" in h and not i in cruz :
            cruz.append(i)
        if "hillary" in h or "clinton" in h and i not in hillary:
            hillary.append(i)
        if "bernie" in h or "sanders" in h and i not in sanders:
            sanders.append(i)

print "donald %d     hillary %d     sanders %d   cruz %d "%(len(donald),len(hillary),len(sanders),len(cruz))


# In[11]:

#!pip install nltk
#!pip install vaderSentiment
#!pip install --upgrade vaderSentiment
#!pip install --upgrade nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.sentiment import SentimentAnalyzer
import vaderSentiment
import re
#from vaderSentiment import sentiment as vaderSentiment
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

def SentimentCalculation():
    filename = "00_TwitterData/sentimentscore.csv"
    target = open(filename, 'w')
    target.truncate()


    for i in range(0,len(twitter)):
        sentences = []
        string = ""

        for j in twitter['text'][i].strip():
            if ord(j) >= 0 and ord(j) <= 127:
                string += j
        twitter['text'][i] = string  
        lines_list = tokenize.sent_tokenize(twitter['text'][i].strip())
        sentences.extend(lines_list)

        for sentence in sentences:
            vs = vaderSentiment(sentence)
            target.write(str(i))
            #target.write(",")
            #target.write(twitter['text'][i].strip())
            target.write(",")
            target.write(str(vs))
            target.write(",")
            target.write("\n")

            #print i,",",str(vs)
    target.close()        


