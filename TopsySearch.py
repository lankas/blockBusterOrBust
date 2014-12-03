# scrape tweets from topsy.com
 
import sys, urllib, urllib2, json, random
from scrapeBoxOfficeMojo import getMovieList

 
def search(query, page=1, perpage=100):
  data = {'q': query, 'type': 'tweet', 'page': page, 'perpage': perpage, 'window': 'a', 'sort_method': "-date", 'apikey': '09C43A9B270A470B8EB8F2946A9369F3', "mintime":1414792811, "maxtime":1417125633}
  url = "http://otter.topsy.com/search.js?" + urllib.urlencode(data)
  data = urllib2.urlopen(url)
  o = json.loads(data.read())
  res = o['response']
  return res

def string_to_date(dateString):


def get_all_tweets(movie):
  all_tweets = []
  for page in range(1,11):
    res = search(movie, page=page)
    tweets = [{"text":tweet['title'], "date":tweet['firstpost_date']} for tweet in res['list']]
    all_tweets.extend(tweets)
  return all_tweets

def dump_to_file(obj, outfile):
  o = open(outfile, "w")
  o.write(json.dumps(obj))
  o.close()

 
if __name__ == "__main__":
  movieList = getMovieList()
  all_movie_data = []
  for movie in movieList:
    print movie
    tweets = get_all_tweets(movie)
    all_movie_data.extend([{movie:tweet} for tweet in tweets])

  dump_to_file(all_movie_data, "movie_tweet_data")