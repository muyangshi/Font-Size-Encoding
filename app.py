'''
    the Flask server
    Muyang Shi, 6/24/2019
'''

import sys
import json
import ast
import flask
import random
import csv
from flask_util_js import FlaskUtilJs
from Configures import test_length_config as config
# import config
# import psycopg2

app = flask.Flask(__name__)
fujs = FlaskUtilJs(app)

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
    'Indian Prune', 'Indonesian Lime', 'Imbe', 'Indian Fig',
    'Apples', 'Apricots', 'Avocados',
    'Bananas', 'Boysenberries', 'Blueberries', 'Bing Cherry',
    'Cherries', 'Cantaloupe', 'Crab apples', 'Clementine', 'Cucumbers',
    'Damson plum', 'Dinosaur Eggs', 'Dates', 'Dewberries', 'Dragon Fruit',
    'Elderberry', 'Eggfruit', 'Evergreen Huckleberry', 'Entawak',
    'Fig', 'Farkleberry', 'Finger Lime',
    'Grapefruit', 'Grapes', 'Gooseberries', 'Guava',
    'Honeydew melon', 'Hackberry', 'Honeycrisp Apples',
    'Indian Prune', 'Indonesian Lime', 'Imbe', 'Indian Fig',
    'Apples', 'Apricots', 'Avocados',
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
	return flask.redirect(flask.url_for('get_landing_page'))

@app.route('/word_cognition_study')
def get_landing_page():
    return flask.render_template('landing.html')

# Get the description page, with turker_id as the data passed from HTML form from landing page
@app.route('/word_cognition_study/description', methods = ['POST'])
def get_description():
    turker_id = flask.request.form['turker_id']
    return flask.render_template('description.html', ID = turker_id)

# Get the description page; turker_id is passed from description page through HTML form
@app.route('/word_cognition_study/stimuli', methods = ['POST'])
def get_stimuli_page():
    turker_id = flask.request.form['turker_id']
    # print(turker_id)
    return flask.render_template('stimuli.html', ID = turker_id, List_From_Server=get_tasklist())


@app.route('/word_cognition_study/completion', methods=['POST'])
def get_completion():
    data = flask.request.form
    hash_code = hash(data['turker_id'] + 'Carleton')
    # print(hash_code,type(hash_code))
    return flask.render_template('completion.html', Hash_Code = hash_code)






# Write the turker's id into a csvfile --> client_id.csv
@app.route('/word_cognition_study/turker_id', methods = ['POST'])
def receive_id():
    data = flask.request.form
    turker_id = data["turker_id"]
    # print('receive turker id: ' + turker_id)
    with open('client_id.csv','a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',', quotechar='"')
        hashcode = hash(turker_id+'Carleton')
        writer.writerow([turker_id,hashcode])
    return json.dumps({'id':turker_id,'hashcode':hashcode})
 
# Get the tasklist from test_length_config.py, the tasklist is from test_length.csv
# The format of the tasklist is 
# [{'target_1_fontsize':int,'target_1_length':int,'target_2_fontsize':int,'target_2_length':int},{},{},...]
def get_tasklist():
    tasklist = config.tasklist
    return json.dumps(tasklist)





def list_of_stimuli():
    # Messy Pointer, so read the file first time for length, 
    # and then read it again for use
    row_count = -1
    with open('client_tasklist.csv','r',newline='') as csvfile:
        row_counter = csv.reader(csvfile, delimiter = ',', quotechar='"')
        # row_count = len(list(reader))
        row_count = sum(1 for row in row_counter)
        # print(row_count)
    # Return a random row in the tasklist
    with open('client_tasklist.csv','r',newline='') as csvfile:
        client_tasklist = csv.reader(csvfile,delimiter = ',', quotechar='"')
        task_list = []
        random_row = random.randint(1,row_count) # 1 <= n <= row_count
        # print(random_row)
        for i in range(random_row-1):
            next(client_tasklist)
        row = next(client_tasklist)
        # print(row)
        for num in row:
            task_list.append(int(num))
        # print(task_list)
    return task_list

# Return a list of words in JSON format
@app.route('/randomStim/<numberOfWords>')
def randomStim(numberOfWords):
    try:
        random_words = random.sample(words, int(numberOfWords))
        return json.dumps(random_words)
    except ValueError:
        print('numberOfWords is too big!')

@app.route('/getStim/<target_1_fontsize>/<target_1_length>/<target_2_fontsize>/<target_2_length>')
def getStim(target_1_fontsize,target_1_length,target_2_fontsize,target_2_length, word = config.word): # word = config.experiment
    if word == 'pseudoword':
        # Generate n pseudoword
        # target1 = config.target1, target2 = config.target2
        # print(type(task))
        # print(ast.literal_eval(task))
        # print(json.loads(task))
        return get_pseudo_stimuli(int(config.numberOfWords),{'length':int(target_1_length), 'fontsize':int(target_1_fontsize)}, {'length':int(target_2_length),'fontsize':int(target_2_fontsize)})
    if word == 'english':
        return get_english_stimuli(int(config.numberOfWords),{'length':int(target_1_length), 'fontsize':int(target_1_fontsize)}, {'length':int(target_2_length),'fontsize':int(target_2_fontsize)})

def get_pseudo_stimuli(numberOfWords, target1, target2):
    words = []
    target_words = []
    distractor_words = []

    target_word_1 = {'text': pseudoword(size = target1['length']), 'fontsize': target1['fontsize'], 'html': 'target'}
    target_word_2 = {'text': pseudoword(size = target2['length']), 'fontsize': target2['fontsize'], 'html': 'target'}
    target_words.append(target_word_1)
    target_words.append(target_word_2)

    for i in range(int(numberOfWords) - 2):
        distractor = {'text': pseudoword(size = random.randint(5,8)), 'fontsize': random.randint(20,24), 'html': 'distractor'}
        distractor_words.append(distractor)

    # print(target_words)
    # print(distractor_words)
    # print('combined: ', target_words + distractor_words)
    return json.dumps(target_words + distractor_words)

def pseudoword(size = 5, charset = "weruosazxcvnm"):
    return ''.join(random.choice(charset) for _ in range(size))

def get_english_stimuli(numberOfWords, target1, target2):
    # print(target1,target2)
    # print(target1['length'],target1['fontsize'])
    legit_words = get_legit_word(whole_word_list,5,8)
    # words = []
    target_words = []
    distractor_words = []

    # target_1_length = target1['length']
    # target_2_length = target2['length']

    target1_text = ''
    while True:
        target1_text = random.choice(legit_words)
        if(len(target1_text) == target1['length']):
            legit_words.remove(target1_text)
            break
    
    target2_text = ''
    while True:
        target2_text = random.choice(legit_words)
        if(len(target2_text) == target2['length']):
            legit_words.remove(target2_text)
            break
    # print(target1)
    # print(target2)
    target_word_1 = {'text': target1_text, 'fontsize': target1['fontsize'], 'html': 'target'}
    target_word_2 = {'text': target2_text, 'fontsize': target2['fontsize'], 'html': 'target'}
    target_words.append(target_word_1)
    target_words.append(target_word_2)

    for i in range(int(numberOfWords) - 2):
        distractor = {'text': random.choice(legit_words), 'fontsize': random.randint(20,24), 'html': 'distractor'}
        distractor_words.append(distractor)

    return json.dumps(target_words + distractor_words)

@app.route('/randomStim/post_data', methods = ['POST'])
def post_data():
    data = flask.request.form
    turker_id = data["turker_id"]
    clickedword = data["word"]
    word_x = data["word position[left]"]
    word_y = data["word position[top]"]
    target_distance = data['targets distance']
    correct_word = data['correct word']
    cloud_width = data["container size[width]"]
    cloud_height = data["container size[height]"]
    num_of_Stim = data["number of Stim"]
    span_tags = data["cloud"]

    # print('clicked word: ' + clickedword, word_x, word_y)
    # print('cloud information: ' + span_tags)
    with open('client_data.csv','a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',', quotechar='"')
        # writer.writerow(['turker_id','clickedword', 'word_x', 'word_y', 'target_distance', 'correct_word', 'cloud_width', 'cloud_height', 'num_of_Stim', 'span_tags'])
        writer.writerow([turker_id,clickedword, word_x, word_y, target_distance, correct_word, cloud_width, cloud_height, num_of_Stim, span_tags])
    return json.dumps(data)


def check_hashcode(hashcode):
    with open('client_id.csv','r',newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar='"')
        for row in reader:
            if str(hashcode) == row[1]:
                return True
    return False

whole_word_list = []
def load_all_word():
    with open('COCA_UNQ.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            whole_word_list.append(row[0])
    return whole_word_list
whole_word_list = load_all_word()

def get_legit_word(wordlist,minLen,maxLen):
    legit_word_list = []
    adescenders = r"qtyiplkjhgfdb"
    for word in wordlist:
        if not any(char in word for char in adescenders):
            if not (len(word) < minLen or len(word) > maxLen):
                legit_word_list.append(word)
    return legit_word_list




if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: {0} host port'.format(sys.argv[0]))
		print('  Example: {0} allen.mathcs.carleton.edu xxxx'.format(sys.argv[0]))
		exit()
	
	host = sys.argv[1]
	port = int(sys.argv[2])
	app.run(host=host, port=port, debug=True)