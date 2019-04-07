from flask import Flask, abort, request, jsonify, render_template, redirect, url_for, session
import pymongo
import json, re


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

client = pymongo.MongoClient("mongodb+srv://marrie:qingqingniao@cluster0-vrtyn.gcp.mongodb.net/test?retryWrites=true")
db = client.CS565

users = db["users"]
periods = db["periods"]
moods = db["moods"]
factors = db["factors"]


@app.route("/index", methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def index():
	if not session.get('username'): #user not logged in
		return jsonify({'message': 'not_logged_in'})
	else:
		return jsonify({'message': 'logged_in'})


@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == 'GET':
		return jsonify({'message': 'not_logged_in'})
	else:
		userName = request.get_json()['username']
		password = request.get_json()['password']
		userInfo = users.find_one({"username":userName})
		foundPassword = userInfo["password"]

		if str(foundPassword) == password:
			session['username'] = userName
			return jsonify({'message': 'logged_in'})
		else:	
			return jsonify({'message': 'not_logged_in'})



@app.route('/signup', methods=["GET", "POST"])
def signup():
	if request.method == 'GET':
		return jsonify({'message': 'not_logged_in'})
	else:
		newName = request.get_json()['username']
		newPass = request.get_json()['password']
		addNewUserAccount(newName, newPass)

		session['username'] = newName
		return jsonify({'message': 'logged_in'})
		


def addNewUserAccount(username, password):
	newUserAccount = {"username":username, "password":password}
	users.insert_one(newUserAccount)
	return


@app.route('/logout')
def logout():
	session['username'] = None
	return jsonify({'message': 'not_logged_in'})



if __name__ == '__main__':
	app.run(debug = True)
