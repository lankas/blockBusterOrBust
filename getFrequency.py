
import sys, urllib, urllib2, json, random, locale
import numpy as np
from scrapeBoxOfficeMojo import getMovieList
from datetime import datetime, timedelta


def moviedate(date):
  locale.setlocale(locale.LC_ALL, '')
  return datetime.strptime(date,"%x")


def searchhistcounts(query, period):
  data = {'q': query, 'type': 'tweet', 'period': period, 'apikey': '09C43A9B270A470B8EB8F2946A9369F3'}
  url = "http://otter.topsy.com/searchhistogram.js?" + urllib.urlencode(data)
  data = urllib2.urlopen(url)
  o = json.loads(data.read())
  res = o['response']
  return res


def getfreq(movie, releaseDate):
  start_date = releaseDate - timedelta(days=14)
  diff = datetime.today() - start_date
  days = diff.days + 180
  #return searchhistcounts(movie, days)['histogram'][diff.days:]
  counts = searchhistcounts(movie, days)['histogram'][diff.days:]
  return counts
  

def get_movies_and_dates(infile):
  movieList = getMovieList()
  f = open(infile, "r")
  movieAndDateList = [movie.strip('\n') for movie in f]
  dateList = [movie.split("|")[0] for movie in movieAndDateList]
  locale.setlocale(locale.LC_ALL, '')
  dateList = [datetime.strptime(date,"%x") for date in dateList]
  return zip(movieList, dateList);


def get_all_counts(infile):
  moviesAndDates = get_movies_and_dates(infile)
  movie_freq = {}
  for movie,date in moviesAndDates:
    movie_freq[movie] = getfreq(movie, date)
  return movie_freq


def dump_to_file(obj, outfile):
  o = open(outfile, "w")
  o.write(json.dumps(obj))
  o.close()


def getFrequencies():
  frequencies = get_all_counts("movies.txt")
  dump_to_file(frequencies, "freqTwoWeeks.txt")
