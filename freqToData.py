import json
import numpy as np

def getMovieList():
	movies = open("movies.txt", "r")
	movieAndDateList = [movie.strip('\n').strip('\r') for movie in movies]
	movieList = [movie.split("|")[1] for movie in movieAndDateList]
	return movieList


def getTwelveData(freqname, revname):
	freq_data = open(freqname)
	freq = json.load(freq_data)
	rev_data = open(revname)
	revenue = json.load(rev_data)
	data = np.zeros((158, 13))
	movies = getMovieList()
	for i in xrange(len(movies)):
		movie = movies[i]
		freqs = [int(frequency) for frequency in freq[movie]]
		rev = int(revenue[movie])
		#print movie, len(freq[movie]), rev
		freqs.append(rev)
		data[i] = np.array(freqs)
	return data.astype(int)


def getData(freqname, revname):
	freq_data = open(freqname)
	freq = json.load(freq_data)
	rev_data = open(revname)
	revenue = json.load(rev_data)
	# movie_list = open("tweet_vectors\movies.txt")
	# movie_list = json.load(movie_list)
	# sent_data = open("sentiments.txt")
	# sentimentsList = [sentiment.strip('\n').strip('\r') for sentiment in sent_data]
	# sentList = [float(sentiment.split("|")[0]) for sentiment in sentimentsList]
	# objectList = [float(sent.split("|")[1]) for sent in sentimentsList]
	# print sentList
	# print objectList

	sentiments = np.loadtxt("sentiments.txt")
	data = np.zeros((158, 181))
	movies = getMovieList()
	for i in xrange(len(movies)):
		movie = movies[i]
		freqs = [int(frequency) for frequency in freq[movie]]
		rev = int(revenue[movie])
		#print movie, len(freq[movie]), rev
		freqs.append(rev)
		data[i] = np.array(freqs)
	return data.astype(int)

def getWeekData(freqname, revname):
	freq_data = open(freqname)
	freq = json.load(freq_data)
	rev_data = open(revname)
	revenue = json.load(rev_data)
	data = np.zeros((158, 13))
	movies = getMovieList()
	print freq
	for i in xrange(len(movies)):
		movie = movies[i]
		freqs = [int(frequency) for frequency in freq[movie]]
		#print len(freqs)
		rev = int(revenue[movie])
		freqs = freqs[:12]
		print movie, len(freq[movie]), rev
		freqs.append(rev)
		data[i] = np.array(freqs)
	return data.astype(int)