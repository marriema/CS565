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
		return render_template('login.html')
	else:
		return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == 'GET':
		return render_template("login.html")
	else:
		if request.form['submit_btn'] == 'signup':
			newName = request.form['username']
			newPass = request.form['password']
			addNewUserAccount(newName, newPass)

			session['username'] = newName
			return redirect(url_for('index'))
		else:
			userName = request.form['username']
			password = request.form['password']
			userInfo = users.find_one({"username":userName})
			foundPassword = userInfo["password"]

			if str(foundPassword) == password:
				session['username'] = userName
				return redirect(url_for('index'))
			else:	
				return redirect(url_for('login'))




def addNewUserAccount(username, password):
	newUserAccount = {"username":username, "password":password}
	users.insert_one(newUserAccount)
	return


@app.route('/logout')
def logout():
	session['username'] = None
	return redirect(url_for('login'))



if __name__ == '__main__':
	app.run(debug = True)
