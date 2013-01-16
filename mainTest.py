#for test

import re
import types 
import time
import os
import sys
import urllib
import urllib2
import cookielib
import base64
import hashlib
import json
import pymongo
#from bs4 import BeautifulSoup
from optparse import OptionParser

import Pyweibo
#import mongoDBUtil


'''
a = ''
b = 'aa'
if a:
	print 'a'
elif b:
	print 'aa is not  empty'

'''

#str = 'page=(12), page=(15), page=(1) page=5uu'
#str2 = "$CONFIG['oid'] = '1220349643'"


#list = (re.findall (r'(?<=\()\d{1,}(?=\))' , str))
#print int(list[0])


#c = int(re.findall(r'[\d\.]+', str2)[0])
#print c + 1
#s = s + 1

#print type(c)

#ste1 = all_the_text.partition('$CONFIG[\'oid\'] = \'')[2]  
#ste2 = ste1.partition('\'')[0]
#num = int(re.findall(r'[\d\.]+', ste2)[0])

#print (str2.partition('\'oid\''))[0]
#print time.time()
#file_object = open('profileHtml')
#Data = file_object.read();

#soup = BeautifulSoup(Data)
#s = soup.find(attrs={'class' : "pf_intro bsp"})
#print s
#a = s.find("span", {'class' : "S_txt2"})
#name  = a.get('title') 
#print name


#sStr1 = 'asd'
#sStr2 = 'asdc'
#sStr3 = 'ccc'
#print ''.join([sStr1, sStr2, sStr3])


pyweibo = Pyweibo.Pyweibo() 
pyweibo.analyseFollowsFansInfo(1220349643)
#mongoDB = mongoDBUtil.mongoDBUtil()
#pyweibo.login('xxxxxx', '*******')
#pyweibo.setOid(2145291155)
#profile = pyweibo.getPersonalProfile()
#print profile
#pyweibo.getPersonalFeeds(2145291155, './data2')
#pyweibo.generateRepostMap('http://weibo.com/1763362173/zbGgn0e8U', max=10000)

#ting 2108634957 jia 2218904682
#pyweibo.getPersonalProfile('2108634957')
'''
test_collection = 'repost'
mytest = 'testbase'
conn = pymongo.Connection('localhost',27017)
db = conn.mytest
collection = db.test_collection
post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"], "date": '2012'}
collection.insert(post)
print collection.count()
for item in collection.find():
    print item
'''
#a = [{'uid':'123', 'nickname': 'heyflypig'}, {'uid':'456', 'nickname': 'ding'}]
#mongoDB.saveData(a, 'repost', 'test')
