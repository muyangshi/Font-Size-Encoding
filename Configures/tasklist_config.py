import csv
import os

# word = 'pseudoword'
word = 'english'
num_of_distractor = 200
minSize = 15
maxSize = 25
minLen = 3
maxLen = 10

def loadTask(tasklist_csv_path):
    tasklist = []
    with open(tasklist_csv_path, 'r',newline='') as configFile:
        reader = csv.reader(configFile,delimiter=',')
        heading = next(reader) # Do not use reader.next() because that is python 2
        for row in reader:
            this_task = {}
            for i in range(len(heading)):
                if row[i].isdigit():
                    this_task[heading[i]] = int(row[i])
                else:
                    this_task[heading[i]] = row[i]
            tasklist.append(this_task)
    return tasklist

# tasklist_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_length.csv')
# tasklist_opposite_on_circle = os.path.join(os.path.dirname(os.path.abspath(__file__)),'tasklist_opposite_on_circle.csv')
# tasklist_single_circle = os.path.join(os.path.dirname(os.path.abspath(__file__)),'tasklist_single_circle.csv')
# tasklist_multiple_circles = os.path.join(os.path.dirname(os.path.abspath(__file__)),'tasklist_multiple_circles.csv')
# tasklist_opposite_on_circle_no_flash = os.path.join(os.path.dirname(os.path.abspath(__file__)),'tasklist_opposite_on_circle_no_flash.csv')

def tasklist_path(experiment):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),'tasklist_'+experiment+'.csv')
# print(tasklist_csv)
# tasklist = loadTask(tasklist_csv)