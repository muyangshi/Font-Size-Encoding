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
import psycopg2
import math

app = flask.Flask(__name__)
fujs = FlaskUtilJs(app)

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
    return flask.render_template('landing.html',Experiment = experiment)

# Get the description page, with turker_id as the data passed from HTML form from landing page
@app.route('/word_cognition_study/description', methods = ['POST'])
def get_description():
    turker_id = flask.request.form['turker_id']
    experiment = flask.request.form['experiment']
    if experiment == 'opposite_on_circle':
        template = 'experiment_1.html'
    elif experiment == 'single_circle':
        template = 'experiment_2.html'
    elif experiment == 'multiple_circles':
        template = 'experiment_3.html'
    else:
        template = 'experiment_1.html'
    participant = 'new'
    return flask.render_template(template, ID = turker_id, Participant = participant)

# Get the description page; turker_id is passed from description page through HTML form
@app.route('/word_cognition_study/stimuli', methods = ['POST'])
def get_stimuli_page():
    turker_id = flask.request.form['turker_id']
    experiment = flask.request.form['experiment']
    print(experiment)
    # print(turker_id)
    return flask.render_template('stimuli.html', ID = turker_id, List_From_Server=get_tasklist(experiment))

@app.route('/word_cognition_study/completion', methods=['POST'])
def get_completion():
    data = flask.request.form
    turker_id = data['turker_id']
    hash_code = hash(data['turker_id'] + 'Carleton')
    # print(hash_code,type(hash_code))
    return flask.render_template('completion.html', ID = turker_id, Hash_Code = hash_code)
##########################################################################################################################################################################################################################




# Send information from server py to frontend JS
##########################################################################################################################################################################################################################
# Get the tasklist from test_length_config.py, the tasklist is from test_length.csv
# The format of the tasklist is 
# [{'small_fontsize':int,'smallword_length':int,'big_fontsize':int,'bigword_length':int},{},{},...]
def get_tasklist(experiment):
    if experiment == "opposite_on_circle":
        tasklist = config.loadTask(config.tasklist_opposite_on_circle)
    elif experiment == "single_circle":
        tasklist = config.loadTask(config.tasklist_single_circle)
    elif experiment == "multiple_circles":
        tasklist = config.loadTask(config.tasklist_multiple_circles)
    return tasklist

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
    print("the targets are: ", target_words)
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
@app.route('/_turker_id', methods = ['POST'])
def receive_id():
    data = flask.request.form
    turker_id = data["turker_id"]
    hashcode = hash(turker_id+'Carleton')

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
    distance_between_targets = myround(float(data["distance_between_targets"]),100) #8 INTEGER
    time = float(data["time"]) #9 REAL

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
    index_of_performance = index_of_difficulty/time


    # with open('pilot_client_data.csv','a', newline='') as csvfile:
    #     writer = csv.writer(csvfile, delimiter = ',', quotechar='"')
    #     # writer.writerow(['turker_id',
    #     # 'cloud_width','cloud_height','cloud_center_x','cloud_center_y',
    #     # 'clicked_word','correct_word','wrong_word','distance_between_targets',
    #     # 'correct_word_x','correct_word_y','correct_word_fontsize','correct_word_width','correct_word_height','correct_word_center_distance',
    #     # 'wrong_word_x','wrong_word_y','wrong_word_fontsize','wrong_word_width','wrong_word_height','wrong_word_center_distance',
    #     # 'number_of_words','span_content'])
    #     writer.writerow([turker_id,cloud_width,cloud_height,cloud_center_x,cloud_center_y,clicked_word,correct_word,wrong_word,distance_between_targets,time,correct_word_x,correct_word_y,correct_word_fontsize,correct_word_width,correct_word_height,correct_word_center_distance,wrong_word_x,wrong_word_y,wrong_word_fontsize,wrong_word_width,wrong_word_height,wrong_word_center_distance,number_of_words,span_content])
    return json.dumps([turker_id,clicked_word,correct_word,wrong_word,time,sizeDiff,accuracy,angle,index_of_difficulty,flash_time])

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
    time = float(data["time"]) #6
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
    index_of_performance = index_of_difficulty/time #24

    # with open('hypo2_client_data.csv','a',newline='',encoding="utf-8") as csvfile:
    #     writer = csv.writer(csvfile,delimiter=',',quotechar='"')
    #     writer.writerow([turker_id,cloud_width,cloud_height,cloud_center_x,cloud_center_y,
    #     clicked_word,time,clicked_word_x,clicked_word_y,clicked_word_center_distance,clicked_word_fontsize,
    #     correct_fontsize,wrong_fontsize,
    #     num_words_in_ring0,num_words_in_ring1,num_words_in_ring2,number_of_targets,number_of_words,
    #     span_content])
    return json.dumps([turker_id,
                        clicked_word,time,clicked_word_x,clicked_word_y,clicked_word_center_distance,
                        clicked_word_fontsize,correct_fontsize,wrong_fontsize,
                        num_words_in_ring0,num_words_in_ring1,num_words_in_ring2,number_of_targets,number_of_words,
                        sizeDiff,accuracy,angle,index_of_difficulty,flash_time])


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

    # with open('pilot_demographic_data.csv','a',newline='') as csvfile:
    #     writer = csv.writer(csvfile,delimiter = ',',quotechar='"')
    #     # writer.writerow(['tuerker_id','age','gender','hand','difficulty','confidence','eyetrace'])
    #     writer.writerow([turker_id,age,gender,hand,difficulty,confidence,eyetrace])
    return json.dumps("success saving data")
##########################################################################################################################################################################################################################

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
