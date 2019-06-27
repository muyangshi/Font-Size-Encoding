'''
    the Flask server
    Muyang Shi, 6/24/2019
'''

import sys
import json
import flask
import random
import csv
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

words = ['Apples', 'Apricots', 'Avocados',
    'Bananas', 'Boysenberries', 'Blueberries', 'Bing Cherry',
    'Cherries', 'Cantaloupe', 'Crab apples', 'Clementine', 'Cucumbers',
    'Damson plum', 'Dinosaur Eggs', 'Dates', 'Dewberries', 'Dragon Fruit',
    'Elderberry', 'Eggfruit', 'Evergreen Huckleberry', 'Entawak',
    'Fig', 'Farkleberry', 'Finger Lime',
    'Grapefruit', 'Grapes', 'Gooseberries', 'Guava',
    'Honeydew melon', 'Hackberry', 'Honeycrisp Apples',
    'Indian Prune', 'Indonesian Lime', 'Imbe', 'Indian Fig']

@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def get_hello_page():
	return flask.render_template('index.html')

@app.route('/randomStim/<numberOfWords>')
def randomStim(numberOfWords):
    try:
        random_words = random.sample(words, int(numberOfWords))
        return json.dumps(random_words)
    except ValueError:
        print('numberOfWords is too big!')
        
@app.route('/randomStim/receive_data', methods = ['POST'])
def receive_data():
    data = flask.request.form.to_dict()
    clickedword = data["word"]
    word_x = data["word position[left]"]
    word_y = data["word position[top]"]
    cloud_width = data["container size[width]"]
    cloud_height = data["container size[height]"]
    num_of_Stim = data["number of Stim"]
    cloud_info = data["cloud"]

    print('clicked word: ' + clickedword, word_x, word_y)
    print('cloud information: ' + num_of_Stim, cloud_info)
    with open('client_data.csv','w', newline='') as csvfile:
        # fieldnames = ['clickedword','word_x','word_y','cloud_width','cloud_height','num_of_Stim','cloud_info']
        writer = csv.writer(csvfile, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([clickedword, word_x, word_y, cloud_width, cloud_height, num_of_Stim, cloud_info])
    return json.dumps(data)


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: {0} host port'.format(sys.argv[0]))
		print('  Example: {0} allen.mathcs.carleton.edu xxxx'.format(sys.argv[0]))
		exit()
	
	host = sys.argv[1]
	port = int(sys.argv[2])
	app.run(host=host, port=port, debug=True)