import pymongo
from pymongo import MongoClient
from flask import jsonify
from random import randint as rdi

cluster = MongoClient("mongodb+srv://Lorrain_Password:0ui0uiBaguette@cluster0.lt7grto.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Rubiks_Cube_Timings"]

list_Coll = db.list_collection_names()

print(list_Coll)

if("Test" not in list_Coll):
    db.create_collection("Test")
    print("on a créé test")
else:
    print("existe déja")
    db["Test"].drop()
    print("test a été suppr")

Session = db["Session1"]
result = list(Session.find({}))
print(Session.count_documents({}))
t = []
for x in result:
    t.append(x)
print(t)


for x in Session.find().sort([('_id', -1)]):
    print("aaaaaaaaaaaa", x)
last_id = int(Session.find().sort([('_id', -1)]).limit(1)[0]['_id'])
print("last_id : ", last_id)
post = {"_id": last_id+1, "Temps":rdi(0,20), "Melange":"ABCDEFGH"[rdi(0,6)]}
#Session.insert_one(post)

print(Session.find_one({'_id':2}))

post = {"$set":{"Temps":rdi(0,100), "Melange":"ABCDEFGHIJKLMNOPQRSTUVWXYZ"[rdi(0,10):rdi(11,23)]}}
Session.update_one({'_id':4}, post)
print(Session.find_one({'_id':4}))


res = Session.delete_one({"_id":4})
print(res)

