"""

 author: Sarah
 script take a collection of tweets for a movie and transform it into a frequency vector
 still to-do:

"""

import numpy as np
import json

#each movie has a json - dictionary is date and text

#these things will  be arguments potentially
releaseTime
tweetsFile


with open(tweetsFile) as json_data:
    tweets = json.loads(json_data)
    pprint(d)

for tweet in tweets
    tweet.time #unix  

np.savetxt("freqMovies.data", freq_vect, delimiter=",")
