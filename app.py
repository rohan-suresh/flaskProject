from flask import Flask, json
from flask_cors import CORS, cross_origin
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/testing')
def test():
    return 'Hello, test!'

@app.route('/getData', methods = ['GET'])
def getData():
	return json.dumps({"success": True,
  "events": [ {"chapter_number": 1, "section_number": 1, "user_id": 333, "date": datetime.datetime.now().isoformat()}, {"chapter_number": 1, "section_number": 1, "user_id": 444}]})

if __name__ == '__main__':
    app.run(use_reloader=True)