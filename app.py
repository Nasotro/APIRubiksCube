import pymongo
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS


cluster = MongoClient("mongodb+srv://Lorrain_Password:0ui0uiBaguette@cluster0.lt7grto.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Rubiks_Cube_Timings"]

print(db.list_collection_names())

app = Flask(__name__)
app.config["DEBUG"]=True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/All_Session/", methods=['GET', 'POST', 'DELETE'])
def All_Session():
    #return all sessions
    if request.method == "GET":
        return(jsonify(db.list_collection_names()))
    #crée un nouvelle session
    if request.method == "POST":
        list_Coll = db.list_collection_names()
        new_Nom = request.form["Nom"]
        if(new_Nom not in list_Coll):
            db.create_collection(new_Nom)
            return(f"la session {new_Nom} a bien été crée")
        else:
            return(f"La session {new_Nom} existe déja")
    #supprime une session
    if request.method=="DELETE":
        new_Nom = request.form["Nom"]
        if(new_Nom in db.list_collection_names()):
            db[new_Nom].drop()
            return(f"la session {new_Nom} a bien été retirée")
        return(f"la session {new_Nom} n'existe pas")


@app.route('/Single_Session/<string:nomSession>', methods = ['GET', 'POST'])
def Single_Sessions(nomSession):
    Session = db[nomSession]
    #return tous les temps d'une certaine session
    if request.method=='GET':
        result = list(Session.find({}))
        t = []
        for x in result:
            t.append(x)
        t.reverse()
        if t is not None:
            return jsonify(t)
        else :
            return ("something wrong")
    #rajoute un temps dans la session en question
    if request.method == "POST":
        last_id = 0
        if(len(list(Session.find({}))) > 0):
            last_id = Session.find({}).sort([('_id', -1)]).limit(1)[0]['_id']
        new_Temp = request.form["Temps"]
        new_Melange = request.form["Melange"]
        post = {"_id": last_id+1, "Temps":new_Temp, "Melange":new_Melange}
        Session.insert_one(post)
        return f"Le Temp {new_Temp} avec l'id {last_id+1} et le melange {new_Melange} a bien été ajouté dans la table {nomSession}", 201


@app.route('/Single_Time/<string:nomSession>', methods=["GET", "PUT", "DELETE"])
def single_Temps(nomSession):
    print(request.form['id'])
    id=int(request.form['id'])
    Session = db[nomSession]
    #return les infos d'un temps en fonction de son id
    if request.method == "GET":
        Temps = Session.find_one({'_id':id})
        print(Temps)
        if Temps is not None:
            return jsonify(Temps), 200
        else :
            return "Something Wrong", 404
    #modifie les infos d'un temps en fonction de son id
    if request.method=="PUT":
        new_Temp = request.form["Temps"]
        new_Melange = request.form["Melange"]
        set = {"$set":{"Temps":new_Temp, "Melange":new_Melange}}
        Session.update_one({'_id':id}, set)
        return f"Le Temp avec l'id {id} a bien été modifié : {new_Temp}, {new_Melange} ", 201
    #supprime un temps en fonction de son id
    if request.method=="DELETE":
        Session.delete_one({"_id":id})
        return f"The Temps with id: {id} has been deleted.".format(id), 200
        
if __name__ == '__main__':
    app.run(debug=True)


