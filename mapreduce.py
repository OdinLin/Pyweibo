#coding=utf8

from pymongo import Connection
from bson.code import Code

db = Connection().test
#先删除things集合
db.things.drop()
db.things.insert({"x":1,"tags":["dog","cat"]})
db.things.insert({"x":2,"tags":["cat"]})
db.things.insert({"x":3,"tags":["mouse","cat","dog"]})
db.things.insert({"x":4,"tags":[]})

mapper = Code("""function() {
this.tags.forEach(function(z) {
emit(z, 1);
});
}
""")
reducer = Code("""
function(key, values) {
var total = 0;
for (var i = 0; i < values.length; i++) {
total += values[i];
}
return total;
}
""")

result=db.things.map_reduce(mapper,reducer,out ="myresults",full_response=True,query={"tags":{"$exists": "true"}})

print result
for doc in db.myresults.find():
	print doc
#删除保存结果的集合
db.myresults.d