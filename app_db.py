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
from Configures import tasklist_config as config
# import config
import numpy
import psycopg2
from psycopg2 import sql
import math
from datetime import datetime

from Configures import dbconfig_e3 as dbconfig
turker_database = dbconfig.turker_db
opposite_on_circle_database = dbconfig.results_db
demographics_database = dbconfig.dem_db

app = flask.Flask(__name__)
fujs = FlaskUtilJs(app)

# ll_e1_turker_db = 'll_e1_turkers'
#
# ll_e1n_turker_db = 'll_e1n_turkers'
# ll_e1n_results_db = 'll_e1n_results'
# ll_e1n_dem_db = 'll_e1n_dem'

pilot_gits_turker_db = 'gist_turkers'
single_circle_database = 'pilot_single_circle'

# turker_database = ll_e1n_turker_db
# opposite_on_circle_database = ll_e1n_results_db
# demographics_database = ll_e1n_dem_db

#turker_database = 'll_e1_turkers'
#opposite_on_circle_database = 'll_e1_results'

#multiple_circle_database = 'pilot_multiple_circles'
#demographics_database = 'll_e1_dem'

def get_connection():
	'''
	Returns a connection to the database described
	in the config module. Returns None if the
	connection attempt fails.
	'''
	connection = None
	try:
		connection = psycopg2.connect(host='localhost',
                                      database='fontsize',
									  user='fontsize',
									  password='wordcloudsbad?')
	except Exception as e:
		print(e, file=sys.stderr)
	return connection



# Get and render web pages
##########################################################################################################################################################################################################################
@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def get_hello_page():
	return flask.redirect(flask.url_for('get_landing_page',exp='1'))

@app.route('/word_cognition_study/<exp>')
def get_landing_page(exp):
    if exp == '1':
        experiment = 'opposite_on_circle'
    elif exp == '2':
        experiment = 'single_circle'
    elif exp == '3':
        experiment = 'multiple_circles'
    elif exp == '1n':
        experiment = 'opposite_on_circle_no_flash'
    elif exp == 'gist':
        experiment = 'gist'
    elif exp == 'c':
        experiment = 'color_flash'
    elif exp == 'cn':
        experiment = 'color_no_flash'
    elif exp == 'e3_f':
        experiment = 'e3_font'
    elif exp == 'e3_c':
        experiment = 'e3_color'
    elif exp == 'e3n_f':
        experiment = 'e3n_font'
    elif exp == 'e3n_c':
        experiment = 'e3n_color'
    return flask.render_template('landing.html',Experiment = experiment)

# Get the description page, with turker_id as the data passed from HTML form from landing page
@app.route('/word_cognition_study/description', methods = ['POST'])
def get_description():
    turker_id = flask.request.form['turker_id']
    experiment = flask.request.form['experiment']
    # if experiment == 'opposite_on_circle':
    #     template = 'experiment_opposite_on_circle.html'
    # elif experiment == 'single_circle':
    #     template = 'experiment_single_circle.html'
    # elif experiment == 'multiple_circles':
    #     template = 'experiment_multiple_circles.html'
    # elif experiment == "opposite_on_circle_no_flash":
    #     template = 'experiment_opposite_on_circle.html'
    # else:
    #     template = 'experiment_opposite_on_circle.html'

    template = 'description_' + experiment + '.html'
    if not app.debug and experiment != 'gist':
        connection = get_connection()
        cursor = connection.cursor()
        participant = 'new'
        cursor.execute(sql.SQL("SELECT turker_id FROM {} WHERE turker_id = %s").format(sql.Identifier(turker_database)),(turker_id,))
        if len(cursor.fetchall()) > 1:
            participant = 'tested'
        else:
            participant = 'new'
        # cursor.execute("SELECT EXISTS(SELECT turker_id FROM pilot_opposite_on_circle WHERE turker_id = %s)",(turker_id,))
        # existance = cursor.fetchone()[0]
        # if existance == True:
        #     participant = 'tested'
        # else:
        #     cursor.execute("SELECT EXISTS(SELECT turker_id FROM pilot_multi_targets WHERE turker_id = %s)",(turker_id,))
        #     existance = cursor.fetchone()[0]
        #     if existance == True:
        #         participant = 'tested'
        #     else:
        #         cursor.execute("SELECT EXISTS(SELECT turker_id FROM pilot_multi_rings WHERE turker_id = %s)",(turker_id,))
        #         existance = cursor.fetchone()[0]
        #         if existance == True:
        #             participant = 'tested'

        # print(existance,type(existance))
        connection.commit()
        cursor.close()
        connection.close()
    else: #piloting for gist experiment
        participant = 'new'
    
    if turker_id == 'superman':
        participant = 'new'
    return flask.render_template(template, ID = turker_id, Participant = participant)

# Get the description page; turker_id is passed from description page through HTML form
@app.route('/word_cognition_study/stimuli', methods = ['POST'])
def get_stimuli_page():
    turker_id = flask.request.form['turker_id']
    experiment = flask.request.form['experiment']
    print(experiment)
    return flask.render_template('stimuli.html', ID = turker_id, List_From_Server=get_tasklist(experiment))

@app.route('/word_cognition_study/stimuli_gist',methods=['POST'])
def get_stimuli_gist_page():
    turker_id = flask.request.form['turker_id']
    experiment = flask.request.form['experiment']
    print(experiment)
    return flask.render_template('stimuli_gist.html', ID = turker_id, List_From_Server=get_tasklist(experiment))

@app.route('/word_cognition_study/completion', methods=['POST'])
def get_completion():
    data = flask.request.form
    turker_id = data['turker_id']
    hash_code = hash(data['turker_id'] + 'Carleton')
    # print(hash_code,type(hash_code))
    return flask.render_template('completion.html', ID = turker_id, Hash_Code = hash_code)

@app.route('/word_cognition_study/completion_gist', methods=['POST'])
def get_completion_gist():
    data = flask.request.form
    turker_id = data['turker_id']
    hash_code = hash(data['turker_id'] + 'Carleton')
    # print(hash_code,type(hash_code))
    return flask.render_template('completion_gist.html', ID = turker_id, Hash_Code = hash_code)
##########################################################################################################################################################################################################################




# Send information from server py to frontend JS
##########################################################################################################################################################################################################################
# Get the tasklist from test_length_config.py, the tasklist is from test_length.csv
# The format of the tasklist is 
# [{'small_fontsize':int,'smallword_length':int,'big_fontsize':int,'bigword_length':int},{},{},...]
def get_tasklist(experiment):
    # if experiment == "opposite_on_circle":
    #     tasklist = config.loadTask(config.tasklist_opposite_on_circle)
    # elif experiment == "single_circle":
    #     tasklist = config.loadTask(config.tasklist_single_circle)
    # elif experiment == "multiple_circles":
    #     tasklist = config.loadTask(config.tasklist_multiple_circles)
    # elif experiment == "opposite_on_circle_no_flash":
    #     tasklist = config.loadTask(config.tasklist_opposite_on_circle_no_flash)
    return config.loadTask(config.tasklist_path(experiment))

# This getStim is used for generating the words for experiment "opposite_on_circle". 
# num_of_distractor + 2 makes a total number of 202 words.
# the first two of those words are targets, and the 200 rest are distractors
@app.route('/_getStim/<small_fontsize>/<smallword_length>/<big_fontsize>/<bigword_length>')
def getStim(small_fontsize,smallword_length,big_fontsize,bigword_length, word = config.word): # word = config.experiment
    if word == 'pseudoword':
        return get_pseudo_stimuli(int(config.num_of_distractor)+2,{'length':int(smallword_length), 'fontsize':int(small_fontsize)}, {'length':int(bigword_length),'fontsize':int(big_fontsize)})
    if word == 'english':
        return get_english_stimuli(int(config.num_of_distractor)+2,{'length':int(smallword_length), 'fontsize':int(small_fontsize)}, {'length':int(bigword_length),'fontsize':int(big_fontsize)})

# No adescenders, pseudoword
def pseudoword(size = 5, charset = "weruosazxcvnm"):
    return ''.join(random.choice(charset) for _ in range(size))
def get_pseudo_stimuli(num_of_distractor, target1, target2):
    words = []
    target_words = []
    distractor_words = []

    target_word_1 = {'text': pseudoword(size = target1['length']), 'fontsize': target1['fontsize'], 'html': 'target'}
    target_word_2 = {'text': pseudoword(size = target2['length']), 'fontsize': target2['fontsize'], 'html': 'target'}
    target_words.append(target_word_1)
    target_words.append(target_word_2)

    for i in range(int(num_of_distractor) - 2):
        distractor = {'text': pseudoword(size = random.randint(config.minLen,config.maxLen)), 'fontsize': random.randint(config.minSize,config.maxSize), 'html': 'distractor'}
        distractor_words.append(distractor)

    return json.dumps(target_words + distractor_words)

# No adescenders, english words
def get_legit_word(wordlist,minLen,maxLen):
    legit_word_list = []
    adescenders = r"qtyiplkjhgfdb"
    for word in wordlist:
        if not any(char in word for char in adescenders):
            if not (len(word) < minLen or len(word) > maxLen):
                legit_word_list.append(word)
    return legit_word_list
def get_english_stimuli(num_of_distractor, target1, target2):
    legit_words = get_legit_word(decent_word_list,config.minLen,config.maxLen)
    target_words = []
    distractor_words = []

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

    target_word_1 = {'text': target1_text, 'fontsize': target1['fontsize'], 'html': 'target'}
    target_word_2 = {'text': target2_text, 'fontsize': target2['fontsize'], 'html': 'target'}
    target_words.append(target_word_1)
    target_words.append(target_word_2)

    for i in range(int(num_of_distractor) - 2):
        distractor = {'text': random.choice(legit_words), 'fontsize': random.randint(config.minSize,config.maxSize), 'html': 'distractor'}
        distractor_words.append(distractor)

    return json.dumps(target_words + distractor_words)

# Get n target words from this topic
# Used for gist-forming
@app.route('/_getTopicTargets/<number_of_targets>/<correct_fontsize>/<wrong_fontsize>')
def getTopicTargets(number_of_targets,correct_fontsize,wrong_fontsize):
    category_words = {'animal':['meow','purr','milk','yarn','whiskers'],
                        'food':['cake','coffee','sushi','burger','salad'],
                        'beach':['sand','waves','swimsuit','sunscreen','shell'],
                        'coffee':['starbucks','drink','cafe','latte','cappucino'],
                        'chicken':['kentucky','fried','bird','eat','meat'],
                        'banana':['monkey','fruit','yellow','curved','tropical']}
    # legit_words = get_legit_word(decent_word_list,int(word_length),int(word_length))
    target_words = []
    topic = random.choice(list(category_words))
    target_words = category_words[topic]

    for i in range(int(number_of_targets)):
        target_words[i] = {'text': target_words[i], 'fontsize': 22, 'html': topic}
    
    # for i in range(int(number_of_targets)):
    #     correct_target = random.choice(legit_words)
    #     legit_words.remove(correct_target)
    #     target_words.append(correct_target)

    # for i in range(int(number_of_targets)):
    #     if i == 0:
    #         target_words[i] = {'text': target_words[i], 'fontsize': correct_fontsize, 'html': 'target'}
    #     else:
    #         target_words[i] = {'text': target_words[i], 'fontsize': wrong_fontsize, 'html': 'target'}
    # print("the targets are: ", target_words)
    return json.dumps(target_words)

# Used for fetching words for the gist experiment
@app.route('/_getTopicWords/<topic_num>/<size1mean>/<size1sd>/<dist1mean>/<dist1sd>/<n1>/<size2mean>/<size2sd>/<dist2mean>/<dist2sd>/<n2>')
def getTopicWords(topic_num,size1mean,size1sd,dist1mean,dist1sd,n1,size2mean,size2sd,dist2mean,dist2sd,n2):
    with open('dict.json') as json_file:
        Topic_Words = json.load(json_file)
    # topic1 = ''
    # topic2 = ''
    # topic_distractor = ''
    topics = []
    word_list = []
    num_words = [int(n1),int(n2)]
    size_means = [int(size1mean),int(size2mean)]
    size_sds = [int(size1sd),int(size2sd)]
    dist_means = [int(dist1mean),int(dist2mean)]
    dist_sds = [int(dist1sd),int(dist2sd)]
    for i in range(int(topic_num)): # For each topic, fetch n_i words from that topic
        topic = random.choice(list(Topic_Words))
        topics.append(topic) # Push topic1 and topic2 in order
        for _ in range(num_words[i]):
            text = random.choice(Topic_Words[topic])
            if len(Topic_Words[topic]) > 1:
                Topic_Words[topic].remove(text)
            fontsize = int(numpy.random.normal(size_means[i],size_sds[i]))
            dist = int(numpy.random.normal(dist_means[i],dist_sds[i]))
            word = {'text':text,'fontsize':fontsize,'dist':dist,'topic':topic,'html':'target '+topic}
            word_list.append(word)
        del Topic_Words[topic]
    topics.append(random.choice(list(Topic_Words))) # Push a third topic_distractor
    return json.dumps({'topics':topics,'word_list':word_list})

# Used for hypo2
# Specifications about the length of targets, fontsize of the correct and wrong, and the number of words
# are passed from the frontend to the server
# the specifications from the frontend are from tasklist.csv (test_length.csv)
@app.route('/_getMultiTargets/<number_of_targets>/<correct_fontsize>/<wrong_fontsize>/<word_length>')
def getMultiTargets(number_of_targets,correct_fontsize,wrong_fontsize,word_length):
    legit_words = get_legit_word(decent_word_list,int(word_length),int(word_length))
    target_words = []
    for i in range(int(number_of_targets)):
        correct_target = random.choice(legit_words)
        legit_words.remove(correct_target)
        target_words.append(correct_target)
    
    for i in range(int(number_of_targets)):
        if i == 0:
            target_words[i] = {'text': target_words[i], 'fontsize': correct_fontsize, 'html': 'target'}
        else:
            target_words[i] = {'text': target_words[i], 'fontsize': wrong_fontsize, 'html': 'target'}
    # print("the targets are: ", target_words)
    return json.dumps(target_words)

# Used for hypo2
# Specifications about word length, fontsize, and number of distractors
# are found in the config file
# no parameters are needed from the frontend
# return a list of words in dictionary to the front end
@app.route('/_getDistractors')
def getDistractors():
    legit_words = get_legit_word(decent_word_list,config.minLen,config.maxLen)
    distractor_words = []
    for i in range(int(config.num_of_distractor)):
        distractor = {'text': random.choice(legit_words), 'fontsize': random.randint(config.minSize,config.maxSize), 'html': 'distractor'}
        distractor_words.append(distractor)
    return json.dumps(distractor_words)
##########################################################################################################################################################################################################################




# Write data to csvfile/database
##########################################################################################################################################################################################################################
# Write the turker's id into a csvfile --> client_id.csv
@app.route('/_turker_id/<experiment>', methods = ['POST'])
def receive_id(experiment):
    data = flask.request.form
    turker_id = data["turker_id"]
    hashcode = hash(turker_id+'Carleton')
    if not app.debug and experiment != 'gist':
        connection = get_connection()
        cursor = connection.cursor()
        # cursor.execute("SELECT turker_id FROM turker WHERE turker_id = %s",(turker_id,))
        # if len(cursor.fetchall()) == 0:
        cursor.execute(sql.SQL("INSERT INTO {} (turker_id,hashcode) VALUES (%s, %s)").format(sql.Identifier(turker_database)),(turker_id,hashcode))
        connection.commit()
        cursor.close()
        connection.close()
    # with open('pilot_client_id.csv','a', newline='') as csvfile:
    #     writer = csv.writer(csvfile, delimiter = ',', quotechar='"')
    #     # hashcode = hash(turker_id+'Carleton')
    #     writer.writerow([turker_id,hashcode])
    return json.dumps({'id':turker_id,'hashcode':hashcode})

# Post stimuli data
@app.route('/_post_data', methods = ['POST'])
def post_data():
    data = json.loads(flask.request.data)

    turker_id = data["turker_id"] #0 TEXT

    cloud_width = int(data["cloud_width"]) #1 INTEGER
    cloud_height = int(data["cloud_height"]) #2 INTEGER
    cloud_center_x = int(data["cloud_center_x"]) #3 INTEGER
    cloud_center_y = int(data["cloud_center_y"]) #4 INTEGER

    clicked_word = data["clicked_word"] #5 TEXT
    correct_word = data["correct_word"] #6 TEXT
    wrong_word = data["wrong_word"] #7 TEXT
    #distance_between_targets = myround(float(data["distance_between_targets"]),100) #8 INTEGER
    distance_between_targets = float(data["distance_between_targets"]) # For ll_e3n, stopped rounding
    # Rounded distance can be found in attribute d
    d = data["d"]
    timeTaken = float(data["time"]) #9 REAL

    correct_word_x = float(data["correct_word_x"]) #10 REAL
    correct_word_y = float(data["correct_word_y"]) #11 REAL
    correct_word_fontsize = int(data["correct_word_fontsize"]) #12 INTEGER
    correct_word_width = float(data["correct_word_width"]) #13 REAL
    correct_word_height = int(data["correct_word_height"]) #14 INTEGER
    correct_word_center_distance = myround(float(data["correct_word_center_distance"]),50) #15 INTEGER

    wrong_word_x = float(data["wrong_word_x"]) #16 REAL
    wrong_word_y = float(data["wrong_word_y"]) #17 REAL
    wrong_word_fontsize = int(data["wrong_word_fontsize"]) #18 INTEGER
    wrong_word_width = float(data["wrong_word_width"]) #19 REAL
    wrong_word_height = int(data["wrong_word_height"]) #20 INTEGER
    wrong_word_center_distance = myround(float(data["wrong_word_center_distance"]),50) #21 INTEGER

    number_of_words = int(data["number_of_words"]) #22 INTEGER
    span_content = data["span_content"] #23 TEXT

    question_index = int(data["question_index"]) #24 INTEGER

    flash_time = int(data["flash_time"]) # 25 INTEGER

    time_stamp = str(datetime.utcnow()) # 26 TEXT

    # Added color values
    correct_word_lightness = int(data["correct_word_lightness"])
    wrong_word_lightness = int(data["wrong_word_lightness"])
    lightnessDiff = wrong_word_lightness - correct_word_lightness # Darker word is correct, and has lower lightness value

    # Encoding just passed through
    encoding = data['encoding']
    agreement = data['agreement']

    # The below values are calculated
    sizeDiff = correct_word_fontsize - wrong_word_fontsize
    accuracy = 1 if clicked_word == correct_word else 0


    clicked_x = correct_word_x if accuracy == 1 else wrong_word_x
    clicked_y = correct_word_y if accuracy == 1 else wrong_word_y
    clicked_word_width = correct_word_width if accuracy == 1 else wrong_word_width
    clicked_word_height = correct_word_height if accuracy == 1 else wrong_word_height

    angle = clicked_x/clicked_y
    try:
        block_width = data["block_width"]
        block_height = data["block_height"]
        index_of_difficulty = math.log2(distance_between_targets/get_hypotenuse(angle,block_height,block_width))
    except KeyError:
        block_width = -1
        block_height = -1
        index_of_difficulty = math.log2(distance_between_targets/get_hypotenuse(angle,clicked_word_height,clicked_word_width))
    index_of_performance = index_of_difficulty/timeTaken

    if not app.debug:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql.SQL("""
                INSERT INTO {} (turker_id,cloud_width,cloud_height,cloud_center_x,cloud_center_y,
                clicked_word,correct_word,wrong_word,distance_between_targets,time,
                correct_word_x,correct_word_y,correct_word_fontsize,correct_word_width,correct_word_height,correct_word_center_distance,
                wrong_word_x,wrong_word_y,wrong_word_fontsize,wrong_word_width,wrong_word_height,wrong_word_center_distance,
                number_of_words,span_content,question_index,
                sizeDiff,accuracy,clicked_x,clicked_y,angle,index_of_difficulty,index_of_performance,flash_time,time_stamp,correct_word_lightness,wrong_word_lightness,lightnessDiff,encoding,agreement,d)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """).format(sql.Identifier(opposite_on_circle_database)),
                (turker_id,cloud_width,cloud_height,cloud_center_x,cloud_center_y,
                clicked_word,correct_word,wrong_word,distance_between_targets,timeTaken,
                correct_word_x,correct_word_y,correct_word_fontsize,correct_word_width,correct_word_height,correct_word_center_distance,
                wrong_word_x,wrong_word_y,wrong_word_fontsize,wrong_word_width,wrong_word_height,wrong_word_center_distance,
                number_of_words,span_content,question_index,
                sizeDiff,accuracy,clicked_x,clicked_y,angle,index_of_difficulty,index_of_performance,flash_time,time_stamp,correct_word_lightness,wrong_word_lightness,lightnessDiff,encoding,agreement,d))
        connection.commit()
        cursor.close()
        connection.close()

    return json.dumps([turker_id,clicked_word,timeTaken,sizeDiff,accuracy,angle,index_of_difficulty,flash_time])

# Post hypo2 stimuli data
@app.route('/_post_data_multi',methods=['POST'])
def post_data_multi():
    data = json.loads(flask.request.data)

    turker_id = data["turker_id"] #0
    cloud_width = int(data["cloud_width"]) #1
    cloud_height = int(data["cloud_height"]) #2
    cloud_center_x = int(data["cloud_center_x"]) #3
    cloud_center_y = int(data["cloud_center_y"]) #4

    clicked_word = data["clicked_word"] #5
    timeTaken = float(data["time"]) #6
    clicked_word_x = float(data["clicked_word_x"]) #7
    clicked_word_y = float(data["clicked_word_y"]) #8
    clicked_word_center_distance = myround(data["clicked_word_center_distance"],50) #9

    clicked_word_fontsize = int(data["clicked_word_fontsize"]) #10
    correct_fontsize = int(data["correct_fontsize"]) #11
    wrong_fontsize = int(data["wrong_fontsize"]) #12

    num_words_in_ring0 = int(data["num_words_in_ring0"]) #13
    num_words_in_ring1 = int(data["num_words_in_ring1"]) #14
    num_words_in_ring2 = int(data["num_words_in_ring2"]) #15
    number_of_targets = int(data["number_of_targets"]) #16
    number_of_words = int(data["number_of_words"]) #17
    span_content = data["span_content"] #18

    question_index = int(data["question_index"]) #19

    flash_time = int(data["flash_time"]) # 25 integer

    time_stamp = str(datetime.utcnow()) # 26 TEXT

    sizeDiff = correct_fontsize - wrong_fontsize #20
    accuracy = 1 if clicked_word_fontsize == correct_fontsize else 0 #21
    angle = clicked_word_x/clicked_word_y #22

    clicked_word_width = float(data["clicked_word_width"])
    clicked_word_height = float(data["clicked_word_height"])

    try:
        block_width = data["block_width"]
        block_height = data["block_height"]
        index_of_difficulty = math.log2(2*clicked_word_center_distance/get_hypotenuse(angle,block_height,block_width)) #23
    except KeyError:
        block_width = -1
        block_height = -1
        index_of_difficulty = math.log2(2*clicked_word_center_distance/get_hypotenuse(angle,clicked_word_height,clicked_word_height))
    index_of_performance = index_of_difficulty/timeTaken #24

    if not app.debug:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql.SQL("""
                INSERT INTO %s (turker_id,cloud_width,cloud_height,cloud_center_x,cloud_center_y,
                clicked_word,time,clicked_word_x,clicked_word_y,clicked_word_center_distance,clicked_word_fontsize,correct_fontsize,wrong_fontsize,
                num_words_in_ring0,num_words_in_ring1,num_words_in_ring2,number_of_targets,number_of_words,span_content,
                question_index,sizeDiff,accuracy,angle,index_of_difficulty,index_of_performance,flash_time,time_stamp)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """).format(sql.Identifier(single_circle_database)),
                (turker_id,cloud_width,cloud_height,cloud_center_x,cloud_center_y,
                clicked_word,timeTaken,clicked_word_x,clicked_word_y,clicked_word_center_distance,clicked_word_fontsize,correct_fontsize,wrong_fontsize,
                num_words_in_ring0,num_words_in_ring1,num_words_in_ring2,number_of_targets,number_of_words,span_content,
                question_index,sizeDiff,accuracy,angle,index_of_difficulty,index_of_performance,flash_time,time_stamp))
        connection.commit()
        cursor.close()
        connection.close()

    return json.dumps([turker_id,
                        clicked_word,timeTaken,clicked_word_x,clicked_word_y,clicked_word_center_distance,
                        clicked_word_fontsize,correct_fontsize,wrong_fontsize,
                        num_words_in_ring0,num_words_in_ring1,num_words_in_ring2,number_of_targets,number_of_words,
                        sizeDiff,accuracy,angle,index_of_difficulty,flash_time,time_stamp])

# Posting topic data to csv
@app.route('/_postTopicMeasurements',methods=['POST'])
def post_topic_measurements():
    json_data=json.loads(flask.request.data)
    method,data,cloud,time,response,wordcloud_name = json_data["method"],json_data["arr"],json_data["cloud"],json_data["time"],json_data["response"],json_data["wordcloud_name"]
    #data is a list, [[{topic:1}],[{topic:2}]]
    topic_list = []
    mean_dist = []
    sd_dist = []
    mean_size = []
    sd_size = []
    num = []
    for topic in data: # data = [[topic1],[topic2]]
        dist_list = []
        size_list = []
        for word in topic: # topic = [{"topic":topic,"size":size,"center_dist":center_dist,"x_dist":x_dist,"y_dist":y_dist,"word":word},...]
            dist_list.append(word["center_dist"])
            size_list.append(word["size"])
        topic_list.append(topic[0]["topic"])
        mean_dist.append(numpy.mean(dist_list))
        sd_dist.append(numpy.std(dist_list))
        mean_size.append(numpy.mean(size_list))
        sd_size.append(numpy.mean(size_list))
        num.append(len(dist_list))
    # print((topic_list,mean_dist,sd_dist,mean_size,sd_size,num))
    # write_dist(mean_dist+sd_dist+num)
    topic_list.append(json_data["distractor"])
    print(method)
    write_measure(method,topic_list+mean_dist+mean_size+response+[wordcloud_name]+sd_dist+sd_size+num+[time],cloud)
    return json.dumps("lol")

# Post demographic data
@app.route('/_post_demographic_data', methods=['POST'])
def post_demographic_data():
    data = json.loads(flask.request.data)
    turker_id = data["turker_id"]
    age = data["age"]
    gender = data["gender"]
    hand = data["hand"]
    education = data["education"]
    device = data["device"]
    browser = data["browser"]
    game = data["game"]
    difficulty = data["difficulty"]
    confidence = data["confidence"]
    eyetrace = data["eyetrace"]
    comments = data["comments"]

    if not app.debug:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql.SQL("""
                INSERT INTO {} (turker_id,age,gender,hand,education,device,browser,game,difficulty,confidence,eyetrace,comments)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """).format(sql.Identifier(demographics_database)),
                (turker_id,age,gender,hand,education,device,browser,game,difficulty,confidence,eyetrace,comments))
        connection.commit()
        cursor.close()
        connection.close()

    # with open('pilot_demographic_data.csv','a',newline='') as csvfile:
    #     writer = csv.writer(csvfile,delimiter = ',',quotechar='"')
    #     # writer.writerow(['tuerker_id','age','gender','hand','difficulty','confidence','eyetrace'])
    #     writer.writerow([turker_id,age,gender,hand,difficulty,confidence,eyetrace])
    return json.dumps("success saving data")
##########################################################################################################################################################################################################################

# Some helper method for recording gist data
def write_dist(dist):
    with open('spiral_dist.csv','a',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',',quotechar='"')
        writer.writerow(dist)

def write_measure(method,measurements,cloud):
    measurement_file = method+'.csv'
    with open(measurement_file,'a',newline='') as m_csvfile:
        writer = csv.writer(m_csvfile,delimiter=',',quotechar='"')
        writer.writerow(measurements)
    cloud_file = method+'_cloud.csv'
    # print(cloud)
    with open(cloud_file,'a',newline='',encoding="utf-8") as c_csvfile:
        writer = csv.writer(c_csvfile,delimiter=',',quotechar='"')
        writer.writerow([cloud]) #It expects a sequence (eg: a list or tuple) of strings. You're giving it a single string. A string happens to be a sequence of strings too, but it's a sequence of 1 character strings, which isn't what you want.

whole_word_list = []
def load_all_word():
    with open('COCA_UNQ.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            whole_word_list.append(row[0])
    return whole_word_list
print('Loading words...')
whole_word_list = load_all_word()
print('All words loaded, checking for indecent words...')

blacklist = ['ace', 'acerous', 'acers', 'aces', 'acne', 'acnes', 'acorn', 'acorns', 'acre', 'acres', 'aeons', 'anus', 'arc', 'arcs', 'are', 'ares', 'arose', 'arouse', 'ars', 'arson', 'aver', 'axe', 'axes', 'axon', 'axons', 'azure', 'azures', 'can', 'cane', 'caner', 'caners', 'canes', 'canoe', 'canoer', 'canoes', 'cans', 'car', 'care', 'cares', 'carouse', 'cars', 'carve', 'carves', 'case', 'cause', 'causer', 'cave', 'caver', 'cavern', 'cavernous', 'caverns', 'cavers', 'caves', 'censor', 'coarse', 'coarsen', 'coax', 'coaxer', 'coaxes', 'con', 'cone', 'cones', 'cons', 'convex', 'core', 'cores', 'corn', 'cornea', 'corneas', 'corns', 'course', 'cove', 'coven', 'covens', 'cover', 'covers', 'coves', 'crane', 'cranes', 'crave', 'craves', 'craze', 'crazes', 'crone', 'crones', 'crux', 'cruxes', 'cue', 'cues', 'cur', 'cure', 'cures', 'curs', 'curse', 'curve', 'curves', 'czar', 'czars', 'ear', 'earn', 'earns', 'ears', 'ecru', 'ecrus', 'ens', 'eon', 'eons', 'era', 'eras', 'eros', 'euro', 'euros', 'exon', 'exons', 'nares', 'nave', 'naves', 'near', 'nears', 'nervous', 'nevus', 'nexus', 'nor', 'norse', 'nos', 'nose', 'nova', 'novae', 'novas', 'nurse', 'nus', 'oar', 'oars', 'ocean', 'oceans', 'once', 'one', 'ones', 'onus', 'orca', 'ore', 'ores', 'ors', 'ounce', 'ounces', 'our', 'ours', 'ova', 'oven', 'ovens', 'over', 'overs', 'oxane', 'oxen', 'oxens', 'oxes', 'race', 'races', 'ran', 'rave', 'raven', 'ravenous', 'ravens', 'raves', 'raze', 'razes', 'reason', 'recon', 'rescan', 'rev', 'revs', 'roan', 'roans', 'roe', 'roes', 'rose', 'roue', 'roues', 'rouse', 'rove', 'roves', 'rue', 'rues', 'run', 'rune', 'runes', 'runs', 'ruse', 'sac', 'sane', 'saner', 'sauce', 'saucer', 'save', 'saver', 'savor', 'savour', 'sax', 'scan', 'scar', 'scare', 'scone', 'score', 'scorn', 'scour', 'sea', 'sear', 'senor', 'senora', 'sera', 'sex', 'snare', 'snore', 'soar', 'son', 'sonar', 'sore', 'sour', 'source', 'sox', 'suave', 'suaver', 'sue', 'suer', 'sun', 'sure', 'uncase', 'uncover', 'uncovers', 'unsex', 'urea', 'urn', 'urns', 'use', 'user', 'uvea', 'van', 'vane', 'vanes', 'vans', 'vase', 'vear', 'vears', 'venous', 'venus', 'vex', 'xerus', 'zas', 'zax', 'zaxes', 'zen', 'zens', 'zero', 'zeros', 'zoa', 'zoea', 'zoeas', 'zone', 'zoner', 'zoners', 'zones', 'zorse', 'zouave', 'zouaves']
naughtyList = ['anal', 'anus', 'arrse', 'arse', 'ass', 'asses','assfucker', 'assfukka', 'asshole', 'assholes', 'asswhole','b!tch', 'b00bs','b17ch','b1tch','ballbag','balls','ballsack','bastard','beastial','beastiality','bellend','bestial','bestiality','biatch','bitch','bitcher','bitchers','bitches','bitchin','bitching','bloody','blow job','blowjob','blowjobs','boiolas','bollock','bollok','boner','boob','boobs','booobs','boooobs','booooobs','booooooobs','bras','breasts','buceta','bugger','bum','bunny fucker','butt','butthole','buttmuch','buttocks','buttplug','c0ck','c0cksucker','carpet muncher','cawk','chink','cipa','cl1t','clit','clitoris','clits','cnut','cock','cock-sucker','cockface','cockhead','cockmunch','cockmuncher','cocks','cocksuck','cocksucked','cocksucker','cocksucking','cocksucks','cocksuka','cocksukka','cok','cokmuncher','coksucka','coon','cox','cracker','crap','cum','cummer','cumming','cums','cumshot','cunilingus','cunillingus','cunnilingus','cunt','cuntlick','cuntlicker','cuntlicking','cunts','cyalis','cyberfuc','cyberfuck','cyberfucked','cyberfucker','cyberfuckers','cyberfucking','d1ck','damn','diarrhea','dick','dickhead','dike','dildo','dildos','dink','dinks','dirsa','dlck','dog-fucker','doggin','dogging','donkeyribber','doosh','duche','dyke','ejaculate','ejaculated','ejaculates','ejaculating','ejaculatings','ejaculation','ejakulate','f u c k','f u c k e r','f4nny','fag','fagging','faggitt','faggot','faggs','fagot','fagots','fags','fanny','fannyflaps','fannyfucker','fanyy','fatass','fcuk','fcuker','fcuking','feces','feck','fecker','felching','fellate','fellatio','fingerfuck','fingerfucked','fingerfucker','fingerfuckers','fingerfucking','fingerfucks','fistfuck','fistfucked','fistfucker','fistfuckers','fistfucking','fistfuckings','fistfucks','flange','fook','fooker','fuck','fucka','fucked','fucker','fuckers','fuckhead','fuckheads','fucking','fuckings','fuckingshitmotherfucker','fuckme','fucks','fuckwhit','fuckwit','fudge packer','fudgepacker','fuk','fuker','fukker','fukkin','fuks','fukwhit','fukwit','fux','fux0r','f_u_c_k','gangbang','gangbanged','gangbangs','gaylord','gaysex','goatse','God','god-dam','god-damned','goddamn','goddamned','hardcoresex','hell','heshe','hoar','hoare','hoer','homo','homosexual','homosexuals','hooker','hore','horniest','horny','hotsex','"jack-off','jackoff','jap','jerk-off','jism','jiz','jizm','jizz','kawk','knob','knobead','knobed','knobend','knobhead','knobjocky','knobjokey','kock','kondum','kondums','kum','kummer','kumming','kums','kunilingus','l3i+ch','l3itch','labia','lesbian','lesbians','lesbo','lmfao','lust','lusting','m0f0','m0fo','m45terbate','ma5terb8','ma5terbate','masochist','massacre','master-bate','masterb8','masterbat*','masterbat3','masterbate','masterbation','masterbations','masturbate','mo-fo','mof0','mofo','mothafuck','mothafucka','mothafuckas','mothafuckaz','mothafucked','mothafucker','mothafuckers','mothafuckin','mothafucking','mothafuckings','mothafucks','mother fucker','motherfuck','motherfucked','motherfucker','motherfuckers','motherfuckin','motherfucking','motherfuckings','motherfuckka','motherfucks','muff','mutha','muthafecker','muthafuckker','muther','mutherfucker','n1gga','n1gger','nazi','nigg3r','nigg4h','nigga','niggah','niggas','niggaz','nigger','niggers','nob','nob jokey','nobhead','nobjocky','nobjokey','numbnuts','nutsack','orgasim','orgasims','orgasm','orgasms','p0rn','pawn','pecker','penis','penisfucker','phonesex','phuck','phuk','phuked','phuking','phukked','phukking','phuks','phuq','pigfucker','pimpis','piss','pissed','pisser','pissers','pisses','pissflaps','pissin','pissing','pissoff','playboy','poop','porn','porno','pornography','pornos','prick','pricks','pron','pube','pusse','pussi','pussies','pussy','pussys','rape','raper','rapist','rectum','retard','rimjaw','rimming','s hit','s.o.b.','sadist','schlong','screwing','scroat','scrote','scrotum','semen','sensual','sensuous','sex','sexes','"sh!+"','"sh!t"','sh1t','shag','shagger','shaggin','shagging','shemale','"shi+"','shit','shitdick','shite','shited','shitey','shitfuck','shitfull','shithead','shiting','shitings','shits','shitted','shitter','"shitters "','shitting','shittings','"shitty "','skank','slut','sluts','smegma','smut','snatch','"son-of-a-bitch"','spac','spunk','s_h_i_t','t1tt1e5','t1tties','teets','teez','testical','testicle','tit','titfuck','tits','titt','tittie5','tittiefucker','titties','tittyfuck','tittywank','titwank','tosser','turd','tw4t','twat','twathead','twatty','twunt','twunter','urinary','urine','uterus','v14gra','v1gra','vagina','vaginal','viagra','vulva','w00se','wang','wank','wanker','wanky','weiner','whoar','whore','whores','willies','willy','xrated','xxx','FALSE','corpses','corpse','bodies','auschwitz']

decent_word_list = []
for word in whole_word_list:
    # if word in blacklist or word in naughtyList:
    #     print(word)
    if not word in blacklist and not word in naughtyList:
        decent_word_list.append(word)
print('Done.')


def check_hashcode(hashcode):
    with open('pilot_client_id.csv','r',newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar='"')
        for row in reader:
            if str(hashcode) == row[1]:
                return True
    return False 

def myround(x,base):
    return base * round(x/base)

def get_hypotenuse(angle,opposite=29,width=84.9844):
    angle = math.fabs(angle)
    adjacent = angle*opposite
    if adjacent > width:
        angle = 1/angle
        opposite = width
        adjacent = opposite*angle
    hypotenuse = math.sqrt(math.pow(opposite,2)+math.pow(adjacent,2))
    return hypotenuse

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: {0} host port'.format(sys.argv[0]))
		print('  Example: {0} allen.mathcs.carleton.edu xxxx'.format(sys.argv[0]))
		exit()
	
	host = sys.argv[1]
	port = int(sys.argv[2])
	app.run(host=host, port=port, debug=True)
