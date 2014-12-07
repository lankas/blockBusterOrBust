import datetime

def get_older_date(date, days):
	'''Get a datetime object older than the current
	date by the number of days specified'''
	td = datetime.timedelta(days=days)
	return date - td

def get_newer_date(date, days):
	'''Get a datetime object older than the current
	date by the number of days specified'''
	td = datetime.timedelta(days=days)
	return date + td