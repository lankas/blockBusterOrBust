
import sys, urllib, urllib2, json, random, locale
import numpy as np
from datetime import datetime, timedelta

def getMovieList():
  movies = open("movies.txt", "r")
  movieAndDateList = [movie.strip('\n').strip('\r') for movie in movies]
  movieList = [movie.split("|")[1] for movie in movieAndDateList]
  return movieList

def moviedate(date):
  locale.setlocale(locale.LC_ALL, '')
  return datetime.strptime(date,"%x")


def searchhistcounts(query, period):
  data = {'q': query, 'type': 'tweet', 'slice': 86400*14,'period': period, 'apikey': '09C43A9B270A470B8EB8F2946A9369F3'}
  url = "http://otter.topsy.com/searchhistogram.js?" + urllib.urlencode(data)
  data = urllib2.urlopen(url)
  o = json.loads(data.read())
  res = o['response']
  return res


def getfreqWeek(movie, releaseDate):
  #print movie
  start_date = releaseDate - timedelta(days=7)
  diff = datetime.today() - start_date
  days = diff.days + 180
  weeks = days / 14
  num_weeks = diff.days / 14
  counts = searchhistcounts(movie, weeks)['histogram'][num_weeks:]
  print len(counts)
  return counts

def getfreq(movie, releaseDate):
  start_date = releaseDate - timedelta(days=7)
  diff = datetime.today() - start_date
  days = diff.days + 12
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
    print movie
    movie_freq[movie] = getfreqWeek(movie, date)
  return movie_freq


def dump_to_file(obj, outfile):
  o = open(outfile, "w")
  o.write(json.dumps(obj))
  o.close()


def getFrequencies():
  frequencies = get_all_counts("movies.txt")
  dump_to_file(frequencies, "freqTwoWeekInterval.txt")
