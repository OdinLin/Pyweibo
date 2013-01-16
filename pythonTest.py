# -*- coding: utf-8 -*-

import re
#from pytagcloud import create_tag_image, make_tags
#from pytagcloud.lang.counter import get_tag_counts
#import jieba
#import jieba.analyse
#import Pyweibo
import webbrowser
import mongoDBUtil



a = 'action-data="allowForward=1&amp;rootmid=3522439063677390&amp;rootname=8090情侣手册&amp;rootuid=1807128011&amp;rooturl=http://weibo.com/1807128011/z9pK2fqEK&amp;url=http://weibo.com/3024618893/z9Bbg7nxB&amp;mid=3522878781758791&amp;name=獨善其身TT&amp;uid=3024618893&amp;domain=1807128011&amp;pid=6bb695cbjw1dzqzne13umj" action-type="feed_list_forward" href="javascript:void(0);" onclick="return false;'
#print (re.findall(r'(?<=rootmid)\d{1,}(?=\&amp))', a))
#print re.findall (r'rootmid=+(\d+)&amp' , a)[0]
#print re.findall (r'rooturl=+(.+?)&amp' , a)
#print re.findall (r'rootname=+(.+?)&amp' , a)[0]

weibo = {}
bb = []
rootmid = re.findall(r'rootmid=+(\d+)&amp', a)[0] #equal mid may not need
rootname = re.findall(r'rootname=+(.+?)&amp', a)[0]
rootuid = re.findall(r'rootuid=+(\d+)+&amp', a)[0]
rooturl = re.findall(r'rooturl=+(.+?)&amp', a)[0] #equal URL may not need

reposturl = re.findall (r';url=+(.+?)&amp' , a)[0]
repostmid = re.findall(r';mid=+(\d+)+&amp', a)[0]
repostname = re.findall(r';name=+(.+?)&amp', a)[0]
repostuid = re.findall(r';uid=+(\d+)&amp', a)[0]

weibo[1] = "%s\t%s\t%s\t%s\t\n" % (rootmid, rootname, rootuid, rooturl)
weibo[2] = "%s\t%s\t%s\t%s\t\n" % (repostmid, repostname, repostuid, reposturl)
#bb.append(weibo[1])
#print bb

#cc = '"http://tp3.sinaimg.cn/2789672350/50/5637245856/1" usercard="id=2789672350" width="30" height="30" alt="qpzmwoxn6312" /></a></dt><dd><a href="/2789672350" title="qpzmwoxn6312" nick-name="qpzmwoxn6312" '
dd = '/<a href="/n/%E4%BA%92%E8%81%94%E7%BD%91%E4%BA%BA%E5%A3%AB-%E6%9D%8E%E6%BE%8D%E6%99%9F" usercard="name=互联网人士-李澍晟" >@互联网人士-李澍晟</a>'
ee = '<em> //<a href=" //<a href=" //<a href=" '
#print cc
#nick-name="qpzmwoxn6312"
#rootname = re.findall(r'nick-name=\"+(.+?)\"', cc)[0]
#rootname = len(re.findall(r'href=', ee))
#print rootname

#content1 = open('chi.txt','rb').read()


#pyweibo = Pyweibo.Pyweibo()
#pyweibo.login('xxxxxxxxxxxxx', '***********')
#pyweibo.getPersonalFeeds(2218904682)
#content1 = open('feedsContent','rb').read()
#tags = pyweibo.getKeyword(content1, 5)
#pyweibo.generateTagCloudFile(content1, 10)

#print ",".join(tags)
#print tags
#min, max = tags[0][0], tags[5-1][0]
#print min
#print max

#outputs = run("a <- 3; print(a + 5)")

#webbrowser.open("file://" + 'D:/GitHub/Mining-the-Soc ial-Web/web_code/wp_cumulus/tagcloud_template.html')

#a = [{'1':'a'}, {'2':'q'}, {'3':'aw'}, {'4':'e'}, {'5':'ar'}, {'6':'at'}, {'7':'ay'}]
#b = [{'interestTag':['appale', 'orange']}, {'interestTag':['banaba', 'orange']}]

#mongo = mongoDBUtil.mongoDBUtil()
#con = mongo.saveData(b, 'weibo', 'test')
#mongo.analyseCollection2(con, topN=1)

from pymongo import Connection
from bson.code import Code


#'''
#Open a connection to MongoDb (localhost)
connection =  Connection()
db = connection.test

map = Code("function () {"
            "var words = this.text.match(/\w+/g)"
            
            "if(words == null){"
            "  return;"
            "}"
            "for (var i = 0; i < words.length; i++){"
            "emit(this.freq, {count:1});"
            "}")

reduce = Code("function (key, values) {"
               "  var total = 0;"
               "  for (var i = 0; i < values.length; i++) {"
               "    total += values[i].count;"
               "  }"
               "  return {count:total};"
               "}")

#Remove any existing data
db.texts.remove()

#Insert the data 
lines = open('2329.txt').readlines()
[db.texts.insert({'text': line}) for line in lines]

#Load map and reduce functions
#map = Code(open('wordMap.js','r').read())
#reduce = Code(open('wordReduce.js','r').read())


#Run the map-reduce query
results = db.texts.map_reduce(map, reduce, "collection_name")

#Print the results
for result in results.find():
    print result['_id'] , result['value']['count']