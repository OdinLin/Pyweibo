#! /usr/bin/env python
# -*- coding: utf-8 -*-
try:
	import urllib
	import urllib2
	import sys
	import time
	import json
	import cookielib
	import base64	
	import hashlib
	import os
	import string
	import re
	import jieba 
	import webbrowser
	from bs4 import BeautifulSoup
	import networkx as nx
	from ConfigParser import SafeConfigParser

except ImportError:
	print >> sys.stderr, """\

There was a problem importing one of the Python modules required to run yum.
The error leading to this problem was:

%s

Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the current version of Python,
which is:

%s

""" % (sys.exc_value, sys.version)
	sys.exit(1)


reload(sys)
sys.setdefaultencoding('utf-8')

class weiboUtil:
	#login stuff
	cj = cookielib.LWPCookieJar()
	cookie_support = urllib2.HTTPCookieProcessor(cj)
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener)
	postdata = {
		'entry': 'weibo',
		'gateway': '1',
		'from': '',
		'savestate': '7',
		'userticket': '1',
		'ssosimplelogin': '1',
		'vsnf': '1',
		'vsnval': '',
		'su': '',
		'service': 'miniblog',
		'servertime': '',
		'nonce': '',
		'pwencode': 'wsse',
		'sp': '',
		'encoding': 'UTF-8',
		'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
		'returntype': 'META'
	}

	#profile feed stuff
	charset = 'utf8'
	repost = {}

	

	def __init__(self):
		print 'login'

		#config stuff
		parser = SafeConfigParser()
		parser.read('pyweibo.cfg')
		username = parser.get('login', 'username')
		pw = parser.get('login', 'password')
		
		print parser.get('login', 'username')

		self.login(username, pw)

	#login fun
	def get_servertime(self, name):
		url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=' + name +'&client=ssologin.js(v1.3.18)'
		data = urllib2.urlopen(url).read()
		p = re.compile('\((.*)\)')
		try:
			json_data = p.search(data).group(1)
			data = json.loads(json_data)
			servertime = str(data['servertime'])
			nonce = data['nonce']
			return servertime, nonce
		except:
			print 'Get severtime error!'
			return None

	def get_pwd(self, pwd, servertime, nonce):
		pwd1 = hashlib.sha1(pwd).hexdigest()
		pwd2 = hashlib.sha1(pwd1).hexdigest()
		pwd3_ = pwd2 + servertime + nonce
		pwd3 = hashlib.sha1(pwd3_).hexdigest()
		return pwd3

	def get_user(self, username):
		username_ = urllib.quote(username)
		username = base64.encodestring(username_)[:-1]
		return username

	def login(self,username,pwd):
		url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
		name = self.get_user(username)
		try:
			servertime, nonce = self.get_servertime(name)
		except:
			print 'get servertime error!'
			return
		self.postdata['servertime'] = servertime
		self.postdata['nonce'] = nonce
		self.postdata['su'] = self.get_user(username)
		self.postdata['sp'] = self.get_pwd(pwd, servertime, nonce)
		self.postdata = urllib.urlencode(self.postdata)
		headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}
		req  = urllib2.Request(
			url = url,
			data = self.postdata,
			headers = headers
		)
		result = urllib2.urlopen(req)
		text = result.read()
		p = re.compile('location\.replace\(\'(.*?)\'\)')
		try:
			login_url = p.search(text).group(1)
			urllib2.urlopen(login_url)
			print "Login success!"
		except:
			print 'Login error!'

	#profile stuff		
	def getPersonalProfile(self, uid):
		uid = int(uid)
		if uid == 0:
			print 'need uid'
			return
		url = 'http://weibo.com/' + str(uid) + '/profile?page='
		print 'url is ' + url	
		profile = {}
		page = urllib2.urlopen(url).read()
		self.writefile('profilePage', page)	

		#uid 
		profile['uid'] = str(uid)

		#get nickName
		nickName = page.partition('$CONFIG[\'nick\'] = \'')[2].decode('gb2312')  
		profile['nickName'] = nickName.partition('\'')[0].decode("utf-8")
		#try this
		#profile['nickName'] = nickName.partition('\'')[0]
		#print 'nickName is ' + profile['nickName']  #it work well
		#another version use re,should test the speed to decide
		#profile['nickName'] = re.findall(r'$CONFIG[\'nick\'] = \'+(.+?)\';', page)[0]

		#get profileHtml
		content = page.partition('{\"pid\":\"pl_profile_hisInfo\"')
		jsonData = content[2].partition(')</script>')[0]
		jsonData = content[1] + jsonData
		#print jsonData
		htmlData = json.loads(jsonData)['html']
		self.writefile('profileHtml', htmlData)
		soup = BeautifulSoup(htmlData)

		#get domainName
		#means personal domainname like: weibo.com/heflypig
		#heyflypig is the domainname
		domainName = soup.find(attrs={'class' : "pf_lin S_link1"})
		domainName = domainName.get('href')	
		domainName = (re.findall (r'\/+(.+)\?from' , str(domainName)))[0]
		profile['domainName'] = domainName
		print 'domainName is ' + profile['domainName']

		#get vip level
		vipTag = 'http://vip.weibo.com/personal?from=main'
		if vipTag in htmlData:
			profile['vip'] = True
		else:
			profile['vip'] = False

		print 'vip ? ' + str(profile['vip'])
		leveldata = htmlData.partition('W_level_num') 
		leveldata = leveldata[2].partition('\"')[0]
		profile['level'] = int(re.findall(r'[\d\.]+', leveldata)[0]) #magic thing happen!
		print 'level is ' + str(profile['level'])

		#get sex
		sex = htmlData.partition('W_ico12 ')[2]  
		profile['sex'] = sex.partition('\"')[0]
		print 'sex is ' + profile['sex']

		#get intro
		content = soup.find(attrs={'class' : "pf_intro bsp"})
		content = content.find("span", {'class' : "S_txt2"})
		profile['introduction']  = content.get('title')	
		#print 'intro is ' + profile['introduction']  #it work well

		#get Location
		locatTag = '<span class="W_vline S_line1_c">|</span><em class="S_txt2"><a href='
		if locatTag in htmlData:
			locatdata = htmlData.partition(locatTag)[2]
			locatdata = locatdata.partition('<')[0]
			profile['location'] = locatdata.partition('>')[2].decode("utf-8")
			#print 'location is ' + profile['location'] #it work well

		#get profileHtml
		content = page.partition('{\"pid\":\"pl_profile_photo\"')  
		jsonData = content[2].partition(')</script>')[0]
		jsonData = content[1] + jsonData
		#print jsonData
		htmlData = json.loads(jsonData)['html']
		self.writefile('profileHtml2', htmlData)

		#follow
		follows = htmlData.partition('"follow"')[2]
		follows = follows.partition('<')[0]
		profile['follows'] = follows.partition('>')[2]
		print 'follows is ' + profile['follows']

		#fans
		fans = htmlData.partition('"fans"')[2]
		fans = fans.partition('<')[0]
		profile['fans'] = fans.partition('>')[2]
		print 'fans is ' + profile['fans']

		#feeds
		feeds = htmlData.partition('"weibo"')[2]
		feeds = feeds.partition('<')[0]
		profile['feeds'] = feeds.partition('>')[2]
		print 'feeds is ' + profile['feeds']
		
		#get interestTag
		interestTag = []
		content = page.partition('{\"pid\":\"pl_profile_extraInfo\"')  
		jsonData = content[2].partition(')</script>')[0]
		jsonData = content[1] + jsonData
		#print jsonData
		interestData = json.loads(jsonData)['html']
		self.writefile('interest', interestData)
		soup = BeautifulSoup(interestData)
		if soup.findAll('p'):
			interests = soup.findAll('p')[1]
			for interest in interests.findAll("a",{'class' : "S_link1"}):
				interestTag.append(self.clean_content(str(interest)))
				
			profile['interestTag'] = interestTag
		
		#todo:get company
		#get school
		
		return profile

	#feed stuff	
	ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

	def base62_encode(self, num, alphabet=ALPHABET):
		if (num == 0):
			return alphabet[0]
		arr = []
		base = len(alphabet)
		while num:
			rem = num % base
			num = num // base
			arr.append(alphabet[rem])
		arr.reverse()
		return ''.join(arr)

	def base62_decode(self, string, alphabet=ALPHABET):
		base = len(alphabet)
		strlen = len(string)
		num = 0

		idx = 0
		for char in string:
			power = (strlen - (idx + 1))
			num += alphabet.index(char) * (base ** power)
			idx += 1

		return num    

	def murl_to_mid(self, murl):
		mid = (str(self.base62_decode(str(murl[::-1][8:12][::-1])))+str(self.base62_decode(str(murl[::-1][4:8][::-1])))+str(self.base62_decode(str(murl[::-1][0:4][::-1]))))
		return mid    

	def getPersonalFeeds(self, uid, output_file='./out/feedsData'):
		if os.path.exists(output_file):
			last_mid = int(self.murl_to_mid(self.last_murl(output_file)))
		else:
			last_mid = 0

		page     = 1
		uid      = int(uid)
		weibo    = {}
		finished = False
		saved_count = 0 # for top
		Content = {}
		while not finished:
			urls={}
			urls[0]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=50&page=%d&uid=%d' % (page,uid)
			urls[1]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=15&page=%d&uid=%d&pre_page=%d&pagebar=0' % (page,uid,page)
			urls[2]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=15&page=%d&uid=%d&pre_page=%d&pagebar=1' % (page,uid,page)
			print "now page : %d" % page
			page = page + 1
			for p in urls:

				try:
					d = urllib2.urlopen(urls[p]).read()
					n = json.loads(d)
					#self.writefile('jsondata', n)
				except:
					print "Get data error,remove your cookie data and try again"
					finished = True
					break
				soup = BeautifulSoup(n['data'])
				#self.writefile('soup', soup)
				#print soup.prettify()
				posts = soup.findAll(attrs={'action-type' : "feed_list_item"})
				if len(posts)>0:
					for post in posts:
						mid  = post.get('mid')
						if mid:
							mid  = int(mid)
							forward = post.get('isforward')
							#print post.prettify()
							if forward:
								origin_nick     = self.clean_content(str(post.find(attrs={'node-type' : "feed_list_originNick"})))
								forward_content = "[%s : %s]" % (origin_nick,self.clean_content(str(post.find(attrs={'node-type' : "feed_list_reason"}))))
							else:
								forward_content = ""
							wb_from = post.find("a",{'class' : "S_link2 WB_time"})
							murl    = str(re.sub("/.*/","",str(wb_from.get('href'))))
							ptime   = str(wb_from.get('title'))
							content = self.clean_content(str(post.find(attrs={'node-type' : "feed_list_content"})))
							#device  = self.clean_content(str(post.find("a",{'class' : "S_link2" ,"rel" : "nofollow"}))).decode("utf-8")
							#print 'device is ' + device  #work well
							like = self.clean_content(str(post.find(attrs={'action-type' : "feed_list_like"})))
							like = (re.findall (r'(?<=\()\d{1,}(?=\))' , like))
							#print 'like is ' + (like and like[0] or 'empty')                            

							repost = self.clean_content(str(post.find(attrs={'action-type' : "feed_list_forward"})))
							repost = (re.findall (r'(?<=\()\d{1,}(?=\))' , repost))
							#print 'repost is ' + (repost and repost[0] or 'empty')

							favorite = self.clean_content(str(post.find(attrs={'action-type' : "feed_list_favorite"})))
							favorite = (re.findall (r'(?<=\()\d{1,}(?=\))' , favorite))
							#print 'favorite is ' + (favorite and favorite[0] or 'empty')	

							comment = self.clean_content(str(post.find(attrs={'action-type' : "feed_list_comment"})))
							comment = (re.findall (r'(?<=\()\d{1,}(?=\))' , comment))
							#print 'comment is ' + (comment and comment[0] or 'empty')							

							if mid > last_mid:
								weibo[mid] = "%s\t%s\t%s\t%s\t%s\t%s\t%s %s\n" % (murl, ptime, content, like, repost, favorite, comment, forward_content)
								Content[mid] = "%s\t%s\t\n" % (content, forward_content)
							elif saved_count > 2:
								finished = True
							else:
								saved_count = saved_count + 1

				else:
					finished = True

					time.sleep(0.5)

					#finished = True

		f = open(output_file,'a+')
		for i in sorted(weibo.items(), key=lambda e:e[0], reverse=False):

			f.write(i[1])

		f.close()

		f = open('./out/feedsContent','a+')
		for i in sorted(Content.items(), key=lambda e:e[0], reverse=False):

			f.write(i[1])

		f.close()	

	def last_murl(self, output_file):
		with open(output_file, 'r') as f:
			f.seek (0, 2) # Seek @ EOF
			fsize = f.tell() # Get Size
			f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
			lines = f.readlines() # Read to end
		line = lines[-1:] # Get last line
		murl = '0'
		if len(line) > 0:
			murl = re.sub("\t.*", "", line[0])
			murl = re.sub("\n", "", murl)

		return murl

	def getRepost(self, url, level=2, max=100):
		self.getRepostWorker(url, level, True, max)
		level = level - 1
		for i in range(1, level):
			for weibo_id in self.repost.keys():
				self.getRepostWorker(self.repost[weibo_id][2], level, False, max)
		#todo:remove the redundant relation 
		#think about it
		return self.repost

	def getRepostWorker(self, url, level, first, max):
		finished = False
		page = 1
		URL = ''

		if len(self.repost) >= max:
			return

		while not finished: 
			URL = url + '?type=repost&page=%d'  % page
			print 'url is ' + URL
			page = page + 1
			repostPageage = urllib2.urlopen(URL).read()
			self.writefile('repostPage', repostPageage)	
			#get repostHtml
			content = repostPageage.partition('{\"pid\":\"pl_content_weiboDetail\"')  
			jsonData = content[2].partition(')</script>')[0]
			jsonData = content[1] + jsonData
			#print jsonData
			htmlData = json.loads(jsonData)['html']
			self.writefile('repostHtml', htmlData)

			soup = BeautifulSoup(htmlData)
			#print soup.prettify()
			reposts = soup.findAll(attrs={'class' : "comment_list"})
			if len(reposts)>0 :
				print str(len(reposts))
				for post in reposts:
					mid  = post.get('mid')
					if mid and mid not in self.repost.keys():
						if mid == '3524300160600436' or mid == '3524287568904991' or mid == '3523632087162421' or mid == '3523630430176725': 
							print 'yes'	
						content = post.find('em')
						realcontent = self.clean_content(str(content))
						data =  str(post.find("a",{'action-type' : "feed_list_forward"}))	

						#rootmid = re.findall(r'rootmid=+(\d+)&amp', data)[0] #equal mid may not need
						#rootuid = re.findall(r'rootuid=+(\d+)+&amp', data)[0]
						#rooturl = re.findall(r'rooturl=+(.+?)&amp', data)[0] #equal URL may not need			
						#repostmid = re.findall(r';mid=+(\d+)+&amp', data)[0]
						#repostuid = re.findall(r';uid=+(\d+)&amp', data)[0]
						if content.find('a'):
							if len(re.findall(r'href=', str(content))) > level:
								continue
							else:
								repostname = re.findall(r'nick-name=\"+(.+?)\"', str(post))[0]
								if re.findall(r'>@+(.+?)<', str(content)):
									rootname = re.findall(r'>@+(.+?)<', str(content))[0]
								else:
									rootname = re.findall(r'rootname=+(.+?)&amp', data)[0]
								reposturl = re.findall (r';url=+(.+?)&amp', data)[0]

						elif first:
							rootname = re.findall(r'rootname=+(.+?)&amp', data)[0]
							repostname = re.findall(r';name=+(.+?)&amp', data)[0]
							reposturl = re.findall (r';url=+(.+?)&amp', data)[0]			    

						else:
							repostname = re.findall(r';name=+(.+?)&amp', data)[0]
							reposturl = re.findall (r';url=+(.+?)&amp', data)[0]

						if len(self.repost) < max:
							self.repost[mid] = [rootname, repostname, reposturl]
						else:
							return 

			else:
				finished = True

		return 

	def clean_content(self, content):

		content = re.sub("<img src=[^>]* alt=\"", "", content)
		content = re.sub("\" type=\"face\" />", "", content)
		content = re.sub("<[^>]*>", "", content)
		content = re.sub("&quot;", "\"", content)
		content = re.sub("&apos;", "\'", content)
		content = re.sub("&amp;", "&", content)
		content = re.sub("&lt;", "<", content)
		content = re.sub("&gt;", ">", content)

		return content		

	def writefile(self, filename, content):
		fw = file('./out/' + filename,'w')
		fw.write(content)
		fw.close()		

	def saveFile(self, data, dir):
		f = open(dir,'a+')
		for i in sorted(data.items(), key=lambda e:e[0], reverse=False):
			f.write(i[1])

		f.close()		

	def getKeyword(self, sentence, topK=20):
		content = open('idf.txt', 'rb').read().decode('utf-8')
		idf_freq = {}
		lines = content.split('\n')
		for line in lines:
			word,freq = line.split(' ')
			idf_freq[word] = float(freq)
		max_idf = max(idf_freq.values())	

		words = jieba.cut(sentence)
		freq = {}
		for w in words:
			if len(w.strip())<2: continue
			freq[w]=freq.get(w,0.0)+1.0
		total = sum(freq.values())
		freq = [(k,v/total) for k,v in freq.iteritems()]

		tf_idf_list = [(v * idf_freq.get(k, max_idf),k) for k,v in freq]
		#or wo treat it unknowitem as 0?
		#tf_idf_list = [(v * idf_freq.get(k, max_idf),k) for k,v in freq]
		st_list = sorted(tf_idf_list,reverse=True)

		top_tuples= st_list[:topK]
		#tags = [a[1] for a in top_tuples]

		return top_tuples	

	def getFollows(self, uid):
		followItems = []
		finished = False
		uid = int(uid)
		page = 1
		while not finished:
			URL ='http://weibo.com/%d/myfollow?t=1&page=%d' % (uid,page)
			print "now page : %d" % page
			page = page + 1		
			followsPageage = urllib2.urlopen(URL).read()
			self.writefile('followsPageage', followsPageage)	
			#get repostHtml
			content = followsPageage.partition('{\"pid\":\"pl_relation_myfollow\"')  
			jsonData = content[2].partition(')</script>')[0]
			jsonData = content[1] + jsonData
			#print jsonData
			followsData = json.loads(jsonData)['html']
			self.writefile('followsHtml', followsData)
			soup = BeautifulSoup(followsData)
			#print soup.prettify()
			follows = soup.findAll(attrs={'action-type' : "user_item"})
			if len(follows)>0 :
				for follow in follows:
					content = follow.find("a",{'class' : "S_link2"})
					content = str(content.get('action-data'))
					uid = str(re.findall(r'&uid=+(\d+)', content)[0])
					followItems.append(uid)	
			else:
				finished = True	
				
		return followItems

	def getFans(self, uid):
		fanItems = []
		finished = False
		uid = int(uid)
		page = 1
		while not finished:
			URL ='http://weibo.com/%d/myfans?t=1&page=%d' % (uid,page)
			print "now page : %d" % page
			page = page + 1		
			fansPageage = urllib2.urlopen(URL).read()
			self.writefile('fansPageage', fansPageage)	
			#get repostHtml
			content = fansPageage.partition('{\"pid\":\"pl_relation_fans\"')  
			jsonData = content[2].partition(')</script>')[0]
			jsonData = content[1] + jsonData
			#print jsonData
			fansData = json.loads(jsonData)['html']
			self.writefile('fansHtml', fansData)
			soup = BeautifulSoup(fansData)
			#print soup.prettify()
			fans = soup.findAll(attrs={'action-type' : "itmeClick"})
			if len(fans)>0 :
				for fan in fans:
					uid = str(re.findall(r'uid=+(\d+)&', str(fan))[0])
					fanItems.append(uid)	
			else:
				finished = True	
				
		return fans


