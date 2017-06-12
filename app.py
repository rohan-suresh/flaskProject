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

@app.route('/postData', methods = ['POST'])
def postData():
	print(request.json.get('zybook_code'))
	cur.execute("INSERT INTO user(zybook_code, event) VALUES(%s, 'event')", (request.json.get('zybook_code'), ))
	conn.commit()
	return json.dumps({"success": True})

if __name__ == '__main__':
    app.run(use_reloader=True)