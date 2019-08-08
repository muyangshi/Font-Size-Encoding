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
		connection = psycopg2.connect(host='localhost',
                                      database='fontsize',
									  user='fontsize',
									  password='wordcloudsbad?')
	except Exception as e:
		print(e, file=sys.stderr)
	return connection

def get_stimuli_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                SELECT * FROM pilot_data_on_circle 
                WHERE turker_id = %s OR turker_id= %s OR turker_id = %s OR turker_id = %s OR turker_id = %s OR turker_id = %s OR turker_id = %s""",
                ('ericalexander','alper','alpersmells','skylar','muyang','muyang2','mular'))
    data_list = cursor.fetchall()
    print(data_list[0])
    with open('temp.csv','a',newline='') as csvdata:
        writer = csv.writer(csvdata,delimiet = ',',quotechar = '"')
        for row in data_list:
            writer.writerow(row)
    # connection.commit()
    cursor.close()
    connection.close()