'''
    the Flask server
    Muyang Shi, 6/24/2019
'''

import sys
import json
import random
import flask
# import config
# import psycopg2

app = flask.Flask(__name__)

# def get_connection():
# 	'''
# 	Returns a connection to the database described
# 	in the config module. Returns None if the
# 	connection attempt fails.
# 	'''
# 	connection = None
# 	try:
# 		connection = psycopg2.connect(database=config.database,
# 									  user=config.user,
# 									  password=config.password)
# 	except:
# 		try:
# 			connection = psycopg2.connect(database=config_johnny.database,
# 									  user=config_johnny.user,
# 									  password=config_johnny.password)
# 		except Exception as e:
# 			print(e, file=sys.stderr)
# 	return connection

words = ['apple','orange','pear','peach','tangerine','banana']

@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def hello():
	return 'Hello, Tuckers.'

@app.route('/randomStim/<numberOfWords>')
def get_random_cloud(numberOfWords):
    try:
        random_words = random.sample(words, int(numberOfWords))
    except ValueError:
        print('numberOfWords is too big!')
    return json.dumps(random_words)


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: {0} host port'.format(sys.argv[0]))
		print('  Example: {0} allen.mathcs.carleton.edu xxxx'.format(sys.argv[0]))
		exit()
	
	host = sys.argv[1]
	port = int(sys.argv[2])
	app.run(host=host, port=port, debug=True)