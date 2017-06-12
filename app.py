from flask import Flask, json, request
from flask_cors import CORS, cross_origin
import datetime
import MySQLdb as mdb


app = Flask(__name__)
CORS(app)

conn = mdb.connect('localhost', 'root', 'rohan1997', 'Events')
cur = conn.cursor()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/testing')
def test():
    return 'Hello, test!'

@app.route('/getData', methods = ['GET'])
def getData():
	return json.dumps({"success": True,
  "events": [ {"chapter_number": 1, "section_number": 1, "user_id": 333, "date": datetime.datetime.now().isoformat()}, {"chapter_number": 1, "section_number": 1, "user_id": 444, "date": datetime.datetime.now().isoformat()}, {"chapter_number": 2, "section_number": 2, "user_id": 555, "date": datetime.datetime.now().isoformat()}]})

@app.route('/zybook/<zybook_code>/event', methods = ['POST'])
def postData(zybook_code):
	cur.execute("INSERT INTO user(zybook_code, event) VALUES(%s, %s)", (zybook_code, json.dumps({'event': {'chapter number': request.json.get('chapterNum'), 'section number': request.json.get('sectionNum'), 'user id': request.json.get('user_id'), 'date': datetime.datetime.now().isoformat()}}))) #
	#datetime.datetime.now().isoformat()
	#event: chapter_num, section_num, user_id, date
	conn.commit()
	return json.dumps({"success": True})

if __name__ == '__main__':
    app.run(use_reloader=True)