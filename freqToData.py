import json
import numpy as np

def getMovieList():
	movies = open("movies.txt", "r")
	movieAndDateList = [movie.strip('\n').strip('\r') for movie in movies]
	movieList = [movie.split("|")[1] for movie in movieAndDateList]
	return movieList


def getData(freqname):
	freq_data = open(freqname)
	freq = json.load(freq_data)
	rev_data = open('revenue.txt')
	revenue = json.load(rev_data)
	data = np.zeros((160, 181))
	movies = getMovieList()
	for i in xrange(len(movies)):
		movie = movies[i]
		freqs = [int(frequency) for frequency in freq[movie]]
		rev = int(revenue[movie])
		#print movie, len(freq[movie]), rev
		freqs.append(rev)
		data[i] = np.array(freqs)
	return data.astype(int)