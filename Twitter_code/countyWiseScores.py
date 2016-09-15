
# coding: utf-8

# In[5]:

from __future__ import division
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


# In[6]:


def SentimentClubbing(person):
    #data load from csv to pandas dataframe
    cols = ['id_str','from_user','text','time','user_followers_count','user_friends_count','geo_coordinates']

    twitter = pd.read_csv("00_TwitterData/NYPrimaries_29April.csv",
                          usecols = cols, low_memory=False)
    
    user_county = pd.read_csv("00_TwitterData/finalCounty_10000.csv",
                          low_memory=False)
    
    sentiment_score = pd.read_csv("00_TwitterData/sentimentscore.csv",
                           low_memory=False)
    
    primary_results = pd.read_csv("00_TwitterData/primary_results.csv")
    
    #find the number of RTs
    RT = []
    for i in xrange(len(twitter)):
        list_split = str(twitter['text'][i]).split('@') 
        RT.append(len(list_split))
         
    
    #twitter.columns
    l = len(twitter)
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
    
    name = person.lower().strip().split(" ")
    personListHashed = []
    personListText = []
    
    if person == "ted cruz":
        for i in xrange(len(twitter)):
            for h in  text_dict[i][1]:
                h = h.strip().lower()
                if name[1] in h and not i in personListHashed:  
                    personListHashed.append(i)
    else :
        for i in xrange(len(twitter)):
            for h in  text_dict[i][1]:
                h = h.strip().lower()
                if name[0] in h or name[1] in h and not i in personListHashed:  
                    personListHashed.append(i)

                    
                    
    if person == "ted cruz":
        for i in xrange(len(twitter)):
            for h in  text_dict[i][0]:
                h = h.strip().lower()
                if name[1] in h and not i in personListText:  
                    personListText.append(i)
    else :
        for i in xrange(len(twitter)):
            for h in  text_dict[i][0]:
                h = h.strip().lower()
                if name[0] in h or name[1] in h and not i in personListText:  
                    personListText.append(i)
                
    #print "%s   %d   %d    %d "%( person , len(personListHashed), len(personListText), len(twitter)) 
    # find all unique counties in primary_results
    
    
    counties = set()
    for i in xrange(len(primary_results)):
        counties.add(primary_results['county'][i].lower())
    
    score_dict = {}
    for county in counties:
        score_dict.update({county:0})
    
    states = set()
    for i in xrange(len(primary_results)):
        states.add(primary_results['state'][i].lower())
    
    score_dict = {}
    score_dict_state = {}
    for state in states:
        score_dict_state.update({state:0})
    
    
    for index in personListText:
        if index > user_county['DF#'][len(user_county)-1]: break
        if not str(user_county['County'][index]) in score_dict:
            continue
        else:
            score_dict[user_county["County"][index]] += ((sentiment_score['compound'][index]*RT[index])/4)
    
    for index in personListHashed:
        if index > user_county['DF#'][len(user_county)-1]: break
        if not str(user_county['County'][index]) in score_dict:
            continue
        else:
            score_dict[user_county["County"][index]] += ((sentiment_score['compound'][index]*RT[index]))
    
    for index in personListText:
        if index > user_county['DF#'][len(user_county)-1]: break
        
        if not str(user_county['State'][index]) in score_dict_state:
            continue
        else:
            score_dict_state[user_county["State"][index]] += ((sentiment_score['compound'][index]*RT[index])/4)
    
    for index in personListHashed:
        if index > user_county['DF#'][len(user_county)-1]: break
        if not str(user_county['State'][index]) in score_dict_state:
            continue
        else:
            score_dict_state[user_county["State"][index]] += ((sentiment_score['compound'][index]*RT[index]))
    
    
    """for e in score_dict_state:
        if score_dict_state[e] != 0:
            print e,",", score_dict_state[e]
    """
    
    for i in xrange(len(primary_results)):
        #if score_dict[e] != 0:
        print primary_results['state'][i],",",primary_results['county'][i],",", score_dict_state[str(primary_results['state'][i]).lower()]
    
    
    
SentimentClubbing("hillary clinton")   


# In[7]:


def FollowersClubbing(person):
   #data load from csv to pandas dataframe
   cols = ['id_str','from_user','text','time','user_followers_count','user_friends_count','geo_coordinates']

   twitter = pd.read_csv("00_TwitterData/NYPrimaries_29April.csv",
                         usecols = cols, low_memory=False)
   
   user_county = pd.read_csv("00_TwitterData/finalCounty_10000.csv",
                         low_memory=False)
   
   sentiment_score = pd.read_csv("00_TwitterData/sentimentscore.csv",
                          low_memory=False)
   
   primary_results = pd.read_csv("00_TwitterData/primary_results.csv")
   
   #find the number of RTs
   RT = []
   for i in xrange(len(twitter)):
       list_split = str(twitter['text'][i]).split('@') 
       RT.append(len(list_split))
        
   
   #twitter.columns
   l = len(twitter)
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
   
   name = person.lower().strip().split(" ")
   personListHashed = []
   personListText = []
   
   if person == "ted cruz":
       for i in xrange(len(twitter)):
           for h in  text_dict[i][1]:
               h = h.strip().lower()
               if name[1] in h and not i in personListHashed:  
                   personListHashed.append(i)
   else :
       for i in xrange(len(twitter)):
           for h in  text_dict[i][1]:
               h = h.strip().lower()
               if name[0] in h or name[1] in h and not i in personListHashed:  
                   personListHashed.append(i)

                   
                   
   if person == "ted cruz":
       for i in xrange(len(twitter)):
           for h in  text_dict[i][0]:
               h = h.strip().lower()
               if name[1] in h and not i in personListText:  
                   personListText.append(i)
   else :
       for i in xrange(len(twitter)):
           for h in  text_dict[i][0]:
               h = h.strip().lower()
               if name[0] in h or name[1] in h and not i in personListText:  
                   personListText.append(i)
               
   #print "%s   %d   %d    %d "%( person , len(personListHashed), len(personListText), len(twitter)) 
   # find all unique counties in primary_results
   
   
   counties = set()
   for i in xrange(len(primary_results)):
       counties.add(primary_results['county'][i].lower())
   
   score_dict = {}
   for county in counties:
       score_dict.update({county:0})
   
   states = set()
   for i in xrange(len(primary_results)):
       states.add(primary_results['state'][i].lower())
   
   score_dict = {}
   score_dict_state = {}
   for state in states:
       score_dict_state.update({state:0})
   
   
   for index in personListText:
       if index > user_county['DF#'][len(user_county)-1]: break
       if not str(user_county['County'][index]) in score_dict:
           continue
       else:
           score_dict[user_county["County"][index]] += ((twitter['user_followers_count'][index])/4)
   
   for index in personListHashed:
       if index > user_county['DF#'][len(user_county)-1]: break
       if not str(user_county['County'][index]) in score_dict:
           continue
       else:
           score_dict[user_county["County"][index]] += ((twitter['user_followers_count'][index]))
   
   for index in personListText:
       if index > user_county['DF#'][len(user_county)-1]: break
       
       if not str(user_county['State'][index]) in score_dict_state:
           continue
       else:
           score_dict_state[user_county["State"][index]] += ((twitter['user_followers_count'][index])/4)
   
   for index in personListHashed:
       if index > user_county['DF#'][len(user_county)-1]: break
       if not str(user_county['State'][index]) in score_dict_state:
           continue
       else:
           score_dict_state[user_county["State"][index]] += ((twitter['user_followers_count'][index]))
   
   
   """for e in score_dict_state:
       if score_dict_state[e] > 0:
           print e, score_dict_state[e]
   
   
   for e in score_dict:
       if score_dict[e] > 0:
           print e, score_dict[e]"""
   
   for i in xrange(len(primary_results)):
       #if score_dict[e] != 0:
       print primary_results['state'][i],",",primary_results['county'][i],",", score_dict_state[str(primary_results['state'][i]).lower()]


FollowersClubbing("hillary clinton")   


# In[8]:

def genClubbing(person):
    #data load from csv to pandas dataframe
    cols = ['id_str','from_user','text','time','user_followers_count','user_friends_count','geo_coordinates']

    twitter = pd.read_csv("00_TwitterData/NYPrimaries_29April.csv",
                          usecols = cols, low_memory=False)
    
    user_county = pd.read_csv("00_TwitterData/finalCounty_10000.csv",
                          low_memory=False)
    
    sentiment_score = pd.read_csv("00_TwitterData/sentimentscore.csv",
                           low_memory=False)
    
    primary_results = pd.read_csv("00_TwitterData/primary_results.csv")
    
    #find the number of RTs
    RT = []
    for i in xrange(len(twitter)):
        list_split = str(twitter['text'][i]).split('@') 
        RT.append(len(list_split))
         
    
    #twitter.columns
    l = len(twitter)
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
    
    name = person.lower().strip().split(" ")
    personListHashed = []
    personListText = []
    
    if person == "ted cruz":
        for i in xrange(len(twitter)):
            for h in  text_dict[i][1]:
                h = h.strip().lower()
                if name[1] in h and not i in personListHashed:  
                    personListHashed.append(i)
    else :
        for i in xrange(len(twitter)):
            for h in  text_dict[i][1]:
                h = h.strip().lower()
                if name[0] in h or name[1] in h and not i in personListHashed:  
                    personListHashed.append(i)

                    
                    
    if person == "ted cruz":
        for i in xrange(len(twitter)):
            for h in  text_dict[i][0]:
                h = h.strip().lower()
                if name[1] in h and not i in personListText:  
                    personListText.append(i)
    else :
        for i in xrange(len(twitter)):
            for h in  text_dict[i][0]:
                h = h.strip().lower()
                if name[0] in h or name[1] in h and not i in personListText:  
                    personListText.append(i)
                
    #print "%s   %d   %d    %d "%( person , len(personListHashed), len(personListText), len(twitter)) 
    # find all unique counties in primary_results
    
    
    counties = set()
    for i in xrange(len(primary_results)):
        counties.add(primary_results['county'][i].lower())
    
    score_dict = {}
    for county in counties:
        score_dict.update({county:0})
    
    states = set()
    for i in xrange(len(primary_results)):
        states.add(primary_results['state'][i].lower())
    
    score_dict = {}
    score_dict_state = {}
    for state in states:
        score_dict_state.update({state:0})
    
    
    for index in personListText:
        if index > user_county['DF#'][len(user_county)-1]: break
        if not str(user_county['County'][index]) in score_dict:
            continue
        else:
            score_dict[user_county["County"][index]] += ((sentiment_score['compound'][index]*RT[index])/4)
    
    for index in personListHashed:
        if index > user_county['DF#'][len(user_county)-1]: break
        if not str(user_county['County'][index]) in score_dict:
            continue
        else:
            score_dict[user_county["County"][index]] += ((sentiment_score['compound'][index]*RT[index]))
    
    for index in personListText:
        if index > user_county['DF#'][len(user_county)-1]: break
        
        if not str(user_county['State'][index]) in score_dict_state:
            continue
        else:
            score_dict_state[user_county["State"][index]] += ((sentiment_score['compound'][index]*RT[index])/4)
    
    for index in personListHashed:
        if index > user_county['DF#'][len(user_county)-1]: break
        if not str(user_county['State'][index]) in score_dict_state:
            continue
        else:
            score_dict_state[user_county["State"][index]] += ((sentiment_score['compound'][index]*RT[index]))
    
    
    """for e in score_dict_state:
        if score_dict_state[e] != 0:
            print e,",", score_dict_state[e]
    """
    votes = {}
    sum =  0
    for i in xrange(len(primary_results)):
        if primary_results['state'][i] not in votes and str(primary_results['candidate'][i]).lower().strip() == person.lower().strip() :
            votes.update({primary_results['state'][i]:primary_results['votes'][i]})
        elif  primary_results['state'][i] in votes and str(primary_results['candidate'][i]).lower().strip() == person.lower().strip():   
            votes[primary_results['state'][i]] += primary_results['votes'][i]
        """if primary_results['state'][i] == primary_results['state'][i+1]  and str(primary_results['candidate'][i]).lower().strip() == person.lower().strip() : 
            sum += primary_results['votes'][i] 
        if  i == len(primary_results) -1  and str(primary_results['candidate'][i]).lower().strip() == person.lower().strip():    
            print primary_results['state'][i],",",sum + primary_results['votes'][i]
            sum = 0
        if  i == len(primary_results) -1  and not str(primary_results['candidate'][i]).lower().strip() == person.lower().strip():
            print primary_results['state'][i],",",sum
            sum = 0 
        if not primary_results['state'][i] == primary_results['state'][i+1]  and str(primary_results['candidate'][i]).lower().strip() == person.lower().strip() : 
            print primary_results['state'][i],",",sum
            sum = 0
        """
        
    list_item = []    
    for item in votes:
        list_item.append([item,votes[item]])
    list_item.sort(key=lambda x: x[0])
    
    for item in list_item:
        print item[0],",",item[1]
        
genClubbing("Hillary Clinton") 


# In[4]:

def Aggregation():
    
    
    candidate = pd.read_csv("00_TwitterData/Predict_Hillary Clinton.csv")
    #candidate = pd.read_csv("00_TwitterData/Predict_Bernie Sanders.csv")
    #candidate = pd.read_csv("00_TwitterData/Predict_Donald Trump.csv")
    #candidate = pd.read_csv("00_TwitterData/Predict_Ted Cruz.csv")
    
    votes = {}
    sum =  0
    for i in xrange(len(candidate)):
        if candidate['STATE'][i] not in votes :
            votes.update({candidate['STATE'][i]:candidate['VOTES'][i]})
        elif  candidate['STATE'][i] in votes :   
            votes[candidate['STATE'][i]] += candidate['VOTES'][i]
    
    list_item = []    
    for item in votes:
        list_item.append([item,votes[item]])
    list_item.sort(key=lambda x: x[0])
    
    for item in list_item:
        print item[0],",",int(item[1])
        
Aggregation() 


