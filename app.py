from flask import Flask, json, request
from flask_cors import CORS, cross_origin
import datetime
import MySQLdb as mdb


app = Flask(__name__)
CORS(app)

with open('config_file.json') as config_file:
	config = json.load(config_file)

conn = mdb.connect(host=config['host'], user=config['user'], passwd=config['password'], db=config['db'])

cur = conn.cursor()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/testing')
def test():
    return 'Hello, test!'

def get_events(zybook_code, user_id):
	query = "SELECT event FROM user WHERE zybook_code=" + "'" + zybook_code + "'"
	cur.execute(query)
	rows = cur.fetchall()
	user_rows = []
	for elem in rows:
		if json.loads(elem[0])['event']['user_id'] == int(user_id):
			user_rows.append(json.loads(elem[0])['event'])

	return user_rows

@app.route('/zybook/<zybook_code>/events/<user_id>', methods = ['GET'])
def get_user_zybook_events(zybook_code, user_id):
	user_rows = get_events(zybook_code, user_id)
	return json.dumps({'success': True, 'events': user_rows})

@app.route('/zybook/<zybook_code>/event', methods = ['POST'])
def record_zybook_event(zybook_code):
	cur.execute("INSERT INTO user(zybook_code, event) VALUES(%s, %s)", (zybook_code, json.dumps({'event': {'chapter_number': request.json.get('chapterNum'), 'section_number': request.json.get('sectionNum'), 'user_id': request.json.get('user_id'), 'date': datetime.datetime.now().isoformat()}})))
	conn.commit()
	user_rows = get_events(zybook_code, request.json.get('user_id'))
	return json.dumps({"success": True, 'events': user_rows})

if __name__ == '__main__':
    app.run(use_reloader=True, threaded=True)