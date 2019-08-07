import matplotlib
import matplotlib.pyplot as pyplot
import numpy as np
import csv
from collections import OrderedDict
import re
import math

# Load the correctness versus target_distance(distance between the two targets) from the csv
# (distance_between_targets,correct)
def distance_correct_data():
    # correct = []
    # distance = []
    correct_ans = []
    wrong_ans = []
    with open('pilot_client_data.csv','r') as csvdata:
        reader = csv.reader(csvdata,delimiter = ',')
        heading = next(reader)
        for row in reader:
            value = _round_distance_between_targets(row)
            if row[5] != row[6]:
                wrong_ans.append((value, False))
            else:
                correct_ans.append((value, True))
    return correct_ans,wrong_ans

# Load the clickedword's correctness, and it's position
def position_correct_data():
    correct_ans = []
    wrong_ans = []
    with open('pilot_client_data.csv','r') as csvdata:
        reader = csv.reader(csvdata,delimiter = ',')
        heading = next(reader)
        for row in reader:
            if row[5] != row[6]: # The click doesn't match the correct_word, so it's a wrong choice
                x_pos = float(row[16])
                y_pos = float(row[17])
                wrong_ans.append((x_pos,y_pos,False))
            else: # The click matches the correct_word, so it's a correct choice
                x_pos = float(row[10])
                y_pos = float(row[11])
                correct_ans.append((x_pos,y_pos,True))
    return correct_ans,wrong_ans

# Load the clickedword's distance to the center of the word cloud
def dist_from_center():
    correct_ans = []
    wrong_ans = []
    with open('pilot_client_data.csv','r') as csvdata:
        reader = csv.reader(csvdata,delimiter = ',')
        heading = next(reader)
        for row in reader:
            value = float(row[21])
            if (40 < value < 60):
                value = 50
            elif (90 < value < 110):
                value = 100
            elif (140 < value < 160):
                value = 150
            elif (190 < value < 210):
                value = 200
            if row[5] != row[6]: # The click doesn't match the correct_word, so it's a wrong choice
                wrong_ans.append((value,False))
            else: # The click matches the correct_word, so it's a correct choice
                correct_ans.append((value,True))
    return correct_ans,wrong_ans

# Load the time taken to make a comparison,
# and the distance between the two targets
def load_time_and_distance_between_targets():
    d100 = []
    d200 = []
    d300 = []
    d400 = []
    derror = []
    with open('pilot_client_data.csv','r') as csvdata:
        reader = csv.reader(csvdata,delimiter=',')
        heading = next(reader)
        for row in reader:
            time = float(row[9])
            distance_between_targets = _round_distance_between_targets(row)
            if distance_between_targets == 100:
                d100.append(time)
            elif distance_between_targets == 200:
                d200.append(time)
            elif distance_between_targets == 300:
                d300.append(time)
            elif distance_between_targets == 400:
                d400.append(time)
            else:
                derror.append(time)
    return d100,d200,d300,d400,derror


def _round_distance_between_targets(row):
    value = float(row[8])
    if (90 < value < 110):
        value = 100
    elif (190 < value < 210):
        value = 200
    elif (290 < value < 310):
        value = 300
    elif (390 < value < 410):
        value = 400
    return value


# # Load target distance between, middle to center distance, and correctness
# def dist_dist_accuracy():
#     correct_ans = []
#     wrong_ans = []
#     with open('client_data.csv','r') as csvdata:
#         reader = csv.reader(csvdata,delimiter = ',')
#         heading = next(reader)
#         for row in reader:
#             # print("word: ",row[1])
#         # Distance between the two words
#             distance_between_targets = float(row[8])
#         # Distence between the middle of the two words to the center of cloud
#             mid_x_pos = (float(re.search(r'\d+',row[6]).group()) + float(re.search(r'\d+',row[9]).group()))/2
#             mid_y_pos = (float(re.search(r'\d+',row[7]).group()) + float(re.search(r'\d+',row[10]).group()))/2
#             center_x = float(re.search(r'\d+',row[11]).group())/2
#             center_y = float(re.search(r'\d+',row[12]).group())/2
#             mid_dist_from_center = math.sqrt(pow(mid_x_pos - center_x,2)+pow(mid_y_pos - center_y,2))
#             if row[1] != row[5]:
#                 wrong_ans.append((dist_betw,mid_dist_from_center,False))
#             else:
#                 correct_ans.append((dist_betw,mid_dist_from_center,True))
#     return correct_ans,wrong_ans
#############################################################################
# # Use Matplotlib to print one scatter plot
# # Each point in the scatter represent a relation 
# # of the distance between the two target words and the center-distance of the 
# # middle of the two target words (as a relative distance to the center)
# # and the color represent it's correctness
# def dist_dist_scatter():
#     result = dist_dist_accuracy()
#     datas = (result[0],result[1]) #(the list of tuples of correct, the list of tuples of wrong)
#     # print(datas)
#     colors = ("blue","red")
#     groups = ("correct","wrong")

#     # Create plot
#     figure = pyplot.figure()
#     scatterplot = figure.add_subplot(1,1,1)

#     for data, color, group in zip(datas, colors, groups):
#         for data_tuple in data:
#             dist_betw,mid_center_dist = data_tuple[0],data_tuple[1]
#             scatterplot.scatter(mid_center_dist,dist_betw,c=color,label=group,alpha = 0.6)
    
#     # Calculating the mean values for the x,y coordinates for the correct clicks and the wrong clicks
#     # correct_pos_mean = (sum(datum[0] for datum in result[0])/len(result[0]),sum(datum[1] for datum in result[0])/len(result[0]))
#     # wrong_pos_mean = (sum(datum[0] for datum in result[1])/len(result[1]),sum(datum[1] for datum in result[1])/len(result[1]))
#     # print(correct_pos_mean,wrong_pos_mean)

#     # Plot the mean value coordinates for the correct and wrong clicks
#     # scatterplot.scatter(correct_pos_mean[0],correct_pos_mean[1],c='blue',marker="s")
#     # scatterplot.scatter(wrong_pos_mean[0],wrong_pos_mean[1],c='red',marker="s")


#     pyplot.title('Dist Dist Correctness scatterplot')
#     pyplot.xlabel('Distance of the middle point to the center')
#     pyplot.ylabel('Distance between the two target words')

#     # StackOverflow solution
#     # Dealing with replicated entries in legend
#     handles, labels = pyplot.gca().get_legend_handles_labels()
#     by_label = OrderedDict(zip(labels, handles))
#     pyplot.legend(by_label.values(), by_label.keys(),loc='upper right')

#     pyplot.show()

#############################################################################
# Use Matplotlib to print one scatter plot
# Each point in the scatter represent a click, 
# the position represent the position of the word in the cloud,
# and the color represent it's correctness
def click_position_scatter():
    result = position_correct_data()
    datas = (result[0],result[1]) #(the list of tuples of correct, the list of tuples of wrong)
    # print(datas)
    colors = ("blue","red")
    groups = ("correct","wrong")

    # Create plot
    figure = pyplot.figure()
    scatterplot = figure.add_subplot(1,1,1)

    for data, color, group in zip(datas, colors, groups):
        for data_pair in data:
            x,y = data_pair[0],data_pair[1]
            scatterplot.scatter(x,y,c=color,label=group,alpha = 0.2)
    
    # Calculating the mean values for the x,y coordinates for the correct clicks and the wrong clicks
    correct_pos_mean = (sum(datum[0] for datum in result[0])/len(result[0]),sum(datum[1] for datum in result[0])/len(result[0]))
    wrong_pos_mean = (sum(datum[0] for datum in result[1])/len(result[1]),sum(datum[1] for datum in result[1])/len(result[1]))
    print(correct_pos_mean,wrong_pos_mean)

    # Plot the mean value coordinates for the correct and wrong clicks
    scatterplot.scatter(correct_pos_mean[0],correct_pos_mean[1],c='blue',marker="s")
    scatterplot.scatter(wrong_pos_mean[0],wrong_pos_mean[1],c='red',marker="s")


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
def distance_between_targets_hist():
    result = distance_correct_data()
    correct_dist = [data_pair[0] for data_pair in result[0]]
    wrong_dist = [data_pair[0] for data_pair in result[1]]

    num_bins = 100

    # Create plot 
    figure = pyplot.figure()

    # Create the upper histogram
    correct_hist = figure.add_subplot(2,1,1)
    correct_hist.hist(correct_dist, num_bins, facecolor='blue',range=(0,1000),alpha = 0.5)
    pyplot.title('Histogram of correct and wrong')
    pyplot.ylabel('N Correct')

    # Create the bottom histogram
    wrong_hist = figure.add_subplot(2,1,2)
    wrong_hist.hist(wrong_dist, num_bins, facecolor = 'red',range=(0,1000),alpha = 0.5)
    pyplot.xlabel('distance between the two words')
    pyplot.ylabel('N Wrong')

    pyplot.show()
#############################################################################
# Use matplotlib to print a histogram of the overlay of the right and wrong
# and a barplot of the percentage accuracy at each distance between targets
# that shows the accuracy versus the distance between the two target words
# I should assume that the barplot is right skewed (if closer distance means higher accuracy)
def distance_between_targets_accuracy():
    result = distance_correct_data()
    correct_dist = [data_pair[0] for data_pair in result[0]]
    wrong_dist = [data_pair[0] for data_pair in result[1]]

    num_bins = 50

    # Create plot 
    figure = pyplot.figure()
    acc_histogram = figure.add_subplot(2,1,1)

    correct_plot = acc_histogram.hist(correct_dist,num_bins,edgecolor='black',facecolor='blue',range=(0,500),alpha=0.5,label = 'correct')
    wrong_plot = acc_histogram.hist(wrong_dist,num_bins,edgecolor='black',facecolor='red',range=(0,500),alpha=0.5,label = 'wrong')
    
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
    for a,b in zip(x_coordinate,percentage):
        if b != 0:
            pyplot.text(a,b,str(b)[:5])
    pyplot.ylabel('Percentage Correct')
    pyplot.xlabel('Distance between the two target words (px)')

    pyplot.show()

#############################################################################
# Use matplotlib to print a histogram and a barplot
# that shows the accuracy versus the distance between the target word and the center of the cloud
# I should assume that the histogram is right skewed (if closer distance means higher accuracy)
def distance_to_center_accuracy():
    result = dist_from_center()

    correct_dist = [data_pair[0] for data_pair in result[0]]
    wrong_dist = [data_pair[0] for data_pair in result[1]]

    num_bins = 40

    # Create plot 
    figure = pyplot.figure()
    # The first plot is a histogram that overlay the correct and the wrong together
    acc_histogram = figure.add_subplot(2,1,1)

    correct_plot = acc_histogram.hist(correct_dist,num_bins,edgecolor='black',facecolor='blue',range=(0,400),alpha=0.5,label = 'correct')
    wrong_plot = acc_histogram.hist(wrong_dist,num_bins,edgecolor='black',facecolor='red',range=(0,400),alpha=0.5,label = 'wrong')
    
    pyplot.legend(loc='upper right')
    pyplot.title('Histogram of number correct and wrong')
    pyplot.ylabel('N')

    percentage = [float((a)/(a+b)) if (a+b) != 0 else 0 for a,b in zip(correct_plot[0],wrong_plot[0])]

    x_coordinate = [int(a) for a in correct_plot[1]]
    x_coordinate.pop(-1)
    # x_coordinate = [0,50,100,150,200,250,300,350,400,450,500]

    percent_bar = figure.add_subplot(2,1,2)
    percent_bar.bar(x_coordinate,percentage,width=6,alpha = 0.8)
    for a,b in zip(x_coordinate,percentage):
        if b != 0:
            pyplot.text(a,b,str(b)[:5])
    pyplot.ylabel('Percentage Correct')
    pyplot.xlabel('Distance of the click from center (px)')

    pyplot.show()

##############################################################################
def time_distance_between_targets():
    result = load_time_and_distance_between_targets()
    d100 = sum(result[0])/len(result[0])
    d200 = sum(result[1])/len(result[1])
    d300 = sum(result[2])/len(result[2])
    d400 = sum(result[3])/len(result[3])
    list_mean_time = [d100,d200,d300,d400]
    index = [1,2,3,4]
    label = ['100px','200px','300px','400px']
    pyplot.bar(index,list_mean_time,width=0.5)
    for a,b in zip(index,list_mean_time):
        pyplot.text(a,b,str(b)[:6])
    pyplot.xticks(index,label,fontsize=10)
    pyplot.xlabel('Distance between target words (px)',fontsize = 12)
    pyplot.ylabel('Time taken to make decision (s)', fontsize = 12)
    pyplot.title('Time v.s. Distance between targets')

    pyplot.show()



#hypo2
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
def hypo2_load_click_pos():
    correct_clicks = []
    wrong_clicks = []
    with open('hypo2_client_data.csv','r')as csvdata:
        reader = csv.reader(csvdata,delimiter=',')
        heading = next(reader)
        for row in reader:
            clicked_word_x = float(row[7])
            clicked_word_y = float(row[8])
            clicked_word_center_distance = float(row[9])
            sizeDiff = int(row[11]) - int(row[12])
            # print(sizeDiff)
            if row[10] != row[11]:
                wrong_clicks.append((clicked_word_x,clicked_word_y,clicked_word_center_distance,sizeDiff,False))
            else:
                correct_clicks.append((clicked_word_x,clicked_word_y,clicked_word_center_distance,sizeDiff,True))
    return correct_clicks,wrong_clicks

def hypo2_scatterplot():
    result = hypo2_load_click_pos()
    datas = (result[0],result[1])
    colors = ("blue","red")
    groups = ("correct","wrong")

    figure = pyplot.figure()
    scatterplot = figure.add_subplot(1,1,1)
    for data, color, group in zip(datas, colors, groups):
        for data_set in data:
            x,y = data_set[0],data_set[1]
            scatterplot.scatter(x,y,c=color,label=group,alpha=0.3)
    pyplot.title('Scatterplot of word\'s Position versus correctness')
    pyplot.xlabel('x position (px)')
    pyplot.ylabel('y position (px)')

    handles, labels = pyplot.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    pyplot.legend(by_label.values(), by_label.keys(),loc=2)

    pyplot.show()

def hypo2_stacked_bar():
    result = hypo2_load_click_pos()
    correct_clicks = result[0]
    wrong_clicks = result[1]
    total_clicks = len(correct_clicks) + len(wrong_clicks)
    ring0_clicks_correct,ring0_clicks_wrong = [],[]
    ring1_clicks_correct,ring1_clicks_wrong = [],[]
    ring2_clicks_correct,ring2_clicks_wrong = [],[]
    for data in correct_clicks:
        distance_from_center = data[2]
        if distance_from_center < 100:
            # ring0
            ring0_clicks_correct.append(data)
        elif 100< distance_from_center < 200:
            # ring1
            ring1_clicks_correct.append(data)
        elif 300 < distance_from_center:
            #ring2
            ring2_clicks_correct.append(data)
    for data in wrong_clicks:
        if distance_from_center < 100:
            ring0_clicks_wrong.append(data)
        elif 100 < distance_from_center < 200:
            ring1_clicks_wrong.append(data)
        elif 300 < distance_from_center:
            ring2_clicks_wrong.append(data)
    # ring0_percent_click = (len(ring0_clicks_correct) + len(ring0_clicks_wrong))/total_clicks
    # ring1_percent_click = (len(ring1_clicks_correct)+len(ring1_clicks_wrong))/total_clicks
    # ring2_percent_click = (len(ring2_clicks_correct)+len(ring2_clicks_wrong))/total_clicks
    # ring0_percent_accuracy = len(ring0_clicks_correct)/(len(ring0_clicks_correct)+len(ring0_clicks_wrong))
    # ring1_percent_accuracy = len(ring1_clicks_correct)/(len(ring1_clicks_correct)+len(ring1_clicks_wrong))
    # ring2_percent_accuracy = len(ring2_clicks_correct)/(len(ring2_clicks_correct)+len(ring2_clicks_wrong))
    

    size1_ring0_c,size1_ring1_c,size1_ring2_c = [],[],[]
    size2_ring0_c,size2_ring1_c,size2_ring2_c = [],[],[]
    size3_ring0_c,size3_ring1_c,size3_ring2_c = [],[],[]

    for click in ring0_clicks_correct:
        if click[3] == 1:
            size1_ring0_c.append(click)
        elif click[3] == 2:
            size2_ring0_c.append(click)
        elif click[3] == 3:
            size3_ring0_c.append(click)

    for click in ring1_clicks_correct:
        if click[3] == 1:
            size1_ring1_c.append(click)
        elif click[3] == 2:
            size2_ring1_c.append(click)
        elif click[3] == 3:
            size3_ring1_c.append(click)

    for click in ring2_clicks_correct:
        if click[3] == 1:
            size1_ring2_c.append(click)
        elif click[3] == 2:
            size2_ring2_c.append(click)
        elif click[3] == 3:
            size3_ring2_c.append(click)
    
    size1_ring0_w,size1_ring1_w,size1_ring2_w = [],[],[]
    size2_ring0_w,size2_ring1_w,size2_ring2_w = [],[],[]
    size3_ring0_w,size3_ring1_w,size3_ring2_w = [],[],[]

    for click in ring0_clicks_wrong:
        if click[3] == 1:
            size1_ring0_w.append(click)
        elif click[3] == 2:
            size2_ring0_w.append(click)
        elif click[3] == 3:
            size3_ring0_w.append(click)

    for click in ring1_clicks_wrong:
        if click[3] == 1:
            size1_ring1_w.append(click)
        elif click[3] == 2:
            size2_ring1_w.append(click)
        elif click[3] == 3:
            size3_ring1_w.append(click)

    for click in ring2_clicks_wrong:
        if click[3] == 1:
            size1_ring2_w.append(click)
        elif click[3] == 2:
            size2_ring2_w.append(click)
        elif click[3] == 3:
            size3_ring2_w.append(click)
    # print(size1_ring0_c,size2_ring0_c,size3_ring0_c)
    # size1_ring0_c.append((1,1,1,1,True))
    # size1_ring0_c.append((2,2,2,2,True))
    # print(size1_ring0_c,size2_ring0_c,size3_ring0_c)


    ring0_correct_clicks = [len(size1_ring0_c),len(size2_ring0_c),len(size3_ring0_c)]
    ring0_wrong_clicks = [len(size1_ring0_w),len(size2_ring0_w),len(size3_ring0_w)]
    ring1_correct_clicks = [len(size1_ring1_c),len(size2_ring1_c),len(size3_ring1_c)]
    ring1_wrong_clicks = [len(size1_ring1_w),len(size2_ring1_w),len(size3_ring1_w)]
    ring2_correct_clicks = [len(size1_ring2_c),len(size2_ring2_c),len(size3_ring2_c)]
    ring2_wrong_clicks = [len(size1_ring2_w),len(size2_ring2_w),len(size3_ring2_w)]


    N = 3
    index = np.arange(N)
    width = 0.2
    correct_ring0 = pyplot.bar(index-width, ring0_correct_clicks, width,color="blue",edgecolor="black",label="correct")
    wrong_ring0 = pyplot.bar(index-width, ring0_wrong_clicks, width,bottom=ring0_correct_clicks,color="orange",edgecolor="black",label="wrong")
    correct_ring1 = pyplot.bar(index,ring1_correct_clicks,width,color="blue",edgecolor="black",label="correct")
    wrong_ring1 = pyplot.bar(index,ring1_wrong_clicks,width,bottom=ring1_correct_clicks,color="orange",edgecolor="black",label="wrong")
    correct_ring2 = pyplot.bar(index+width,ring2_correct_clicks,width,color="blue",edgecolor="black",label="correct")
    wrong_ring2 = pyplot.bar(index+width,ring2_wrong_clicks,width,bottom=ring2_correct_clicks,color="orange",edgecolor="black",label="wrong")


    pyplot.xticks(index,('1px','2px','3px'))
    # pyplot.legend()
    handles, labels = pyplot.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    pyplot.legend(by_label.values(), by_label.keys(),loc=2)
    # pyplot.legend((correct[0],wrong[0]),('Correct','Wrong'))
    # print(correct[0],wrong[0])
    # print(ring0_c[0],ring0_w[0])
    # pyplot.legend((ring1_c[0],ring1_w[0]),('Correct','Wrong'))
    # print(ring1_c[0],ring1_w[0])
    pyplot.show()


    # pass
def hypo2_percentages():
    result = hypo2_load_click_pos()
    correct_clicks = result[0]
    wrong_clicks = result[1]
    total_clicks = len(correct_clicks) + len(wrong_clicks)
    ring0_clicks_correct,ring0_clicks_wrong = [],[]
    ring1_clicks_correct,ring1_clicks_wrong = [],[]
    ring2_clicks_correct,ring2_clicks_wrong = [],[]
    for data in correct_clicks:
        distance_from_center = data[2]
        if distance_from_center < 100:
            # ring0
            ring0_clicks_correct.append(data)
        elif 100< distance_from_center < 200:
            # ring1
            ring1_clicks_correct.append(data)
        elif 300 < distance_from_center:
            #ring2
            ring2_clicks_correct.append(data)
    for data in wrong_clicks:
        if distance_from_center < 100:
            ring0_clicks_wrong.append(data)
        elif 100 < distance_from_center < 200:
            ring1_clicks_wrong.append(data)
        elif 300 < distance_from_center:
            ring2_clicks_wrong.append(data)
    ring0_percent_click = (len(ring0_clicks_correct) + len(ring0_clicks_wrong))/total_clicks
    ring1_percent_click = (len(ring1_clicks_correct)+len(ring1_clicks_wrong))/total_clicks
    ring2_percent_click = (len(ring2_clicks_correct)+len(ring2_clicks_wrong))/total_clicks
    ring0_percent_accuracy = len(ring0_clicks_correct)/(len(ring0_clicks_correct)+len(ring0_clicks_wrong))
    ring1_percent_accuracy = len(ring1_clicks_correct)/(len(ring1_clicks_correct)+len(ring1_clicks_wrong))
    ring2_percent_accuracy = len(ring2_clicks_correct)/(len(ring2_clicks_correct)+len(ring2_clicks_wrong))

    labels = ['ring1','ring2','ring3']
    percent_clicks = [ring0_percent_click,ring1_percent_click,ring2_percent_click]
    percent_accuracy = [ring0_percent_accuracy,ring1_percent_accuracy,ring2_percent_accuracy]
    
    index = np.arange(len(labels)) # the label locations
    width = 0.2 # the width of the bars

    fig, ax = pyplot.subplots()
    rects1 = ax.bar(index - width/2,percent_clicks,label = "percent clicks",width=0.2)
    rects2 = ax.bar(index + width/2, percent_accuracy,label = "accuracy",width=0.2)
    ax.set_ylabel("Percentage")
    ax.set_title("Percentage by each ring")
    ax.set_xticks(index)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    pyplot.show()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax = pyplot.gca()
        ax.annotate('{}'.format(height)[:4],
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

