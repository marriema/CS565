from flask import Flask, abort, request, jsonify, render_template, redirect, url_for, session
import pymongo
import json, re
import datetime
from datetime import date


from mystat import get_topk_factors


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

client = pymongo.MongoClient("mongodb+srv://marrie:qingqingniao@cluster0-vrtyn.gcp.mongodb.net/test?retryWrites=true")
db = client.CS565

users = db["users"]
periods = db["periods"]
factors = db["factors"]


@app.route("/index", methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def index():
	if not session.get('username'): #user not logged in
		return redirect(url_for('login'))
	else:
		ret, not_finished_period = getPastPeriods(True)
		pp = []
		for each in ret:
			pp.append([each[0], each[1]])
		
		return render_template('index.html', username=session.get('username'), pp=pp, not_finished_period=not_finished_period)


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
	#find last inserted period
	last_period = periods.find_one(
  				{'username': session['username']},
  				sort=[( '_id', pymongo.DESCENDING )])

	if request.method == 'GET':
		if last_period is not None:
			if last_period['end_date'] is None:
				return jsonify(status='OK',lastPeriod=str(last_period['start_date']))

		return jsonify(status='OK',lastPeriod='none')
	else:
		res = request.get_json()["action"]
		if res == "start":  #start a new period
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
			return jsonify(status='OK')
		else:  #end current period
			d = datetime.date.today()
			day = '%02d' % d.day
			month = '%02d' % d.month
			year = '%02d' % d.year

			complete_date = month+'/'+day+'/'+year
			periods.update_one(
				 {'_id': last_period['_id']},
				{
				'$set':
				{
					"end_date":complete_date
				}}, upsert=False)
			return jsonify(status='OK')

	return jsonify(status='OK')



@app.route('/moods', methods=["GET", "POST"])
def pastMoods():
	d = datetime.date.today()
	day = '%02d' % d.day
	month = '%02d' % d.month
	year = '%02d' % d.year

	complete_date = month+'/'+day+'/'+year

	today = factors.find_one(
  				{'username': session['username'],
				 'date': complete_date})

	if request.method == 'GET':  #get today's moods and factors
		if today is not None:
			today['_id'] = ""
			return jsonify(status='OK',today=today)
		return jsonify(status='OK',today='none')

	else:  #post moods and factors
		res = request.get_json()
		factors_res = res["factors"]
		moods_res = res["moods"]
		if today is None:
			new_record = {
				"username": session['username'],
				"date": complete_date,
				"factors": factors_res,
				"moods": moods_res
			}
			factors.insert_one(new_record)
		else:
			factors.update_one(
				 {'_id': today['_id']},
				{
				'$set':
				{
					"factors": factors_res,
					"moods": moods_res
				}}, upsert=False)
		return jsonify(status='OK')



@app.route('/periodHistory')
def periodHistory():
	return render_template('periodHistory.html',username=session.get('username'))


@app.route('/getPastPeriods')
def getPastPeriods(local=False):
	
	history = periods.find({'username': session['username']},sort=[( '_id', pymongo.ASCENDING )])
	history = list(history)
	ret = []
	not_finished_period = None

	for i, each in enumerate(history):

		if each["end_date"] is not None:
			start_split = each["start_date"].split('/')
			end_split = each["end_date"].split('/')
			d0 = date(int(start_split[2]), int(start_split[0]), int(start_split[1]))
			d1 = date(int(end_split[2]), int(end_split[0]), int(end_split[1]))
			period_len = abs(d1-d0).days

			cycle_len = 0
			if i is not len(history)-1:
				next = history[i+1]
				cycle_end_split = next["start_date"].split('/')
				d0 = date(int(end_split[2]), int(end_split[0]), int(end_split[1]))
				d1 = date(int(cycle_end_split[2]), int(cycle_end_split[0]), int(cycle_end_split[1]))
				cycle_len = abs(d1-d0).days

			else:
				d1 = datetime.date.today()
				cycle_len = abs(d1 - date(int(start_split[2]), int(start_split[0]), int(start_split[1]))).days

			ret.append([each["start_date"], each["end_date"], period_len, cycle_len])
		else: #current not_finished period
			not_finished_period = each["start_date"]

	if local is False:
		return jsonify(status='OK', history=ret, not_finished_period=not_finished_period)
	else:
		return (ret, not_finished_period)


@app.route('/getPastFactors', methods=["POST"])
def getPastFactors():
	res = request.get_json()

	start_split = res["start_date"].split('/')
	d0 = date(int(start_split[2]), int(start_split[0]), int(start_split[1]))
	d1 = None

	if res["end_date"] is not None:
		end_split = res["end_date"].split('/')
		d1 = date(int(end_split[2]), int(end_split[0]), int(end_split[1]))

	ret = []
	history = factors.find({'username': session['username']},sort=[( '_id', pymongo.ASCENDING )]) #find all factors of this person
	history = list(history)
	for i, each in enumerate(history):
		current_date = each["date"].split('/')
		current_date = date(int(current_date[2]), int(current_date[0]), int(current_date[1]))
		if current_date >= d0 and ((d1 is None) or (current_date <= d1)):
			mood_avg = []
			if int(each["moods"]["mood1"]) != -1:
				mood_avg.append(int(each["moods"]["mood1"]))
			if int(each["moods"]["mood2"]) != -1:
				mood_avg.append(int(each["moods"]["mood2"]))

			if len(mood_avg) == 0:
				mood_avg = 0
			else:
				mood_avg = float(sum(mood_avg)/len(mood_avg))
			
			t = each["factors"]
			for key,value in t.iteritems():
				t[key] = int(value)
				if t[key] > -1:
					t[key] -= 1

			ret.append({
				'date': each["date"],
				'moods': mood_avg,
				'factors': t
			})
	
	return jsonify(status='OK', history=ret)






@app.route('/test_add', methods=["GET"])
def test_add():
	uname = 's'
	cdate = '04/21/2019'
	mds = [
	{'mood1':0, 'mood2':0},
	{'mood1':6, 'mood2':6},
	{'mood1':5, 'mood2':5},
	{'mood1':3, 'mood2':3},
	{'mood1':0, 'mood2':0},
	{'mood1':1, 'mood2':1},
	{'mood1':5, 'mood2':5},
	{'mood1':4, 'mood2':5},
	{'mood1':1, 'mood2':2},
	{'mood1':1, 'mood2':2}
	]
	fs = [
	{'alcohol':1, 'caffeine':1, 'sugar':1, 'water':1, 'sleep':3, 'social':4, 'eat':2, 'exercise':4},
	{'alcohol':4, 'caffeine':4, 'sugar':4, 'water':2, 'sleep':1, 'social':1, 'eat':2, 'exercise':1},
	{'alcohol':3, 'caffeine':4, 'sugar':3, 'water':3, 'sleep':2, 'social':2, 'eat':2, 'exercise':2},
	{'alcohol':2, 'caffeine':2, 'sugar':2, 'water':4, 'sleep':2, 'social':2, 'eat':2, 'exercise':2},
	{'alcohol':2, 'caffeine':2, 'sugar':2, 'water':1, 'sleep':4, 'social':4, 'eat':2, 'exercise':4},
	{'alcohol':1, 'caffeine':1, 'sugar':1, 'water':2, 'sleep':3, 'social':3, 'eat':2, 'exercise':3},
	{'alcohol':4, 'caffeine':4, 'sugar':4, 'water':3, 'sleep':2, 'social':1, 'eat':2, 'exercise':1},
	{'alcohol':3, 'caffeine':3, 'sugar':4, 'water':4, 'sleep':1, 'social':2, 'eat':2, 'exercise':1},
	{'alcohol':1, 'caffeine':1, 'sugar':1, 'water':1, 'sleep':4, 'social':4, 'eat':2, 'exercise':3},
	{'alcohol':2, 'caffeine':2, 'sugar':1, 'water':2, 'sleep':3, 'social':4, 'eat':2, 'exercise':4}
	]
	for i in range(10):
		factors.insert_one({
			'username':uname,
			'date':cdate,
			'factors':fs[i],
			'moods':mds[i],
		})
	return jsonify(status='OK')

@app.route('/get_factors', methods=["GET"])
def get_factors():
	# Retrieve all the everyday moods, factors
	data = factors.find({"username" : session["username"]})
	data_list = list(data)
	top_k = get_topk_factors(data_list, 3)
	return jsonify(status='OK', data = top_k)
	# Pass the data to stat module
	# Return top k factors and their scores as json string

if __name__ == '__main__':
	app.run(debug = True)
