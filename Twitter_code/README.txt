1. countyWiseScores.py =  
	-calculates rthe aggregation of sentiment scores weighted by re-tweet value of each tweet by county and writes to console per candidate
	-calculates the aggregation of popularity scores weighted by the #followersof each user by county and writes to console per candidate
	-aggregates all votes by state and writes to console per candidate

2. Find_County.py 
	-using fuzzy logic matching calculates the closest match a user's profile's location matches to the 
		location (county/state/city) from the list of already known US city/state/county names

3.FindingLocation.py 
	-scrap the twitter accounts of users using streaming API and find the profile location of each user
			
4. separate_tweets.py
	-use regex to seaparate each tweet according to the candidate 
	- if tweet contains hashtag then the whole tweet would go to the particular candidate
	- if a word mention occurs then it will get 0.25 contribution towards the candidate.
