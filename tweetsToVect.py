"""

 author: Sarah
 script take a collection of tweets for a movie and transform it into a frequency vector
 still to-do:

"""

import numpy as np
import json
import sys
from datetime import datetime

#each movie has a json - dictionary is date and text
    
#these things will  be arguments potentially
rT = datetime.strptime(sys.argv[1],"%d %b %y")
tF = sys.argv[2]



def tweetsToFreq(tweetsFile, releaseTime):
    freq = np.zeros(100) #curently looking at 100 days before release position 0 is 1 day before release... position n is n+1 days before release
    #with open(tweetsFile) as json_data:
    #    tweets = json.loads(json_data)
        
    f = open(tweetsFile)
    text = f.read()
    tweets = json.loads(text)

    for tweet in tweets:    
        #   print tweet['text']
        #print tweet.time #unix
        
        tweet_date = datetime.fromtimestamp(tweet['date'])
        #print tweet_date
        days_before_release = (releaseTime - tweet_date).days
        print days_before_release
        if days_before_release > 30: print tweet['text']
        freq[int(days_before_release)-1] = freq[days_before_release-1]+1
        #use this value to place in the right vector postion
    return freq
        
        
print tweetsToFreq(tF,rT)

#np.savetxt("freqMovies.data", freq_vect, delimiter=",")
