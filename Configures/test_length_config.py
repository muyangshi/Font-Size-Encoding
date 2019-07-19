import csv
import os

# word = 'pseudoword'
word = 'english'
numberOfWords = 150
minSize = 10
maxSize = 23
minLen = 3
maxLen = 10

def loadTask(tasklist_csv_path):
    tasklist = []
    with open(tasklist_csv_path, 'r',newline='') as configFile:
        reader = csv.reader(configFile,delimiter=',')
        heading = next(reader) # Do not use reader.next() because that is python 2
        for row in reader:
            this_task = {}
            for i in range(len(heading)-1):
                this_task[heading[i]] = int(row[i])
            this_task[heading[-1]] = row[-1]
            tasklist.append(this_task)
    # print(tasklist)
    return tasklist

tasklist_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_length.csv')
# print(tasklist_csv)
tasklist = loadTask(tasklist_csv)