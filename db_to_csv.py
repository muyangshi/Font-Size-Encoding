'''
Allen server does not provide a display
So, in order to access the database data, we need to have them locally in csv format.
OR, can I actually have psql on my computer?
'''
import sys
import psycopg2
import csv
def get_connection():
	'''
	Returns a connection to the database described
	in the config module. Returns None if the
	connection attempt fails.
	'''
	connection = None
	try:
		connection = psycopg2.connect(host='localhost',database='fontsize',user='fontsize',password='wordcloudsbad?')
	except Exception as e:
		print(e, file=sys.stderr)
	return connection

def get_stimuli_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT turker_id,clicked_word,correct_word,wrong_word,distance_between_targets,time,correct_word_fontsize,wrong_word_fontsize,correct_word_width,wrong_word_width,correct_word_height,wrong_word_height,correct_word_x,wrong_word_x,correct_word_y,wrong_word_y FROM pilot_opposite_on_circle")
    data_list = cursor.fetchall()
    print(data_list[0])
    with open('for_calculation.csv','a',newline='') as csvdata:
        writer = csv.writer(csvdata,delimiter = ',',quotechar = '"')
        writer.writerow(['turker_id','clicked_word','correct_word','wrong_word','distance_between_targets','time','correct_word_fontsize','wrong_word_fontsize','correct_word_width','wrong_word_width','correct_word_height','wrong_word_height','correct_word_x','wrong_word_x','correct_word_y','wrong_word_y'])
        for row in data_list:
            writer.writerow(row)
    # connection.commit()
    cursor.close()
    connection.close()