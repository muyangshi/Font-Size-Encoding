import matplotlib.pyplot as pyplot
import csv
from collections import OrderedDict
import re

# Load the correctness versus distance from the csv
# (distance,correct)
def distance_correct_data():
    # correct = []
    # distance = []
    correct_ans = []
    wrong_ans = []
    with open('client_data.csv','r') as csvdata:
        reader = csv.reader(csvdata,delimiter = ',')
        heading = next(reader)
        for row in reader:
            if row[1] != row[5]:
                wrong_ans.append((int(float(row[4])), False))
            else:
                correct_ans.append((int(float(row[4])), True))
    return correct_ans,wrong_ans

# Load the word's correctness, and it's position
def position_correct_data():
    correct_ans = []
    wrong_ans = []
    with open('client_data.csv','r') as csvdata:
        reader =csv.reader(csvdata,delimiter = ',')
        heading = next(reader)
        for row in reader:
            x_pos = int(re.search(r'\d+',row[2]).group())
            y_pos = int(re.search(r'\d+',row[3]).group())
            if row[1] != row[5]:
                wrong_ans.append((x_pos,y_pos,False))
            else:
                correct_ans.append((x_pos,y_pos,True))
    return correct_ans,wrong_ans


#############################################################################
# Use Matplotlib to print one scatter plot
# Each point in the scatter represent a click, 
# the position represent the position of the word in the cloud,
# and the color represent it's correctness
def position_scatter():
    result = position_correct_data()
    datas = (result[0],result[1]) #the list of tuples of correct, the list of tuples of wrong
    # print(datas)
    colors = ("blue","red")
    groups = ("correct","wrong")

    # Create plot
    figure = pyplot.figure()
    scatterplot = figure.add_subplot(1,1,1)

    for data, color, group in zip(datas, colors, groups):
        for data_pair in data:
            x,y = data_pair[0],data_pair[1]
            scatterplot.scatter(x,y,c=color,label=group,alpha = 0.85)

    pyplot.title('Scatterplot of Word\'s Position versus Correctness')
    pyplot.xlabel('x position (px)')
    pyplot.ylabel('y position (px)')

    # StackOverflow solution
    # Dealing with replicated entries in legend
    handles, labels = pyplot.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    pyplot.legend(by_label.values(), by_label.keys(),loc=2)

    pyplot.show()

#############################################################################
# Use matplotlib to print two top and bottom parallel histogram
# that shows the number of correct/wrong versus the distance between the two target words
# I should assume that the correct histogram is right skewed
# and the wrong histogram to be left skewed?
def parallel_hist():
    result = distance_correct_data()

    correct_dist = []
    for data_pair in result[0]:
        correct_dist.append(data_pair[0])
    wrong_dist = []
    for data_pair in result[1]:
        wrong_dist.append(data_pair[0])

    num_bins = 50

    # Create plot 
    figure = pyplot.figure()

    # Create the upper histogram
    correct_hist = figure.add_subplot(2,1,1)
    correct_hist.hist(correct_dist, num_bins, facecolor='blue',range=(0,650),alpha = 0.5)
    pyplot.title('Histogram of correct and wrong')
    pyplot.ylabel('N Correct')

    # Create the bottom histogram
    wrong_hist = figure.add_subplot(2,1,2)
    wrong_hist.hist(wrong_dist, num_bins, facecolor = 'red',range=(0,650),alpha = 0.5)
    pyplot.xlabel('distance between the two words')
    pyplot.ylabel('N Wrong')

    pyplot.show()
#############################################################################
# Use matplotlib to print a histogram and a barplot
# that shows the accuracy versus the distance between the two target words
# I should assume that the barplot is right skewed (if closer distance means higher accuracy)
def dist_accuracy():
    result = distance_correct_data()

    correct_dist = []
    for data_pair in result[0]:
        correct_dist.append(data_pair[0])
    wrong_dist = []
    for data_pair in result[1]:
        wrong_dist.append(data_pair[0])

    num_bins = 50

    # Create plot 
    figure = pyplot.figure()
    acc_histogram = figure.add_subplot(2,1,1)

    correct_plot = acc_histogram.hist(correct_dist,num_bins,facecolor='blue',range=(0,650),alpha=0.5,label = 'correct')
    wrong_plot = acc_histogram.hist(wrong_dist,num_bins,facecolor='red',range=(0,650),alpha=0.5,label = 'wrong')
    
    pyplot.legend(loc='upper right')
    pyplot.title('Histogram of number correct and wrong')
    pyplot.ylabel('N')

    # print(type(correct_plot[0][0]))
    # print(wrong_plot[0],wrong_plot[1])
    percentage = [float((a)/(a+b)) if (a+b) != 0 else 0 for a,b in zip(correct_plot[0],wrong_plot[0])]
    # print(percentage)
    x_coordinate = [int(a) for a in correct_plot[1]]
    x_coordinate.pop(-1)
    # print(x_coordinate)
    percent_bar = figure.add_subplot(2,1,2)
    percent_bar.bar(x_coordinate,percentage,width=8)
    pyplot.ylabel('Percentage Correct')
    pyplot.xlabel('Distance between the two words')

    pyplot.show()