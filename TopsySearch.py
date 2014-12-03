# scrape tweets from topsy.com
 
import sys, urllib, urllib2, json, random
 
def search(query, page=1, perpage=100):
  data = {'q': query, 'type': 'tweet', 'page': page, 'perpage': perpage, 'window': 'a', 'sort_method': "-date", 'apikey': '09C43A9B270A470B8EB8F2946A9369F3', "mintime":1414792811, "maxtime":1417125633}
  url = "http://otter.topsy.com/search.js?" + urllib.urlencode(data)
  data = urllib2.urlopen(url)
  o = json.loads(data.read())
  res = o['response']
  return res


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
  try: tanya = str(sys.argv[1])
  except: print "python " + sys.argv[0] + " <query keyword>"
  print "> Querying for", tanya
  res = search(tanya)
  print "> Total fetched:", str(res['total'])
  print "> Here is the preview:"
  for i in res['list'][:1000]:
    print "-->", i['firstpost_date'], i['title']