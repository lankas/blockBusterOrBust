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

	sentiments = np.loadtxt("sentiments.txt")
	data = np.zeros((158, 12))
	revs = np.zeros((158,))
	movies = getMovieList()
	for i in xrange(len(movies)):
		movie = movies[i]
		freqs = [int(frequency) for frequency in freq[movie]]
		rev = int(revenue[movie])
		#print movie, len(freq[movie]), rev
		#freqs.append(rev)
		revs[i] = rev
		data[i] = np.array(freqs)
	return data, revs


def getData(freqname, revname):
	freq_data = open(freqname)
	freq = json.load(freq_data)
	rev_data = open(revname)
	revenue = json.load(rev_data)

	sentiments = np.loadtxt("sentiments.txt")
	#print sentiments
	data = np.zeros((158, 180))
	revs = np.zeros((158,))
	movies = getMovieList()
	for i in xrange(len(movies)):
		movie = movies[i]
		freqs = [int(frequency) for frequency in freq[movie]]
		rev = int(revenue[movie])
		#print movie, len(freq[movie]), rev
		#freqs.append(rev)
		revs[i] = rev
		data[i] = np.array(freqs)
	#print revs
	# print len(revs), len(data), len(sentiments)
	# data = np.hstack((data, sentiments, revs))
	# print data
	return data, revs
	#return data.astype(int)

def getWeekData(freqname, revname):
	freq_data = open(freqname)
	freq = json.load(freq_data)
	rev_data = open(revname)
	revenue = json.load(rev_data)

	sentiments = np.loadtxt("sentiments.txt")
	data = np.zeros((158, 12))
	revs = np.zeros((158,))
	movies = getMovieList()
	#sprint freq
	for i in xrange(len(movies)):
		movie = movies[i]
		freqs = [int(frequency) for frequency in freq[movie]]
		#print len(freqs)
		rev = int(revenue[movie])
		freqs = freqs[:12]
		#print movie, len(freq[movie]), rev
		#freqs.append(rev)
		revs[i] = rev
		data[i] = np.array(freqs)
	#data = np.hstack(data, )
	#return data.astype(int)
	return data, revs