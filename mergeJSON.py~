import json

f1 = open('tweet_dir1.txt')
f2 = open('tweet_dir2.txt')
text1 = f1.read()
text2 = f2.read()
content1 = json.loads(text1)
content2 = json.loads(text2)

content = {}
content.update(content1)
content.update(content2)

outfile = open('tweetdir.txt','w')
json.dump(content, outfile)

