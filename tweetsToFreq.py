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
sys.argv[1] = releaseTime
sys.argv[2] = tweetsFile

def tweetsToFreq


with open(tweetsFile) as json_data:
    tweets = json.loads(json_data)

for tweet in tweets
    print tweet.time #unix
    print datetime.fromtimestamp(tweet.time)
    #use this value to place in the right vector postion

np.savetxt("freqMovies.data", freq_vect, delimiter=",")
