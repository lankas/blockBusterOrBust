import requests
from bs4 import BeautifulSoup

def getMovieList():
	movies = open("movies.txt", "r")
	movieList = [movie.strip('\n') for movie in movies]
	return movieList

def getMovieRevenues():
	movieRevenue = {}
	movies = getMovieList()
	for movie in movies:
		revenue = scrape(movie)
		movieRevenue[movie] = revenue
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
	print amount
	amt = int(amount)
	return amt

def scrape(search):
	return scrapeUrl(createUrl(search))