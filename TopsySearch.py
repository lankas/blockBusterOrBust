# scrape tweets from topsy.com
 
import sys, urllib, urllib2, json, random, locale, re
from scrapeBoxOfficeMojo import getMovieList
from datetime import datetime
from dateToTimestamp import get_older_date

 
def search(query, page=1, perpage=100, maxtime=None, mintime=None):
  if (maxtime is not None) and (mintime is not None):
    data = {'q': query, 'type': 'tweet', 'page': page, 'perpage': perpage, 'sort_method': "-date", 'apikey': '09C43A9B270A470B8EB8F2946A9369F3', "maxtime":maxtime.strftime("%s"), "mintime":mintime.strftime("%s")}
  elif (maxtime is None):
    data = {'q': query, 'type': 'tweet', 'page': page, 'perpage': perpage, 'sort_method': "-date", 'apikey': '09C43A9B270A470B8EB8F2946A9369F3', "maxtime":maxtime.strftime("%s")}
  else:
    data = {'q': query, 'type': 'tweet', 'page': page, 'perpage': perpage, 'sort_method': "-date", 'apikey': '09C43A9B270A470B8EB8F2946A9369F3'}
  url = "http://otter.topsy.com/search.js?" + urllib.urlencode(data)
  data = urllib2.urlopen(url)
  o = json.loads(data.read())
  res = o['response']
  return res

def get_movies_and_dates(infile):
  movieList = getMovieList()
  f = open(infile, "r")
  movieAndDateList = [movie.strip('\n') for movie in f]
  dateList = [movie.split("|")[0] for movie in movieAndDateList]
  locale.setlocale(locale.LC_ALL, '')
  dateList = [datetime.strptime(date,"%x") for date in dateList]
  return zip(movieList, dateList);

def get_all_tweets(movie, startingDate, endingDate):
  all_tweets = []
  for page in range(1,11):
    res = search(movie, page=page, maxtime=startingDate, mintime=endingDate)
    tweets = [{"text":tweet['title'], "date":tweet['firstpost_date']} for tweet in res['list']]
    all_tweets.extend(tweets)
  return all_tweets

def dump_to_file(obj, outfile):
  o = open(outfile, "w")
  o.write(json.dumps(obj))
  o.close()
 
if __name__ == "__main__":

  try: infile = str(sys.argv[1])
  except: print "python " + sys.argv[0] + " <query keyword>"

  try: outfile = str(sys.argv[2])
  except: print "python " + sys.argv[0] + " <query keyword>"

  moviesAndDates = get_movies_and_dates(infile)
  movie_files_data = dict()
  for movie,date in moviesAndDates:
    print "\n", movie

    starting_date = get_older_date(date, 1)
    tweets = get_all_tweets(movie, starting_date, None)

    print len(tweets)
    tweetfile = "movie_tweets/"+re.sub(r'\W+', '_', movie) + "_tweets.txt"
    print tweetfile
    dump_to_file(tweets, tweetfile)

    movie_files_data[movie] = tweetfile

  dump_to_file(movie_files_data, outfile)


  # Week before the movie comes out to 6 months before that.