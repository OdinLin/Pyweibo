#encoding=utf-8

import csv

class sentimentUtil:
	hownetComment = {}
	hownetSentiment = {}
	def __init__(self):
		file_object = open('row/hownet.positive.comment.txt') 
		list_of_all_the_lines = file_object.readlines( )		
		for line in list_of_all_the_lines:
			item = line.replace(" ","").replace("\t","").strip() 
			hownetComment[item] = '1'				
		
		file_object = open('row/hownet.negative.comment.txt') 
		list_of_all_the_lines = file_object.readlines( )		
		for line in list_of_all_the_lines:
			item = line.replace(" ","").replace("\t","").strip() 
			hownetComment[item] = '0'
			
		file_object = open('row/hownet.positive.sentiment.txt') 
		list_of_all_the_lines = file_object.readlines( )		
		for line in list_of_all_the_lines:
			item = line.replace(" ","").replace("\t","").strip() 
			hownetSentiment[item] = '1'		
			
		file_object = open('row/hownet.negative.sentiment.txt') 
		list_of_all_the_lines = file_object.readlines( )		
		for line in list_of_all_the_lines:
			item = line.replace(" ","").replace("\t","").strip() 
			hownetSentiment[item] = '0'				
			
		#another file to read in...
		
	#calc a feed's sentiment
	#it has two condition:
	#1.it's just a comment, so we judge it is a positive or negetive, return 1 or 0
	#if the feed's key word is all in hownetSentiment, we treat it a comment
	#otherwise, it's a sentiment, is there a better ider to judge?
	#2.the feed has sentiment in it,so we will calc it is value
	#data inme is strint, i guess
	def calcFeedSentiment(self, data):
		#todo:
		#first we should clean the data 
		#then call the isSentiment to judge
		#then calc one of the two condition!!!
		print 'mission complete'
	
	#data income must a list contain all the item	
	def isSentiment(self, listdata):
		#todo:judge the data whether it contain sentiment 
		return True
	
		
