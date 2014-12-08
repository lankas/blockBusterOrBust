"""

 author: Sarah
 script take a collection of tweets for a movie and transform it into a frequency vector
 
 two arguments: a file with moves and dates and a file 
 
 still to-do:

"""

import numpy as np
import json
import sys
from datetime import datetime
from TopsySearch import get_movies_and_dates
from textblob import TextBlob
import stop_words

movieDates = get_movies_and_dates(sys.argv[1])
moviesFile = sys.argv[2]

stopwords = stop_words.get_stop_words("english") #https://pypi.python.org/pypi/stop-words

def tweetsToFreq(tweets, releaseTime, movie_name):
    freq = np.zeros(180) #position n is n+1 days before release

    for tweet in tweets:    
        tweet_date = datetime.fromtimestamp(tweet['date'])
        days_before_release = int((releaseTime - tweet_date).days) 

        if (days_before_release < 180 and days_before_release > 0): 
            freq[days_before_release-1] = freq[days_before_release-1]+1
        else:
            print "out of bounds"
        #could do a sanity check on the ones not in this range
    return freq
    
    
def tweetsSentiment(tweets, releaseTime, movie_name):
    pos_freq = np.zeros(180)  
    neg_freq = np.zeros(180)
    ratio = np.zeros(180)
    for tweet in tweets:    
        tweet_processed = removeStopWords(stopwords,tweet['text']) 
        tweet_processed = tweet_processed.replace(str(movie_name),'')  #make it ignore the actual movie title
        blob = TextBlob(tweet_processed) 
        sentiment = blob.sentiment.polarity

        tweet_date = datetime.fromtimestamp(tweet['date'])
        days_before_release = int((releaseTime - tweet_date).days)
        if (days_before_release < 180 and days_before_release > 0): 
            if (sentiment > 0):
                pos_freq[days_before_release-1] = pos_freq[days_before_release-1]+1

            if (blob.sentiment.polarity < 0):
                neg_freq[days_before_release-1] = neg_freq[days_before_release-1]+1
                
            #maybe introduce a neutral option

    return ratio,pos_freq,neg_freq
    
    
def overallTweetSentiment(tweets, releaseTime, movie_name):
    total_pol = 0
    total_subj = 0
    count_tweets = 0
    for tweet in tweets:
        tweet_processed = removeStopWords(stopwords,tweet['text'])
        tweet_processed = tweet_processed.replace(str(movie_name),'')  #make it ignore the actual movie title
        blob = TextBlob(tweet_processed) 
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        total_sent = total_pol + polarity
        total_subj = total_subj + subjectivity
        count_tweets = count_tweets + 1
        
    return total_sent/count_tweets,total_subj/count_tweets
        
    
    
def removeStopWords(toRemove,tweet):
    tweet = ' '.join([word for word in tweet.split() if word not in toRemove])
    return tweet
    
d = open(moviesFile)
text = d.read()
allMovies = json.loads(text)

freqs = np.zeros((0,180))
pos_freqs = np.zeros((0,180))
neg_freqs = np.zeros((0,180))
ratios = np.zeros((0,180))

sentiments = np.zeros((0,2))

movie_key = []

for movie,date in movieDates:
    movie_key.append(movie)
    f = open(allMovies[movie])
    text = f.read()
    tweets = json.loads(text)
    print movie,date
    
    #freq = np.array([tweetsToFreq(tweets, date, movie)])
    #print freq
    #freqs = np.vstack((freqs, freq))
    
    pol,subj = overallTweetSentiment(tweets, date, movie)
    sent = np.array([pol,subj])
    print sent
    #ratio,pos_freq,neg_freq = tweetsSentiment(tweets, date, movie)
    #ratio = np.array([ratio])
    #pos_freq = np.array([pos_freq])
    #neg_freq = np.array([neg_freq])
    
    sentiments = np.vstack((sentiments, sent))
    
    #freqs = np.vstack((freqs, freq))
    #pos_freqs = np.vstack((pos_freqs, pos_freq))
    #neg_freqs = np.vstack((neg_freqs, neg_freq))
    #ratios = np.vstack((ratios, ratio))
    
print movie_key
print freqs
#print pos_freqs
#print neg_freqs
#print ratios


out = open('tweet_vectors/movies', 'w')
json.dump(movie_key, out)
out.close()

np.savetxt('tweet_vectors/sentiments.txt', sentiments)
#np.savetxt('tweet_vectors/freqs', freqs)
#np.savetxt('tweet_vectors/pos_freqs', pos_freqs)
#np.savetxt('tweet_vectors/neg_freqs', neg_freqs)
#np.savetxt('tweet_vectors/ratios', ratios)

  
#for movie in allMovies[0:50]:

    #open relevant file
#    f = open(tweetsFile)
##    text = f.read()
 #   tweets = json.loads(text)
  #  print movie
   # print tweetsToFreq(tweets, datetime(2014,12,5), movie[0]) #make middle movie[1]


#print tweetsToFreq(tF,rT)

#np.savetxt("freqMovies.data", freq_vect, delimiter=",")
