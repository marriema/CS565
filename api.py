from flask import Flask, abort, request, jsonify, render_template, redirect, url_for, session
import pymongo
import json, re
import datetime



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
		return redirect(url_for('login'))
	else:
		return render_template('index.html', username=session.get('username'))


@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == 'GET':
		return render_template('login.html')
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



@app.route('/signup', methods=["GET", "POST"])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		newName = request.form['username']
		newPass = request.form['password']
		addNewUserAccount(newName, newPass)

		session['username'] = newName
		return redirect(url_for('index'))


def addNewUserAccount(username, password):
	newUserAccount = {"username":username, "password":password}
	users.insert_one(newUserAccount)
	return


@app.route('/logout')
def logout():
	session['username'] = None
	return redirect(url_for('login'))


@app.route('/pastPeriods', methods=["GET", "POST"])
def pastPeriods():
	if request.method == 'GET':
		#find last inserted period
		last_period = periods.find_one(
  				{'username': session['username']},
  				sort=[( '_id', pymongo.DESCENDING )])
				  
		if last_period is not None:
			if last_period['end_date'] is None:
				print last_period
				return jsonify(status='OK',lastPeriod=str(last_period['start_date']))

		return jsonify(status='OK',lastPeriod='none')
	else:
		res = request.get_json()["action"]
		if res == "start":
			d = datetime.date.today()
			day = '%02d' % d.day
			month = '%02d' % d.month
			year = '%02d' % d.year

			complete_date = month+'/'+day+'/'+year
			new_period = {
				"username": session['username'],
				"start_date":complete_date,
				"end_date":None
			}
			periods.insert_one(new_period)
			return 'ok'
		else:
			return 'ok'

	return 'ok'







if __name__ == '__main__':
	app.run(debug = True)
