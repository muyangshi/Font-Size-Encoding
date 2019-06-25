'''
    the Flask server
    Muyang Shi, 6/24/2019
'''

import sys
import json
import flask
import config
# import psycopg2

app = flask.Flask(__name__)

@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def hello():
	return 'Hello, Tuckers.'

@app.route('/randomStim/<num words>')
def get_random_cloud():
    pass

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: {0} host port'.format(sys.argv[0]))
		print('  Example: {0} allen.mathcs.carleton.edu xxxx'.format(sys.argv[0]))
		exit()
	
	host = sys.argv[1]
	port = int(sys.argv[2])
	app.run(host=host, port=port, debug=True)