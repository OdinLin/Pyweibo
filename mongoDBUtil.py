import sys

from pymongo.errors import ConnectionFailure
from pymongo import Connection
#from pymongo.son_manipulator import AutoReference,NamespaceInjector
#from pymongo.code import Code

class mongoDBUtil:
	conn = None
	def __init__(self):
		try:
			self.conn = Connection('localhost', 27017)
		except ConnectionFailure:
			print 'not connect mongodb on localhost:27017'
			print 'connect fail...'
			sys.exit(1)
	
	#follows or fans	
	def saveData(self, data, database, collection):
		weiboDB = self.conn[database]
		for item in data:
			weiboDB.collection.insert(item)		
		return weiboDB.collection
	
	#for now,just 2 var first
	def analyseCollection(self, collection, **args, topN=5)
		list = """collection.group({
		"key":{args['key']:true},
		"initial":{"person":[]}, #consider not display person
		"reduce":function(doc, out){
			out.person.push(doc.name);
		},
		"finalize":function(out){
		out.count = out.person.length;
		},
		"condition":args['condition']
		})"""
		
		sorted_list = sorted(list, key=lambda list : list['count'], reverse=True)
		
		collection.drop() #is it necessory to remove collection?
		return sorted_list[:topN]
		
	def analyseCollection2(self, collection, topN=5)
		mapper=Code("""function () {
			this.interestTag.forEach(function(z) {
				emit(z, {count:1});
			});
		}
		""")
		reducer= Code("""
			function (key, values) {
			var total = 0;
			for (var i = 0; i < values.length; i++) {
				total += values[i].count;
			}
			
			return {count:total};
		}
		""")
		
		results = collection.mapReduce(mapper,reducer,out="resultCollection")
		for result in results.find():
			print result['_id'] , result['value']['count']
		
		resultCollection.drop()
	