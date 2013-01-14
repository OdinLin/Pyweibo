import weiboUtil
import visualizationUtil
import mongoDBUtil

class Pyweibo:
	weiboutil = None
	visualizationutil = None
	mongoDButil = None

	def __init__(self):
		self.weiboutil = weiboUtil.weiboUtil()
		self.visualizationutil = visualizationUtil.visualizationUtil()
		self.mongoDButil = mongoDBUtil.mongoDBUtil()

	def generateRepostMap(self, url, level=2, max=100, out='./out/repost'):
		repost = self.weiboutil.getRepost(url, level, max)
		self.visualizationutil.generateDotFile(repost, out)

	def getRepost(self, url, level=2, max=100):
		return	weiboutil.getRepost(url, level, max)
	
#	def saveRepost2Mongo(self, url, level=2, max=100):
#		repost = weiboutil.getRepost(url, level, max)
#		mongoDButil.saveData(repost, 'repost')
	
	
	#analyse the follows and fans data from weiboUtil.getFollows and weiboUtil.getFans
	#data format will be like [{uid:*, nickname:*}, ...] a dictionary list
	#follows_diff_fans:people who you follow doesn't follow you
	#fans_diff_follows:people who following you but you don't follow
	#follows_inter_fans:people who follow each other
	
	#wo can analyse some useful and funny info about follows or fans, like:
	#topN of fans(follows)'s interest(all? male? female)
	#topN of fans(follows)'s school(all? male? female)
	#topN of fans(follows)'s company(all? male? female)
	#...
	def analyseFollowsFansInfo(self, uid, F='follow'):
		follows = self.weiboutil.getFollows(uid)
		fans = self.weiboutil.getFans(uid)
		#add to do:uid to dic
		if F is 'follow':
			profiles = [self.weiboutil.getPersonalProfile(uid) for uid in follows]
			collection = mongoDButil.saveData(profiles, 'follows', uid)
		elif F is 'fan':
			profiles = [self.weiboutil.getPersonalProfile(uid) for uid in fans]
			collection = mongoDButil.saveData(profiles, 'fans', uid)
		
		#top5 of fans(follows)'s company in male
		#if no condition, condition will be {}
		list = mongoDButil.analyseCollection(collection, key=company, condition={'sex': 'male'}, topN=5)
		#list = mongoDButil.analyseCollection(collection, key=school, condition={'sex': 'male'}, topN=5)
		print list
		
		
		print 'extra info:\n'
		nfollows, nfans = len(follows), len(fans)
		print 'you have %d follows and %d fans\n' % (nfollows, nfans)
		follows_diff_fans = len([val for val in follows if val not in fans])
		print '%d of %d your follows have not follow you\n' % (follows_diff_fans, nfollows)
		fans_diff_follows = len([val for val in fans if val not in follows])
		print '%d of %d your fans you have not follow\n' % (fans_diff_follows, nfans)
		follows_inter_fans = len([val for val in follows if val in fans])
		print '%d people have follow each other\n' % follows_inter_fans
		
		return
	
	def getPersonalProfile(self, uid):
		self.weiboutil.getPersonalProfile(uid)
	
	#todo
	#beside get a person's profile, we can get a lot of
	#info from it.
	def analysePerson(self, uid):
		#fill me!
		return
		
		