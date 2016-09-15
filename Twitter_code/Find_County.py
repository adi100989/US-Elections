
# coding: utf-8

# In[1]:

import pandas as pd

#!pip install --upgrade pip
#!pip install difflib
import difflib
#!pip install fuzzywuzzy
#!pip install python-Levenshtein
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# In[2]:

def location():
    user = pd.read_csv("00_TwitterData/location_csv.csv",
                          low_memory=False)

    #print user.columns
    location = pd.read_csv("00_TwitterData/List-of-Cities-States-and-Counties_csv.csv",
                          low_memory=False)

    #print location.columns


    for i in xrange(len(user)):
        loc = str(user['location'][i]).lower().split(" ")
        c_list_count = 0
        c_length_count = 0
        c = 0
        possible_county = {}
        for l in loc:
            for j in xrange(len(location)):
                if not l == '' and (str(" "+l+" ") in str(" "+str(location['City'][j]) + " ").lower()) : 
                                    #or str(" "+l+" ") in str(" "+str(location['County'][j])+ " ").lower()) :    
                    if not (location['County'][j],location['City'][j]) in possible_county: 
                        possible_county.update({(location['County'][j],location['City'][j]) : [1,len(l)]})
                    else : 
                        possible_county[(location['County'][j],location['City'][j])][0] += 1
                        possible_county[(location['County'][j],location['City'][j])][1] += len(l)
                    #print i,"  ", loc ,"   ", location['County'][j],"   ", location['City'][j]
        print possible_county
        return
    
    
#location()    


# In[3]:

#http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/

#Another method to use fuzzy logic to find best match

from difflib import SequenceMatcher
#m = SequenceMatcher(None, "NEW YORK METS", "NEW YORK MEATS")
#m.ratio() ⇒ 0.962962962963


def FuzzyLocation():
    user = pd.read_csv("00_TwitterData/location_csv_2.csv",
                          low_memory=False)
    
    #print user.columns
    location = pd.read_csv("00_TwitterData/LookupCounty.csv",
                          low_memory=False)
    
    i = 0
    filename = "00_TwitterData/finalCounty_output.csv"
    target = open(filename, 'w')
    target.truncate()
    target.write("DF#")
    target.write(",")
    target.write('City')
    target.write(",")
    target.write('County')
    target.write(",")
    target.write('State')
    target.write(",")
    target.write('TweetLoc')
    target.write(",")    
    target.write("RatioFuzzy")
    target.write('\n')
    
    
    #print location.columns

    for i in range(4717,6000):
        loc = str(user['location'][i]).lower()
        s = " "
        max_score = 0
        if str(user['location'][i]).lower() == " " or str(user['location'][i]).lower().strip() == "" :
            target.write(str(i))
            target.write(",")
            target.write("")
            target.write(",")
            target.write("")
            target.write(",")
            target.write("")
            target.write(",")
            target.write(str(user['location'][i]).lower())
            target.write(",")
            target.write("")
            target.write('\n')
            #print i," is blank"
            continue
        for j in xrange(len(location)):
            strList = [str(location['City'][j]).lower(), str(location['County'][j]).lower(), str(location['State'][j]).lower()]
            str1 = s.join(strList)
            if max_score <= fuzz.partial_ratio(str1,loc):
                max_score = fuzz.partial_ratio(str1,loc)
                max_list = strList
                max_index = j
        target.write(str(i))
        target.write(",")
        target.write(str(location['City'][max_index]).lower())
        target.write(",")
        target.write(str(location['County'][max_index]).lower())
        target.write(",")
        target.write(str(location['State'][max_index]).lower())
        target.write(",")
        target.write(str(user['location'][i]).lower())
        target.write(",")
        target.write(str(max_score))
        target.write('\n')
        
            #print fuzz.ratio(str1,loc), fuzz.partial_ratio(str1,loc) , str1, loc
        
    target.close()

FuzzyLocation()


# In[21]:

def ReadnReplaceCounty():
    Codes = pd.read_csv("00_TwitterData/StateCodes.csv",
                          low_memory=False)
    location = pd.read_csv("00_TwitterData/List-of-Cities-States-and-Counties_csv.csv",
                          low_memory=False)
    codesDict = {}
    
    for i in xrange(len(Codes)):
        codesDict[Codes['Postal Code'][i]]= Codes['State'][i]
    
    #print location.columns    
    
    filename = "00_TwitterData/LookupCounty.csv"
    target = open(filename, 'w')
    target.truncate()
    target.write('Zipcode')
    target.write(",")
    target.write('City')
    target.write(",")
    target.write('County')
    target.write(",")
    target.write('State')
    target.write('\n')
    #target.close()
    
    for i in xrange(len(location)):
        target.write(str(location['ZipCode'][i]))
        target.write(",")
        target.write(str(location['City'][i]).lower())
        target.write(",")
        target.write(str(location['County'][i]).lower())
        target.write(",")
        if not (str(location['State'][i][0:2]).replace('\n','').strip()) in codesDict:
            target.write(" ")
        else:    
            target.write(codesDict[str(location['State'][i][0:2]).replace('\n','').strip()].lower())
        target.write('\n')
    target.close()
    del(codesDict)    
#ReadnReplaceCounty()




