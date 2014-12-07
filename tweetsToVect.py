"""

 author: Sarah
 script take a collection of tweets for a movie and transform it into a frequency vector
 still to-do:

"""

import numpy as np
import json
import sys
from datetime import datetime
from TopsySearch import get_movies_and_dates
from textblob import TextBlob


#each movie has a json - dictionary is date and text
    
#these things will  be arguments potentially
#rT = datetime.strptime(sys.argv[1],"%d %b %y")

allMovies = get_movies_and_dates(sys.argv[1])
tweetsFile = sys.argv[2]


def tweetsToFreq(tweets, releaseTime, movie_name):
    freq = np.zeros(180) #curently looking at 100 days before release position 0 is 1 day before release... position n is n+1 days before release
    

    for tweet in tweets:    
        #   print tweet['text']
        #print tweet.time #unix
        
        tweet_date = datetime.fromtimestamp(tweet['date'])
        days_before_release = int((releaseTime - tweet_date).days) #maybe something about countries for timestamp. also hour?
        print(days_before_release),
        #if days_before_release > 30: #print "\t\t", days_before_release, " days ago:", tweet['text']
        if (days_before_release < 180 and days_before_release > 0): 
            freq[days_before_release-1] = freq[days_before_release-1]+1
            #use this value to place in the right vector postion
        
    return freq
    
    
def tweetsSentiment(tweets, releaseTime, movie_name):
    freq = np.zeros(100) #curently looking at 100 days before release position 0 is 1 day before release... position n is n+1 days before release
    
'''
    for tweet in tweets:    
        #   print tweet['text']
        #print tweet.time #unix
       
        if movie_name in tweet.keys():
        
            blob = TextBlob(tweet[movie_name][)
        #make it ignore the actual movie title
            tweet_date = datetime.fromtimestamp(tweet[movie_name]['date'])
        #try:
        #    tweet_date = datetime.fromtimestamp(tweet[movie_name]['date']) #note that this won't happen once every movie has its own file
        #except KeyError:
        #    break
            days_before_release = int((releaseTime - tweet_date).days) #maybe something about countries for timestamp. also hour?
            if days_before_release > 30: print "\t\t", days_before_release, " days ago:", tweet[movie_name]['text']
            if (days_before_release < 100 and days_before_release > 0): 
                freq[days_before_release-1] = freq[days_before_release-1]+1
            #use this value to place in the right vector postion
        
    return ratio,pos_freq,neg_freq
  '''
  
f = open(tweetsFile)
text = f.read()
tweets = json.loads(text)

print tweetsToFreq(tweets, datetime(2014,1,3), "Paranormal Activity The Marked Ones_tweets.txt")
  
#for movie in allMovies[0:50]:

    #open relevant file
#    f = open(tweetsFile)
##    text = f.read()
 #   tweets = json.loads(text)
  #  print movie
   # print tweetsToFreq(tweets, datetime(2014,12,5), movie[0]) #make middle movie[1]


#print tweetsToFreq(tF,rT)

#np.savetxt("freqMovies.data", freq_vect, delimiter=",")
