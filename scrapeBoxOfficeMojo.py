import json
import requests
from bs4 import BeautifulSoup

def toJSON(filename):
	with open(filename, 'w') as outfile:
		json.dump(classify(), outfile)
		#json.dump(getMovieRevenues(), outfile)

def classify():
	movieRevenue = getMovieRevenues()
	values = movieRevenue.values()
	values.sort()
	l = len(values) / 20

	#first = values[17*l]
	first = 20000000
	print first
	#second = values[19*l]
	second = 60000000
	print second
	#l = len(values) / 2
	#first = values[l]

	for key in movieRevenue.keys():
		v = movieRevenue[key]
		if (v < first):
			#print key
			c = 0
		elif (v < second):
			print key
			c = 1
		else:
			#print key
			c = 2
		#else:
		#	c = 1
		movieRevenue[key] = c
	#print movieRevenue
	return movieRevenue


def getMovieList():
	movies = open("moviesBoxOffice.txt", "r")
	movieList = [movie.strip('\n').strip('\r') for movie in movies]
	#movieList = [movie.split("|")[1] for movie in movieAndDateList]
	return movieList

def getMovieRevenues():
	movieRevenue = {}
	movies = getMovieList()
	for movie in movies:
		revenue = scrape(movie)
		movieRevenue[movie] = revenue
	movieRevenue['The Nut Job'] = 19423000
	movieRevenue['Frank'] = 16056
	movieRevenue['Ride Along'] = 41516170
	movieRevenue['The Lego Movie'] = 69050279
	movieRevenue['Divergent'] = 54607747
	movieRevenue['Brick Mansions'] = 9516855
	movieRevenue['Godzilla'] = 93188384
	movieRevenue['Holiday'] = 394797
	movieRevenue['Guardians of the Galaxy'] = 94320883
	movieRevenue['Teenage Mutant Ninja Turtles'] = 65575105
	movieRevenue['The Maze Runner'] = 32512804
	movieRevenue['Left Behind'] = 6300147
	movieRevenue['Fury'] = 23702421
	return movieRevenue

def createUrl(search):
	delimiter = '%20'
	search = search.replace(" ", delimiter)
	url = 'http://boxofficemojo.com/search/?q=' + search
	return url

def scrapeUrl(url):
	print url
	try:
		req = requests.get(url)
	except:
		return -1
	soup = BeautifulSoup(req.text)

	container = soup.find(id='container')
	main = container.find(id='main')
	body = main.find(id='body')
	table = [i for i in body.children][5] #is this consistent?
	td = table.td
	table = [i for i in td.children][7] #is this consistent?
	tr = [i for i in table.children][3] #is this consistent?
	td = [i for i in tr.children][9] #is this consistent?
	amount = td.text
	amount = amount[1:].replace(",","")
	#print amount
	amt = int(amount)
	return amt

def scrape(search):
	return scrapeUrl(createUrl(search))