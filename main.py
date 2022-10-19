from app.function.functions import getNumberProvider
from app.server.svdb import Svdb
from flask import Flask
from flask import request
from flask import render_template
from app.api.syntax import *
from app.api.control import *
import sqlite3

app = Flask(__name__)
database = sqlite3.connect("database/database.db",check_same_thread=False)
cursor = database.cursor()
databaseControler = DatabaseControler(database,cursor)
server = Svdb(database,cursor)

@app.route("/api/<name>/paid_function",methods=["GET","POST"])
def paidapi(name):
    if request.method=="GET":
        return render_template("login.html")
    elif request.method == "POST":
        print(request.get_data().decode("utf-8"))
        status,data = dataHandling(request.get_data().decode("utf-8"))
        if status != 200: return data,status
        status,information = databaseControler.paidAPIRequest(name,data["apikey"])
        if status != 200: return information,status
        provider = getNumberProvider(data["number"])
        databaseControler.updateBalance(name)
        return databaseControler.response(name,"provider",provider),200
    else:
        return "Method not Allowed",405

@app.route("/api/newmember/<name>",methods=["GET","POST"])
def newmemberapi(name):
    if request.method == "GET":
        ipAdd = request.remote_addr # get client public ip address
        try:
            server.newMember(name,ipAdd)
            return f"username: {name} have been added successfully !"
        except:
            return f"username: {name} already in database"

@app.route("/api/morebalance/<name>",methods=["GET","POST"])
def addbalanceapi(name):
    if request.method == "GET":
        server.addBalance(name,200.00)
        return f"successfully added more 200$ to {name} balance !"