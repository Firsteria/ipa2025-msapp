from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
mydb = client["ipa2025"]
collection = mydb["routers"]

@app.route("/")
def main():
    try:
        data = collection.find({}, {'password':0})
        return render_template("index.html", data=data)
    except Exception as e:
        return f"Error loading data: {e}"

@app.route("/add", methods=["POST"])
def add_comment():
    routerip = request.form.get("routerip")
    username = request.form.get("username")
    password = request.form.get("password")

    if username and password:
        collection.insert_one({"routerip": routerip, "username": username, "password": password})
    return redirect(url_for("main"))

@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = request.form.get("idx")
        myquery = {'_id': ObjectId(idx)}
        collection.delete_one(myquery)
        #if 0 <= idx < len(data):
         #   data.pop(idx)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)