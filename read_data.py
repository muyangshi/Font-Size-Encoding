import csv
import sys
import os
from bs4 import BeautifulSoup


receive_data = """<!DOCTYPE html>
<html>
	<head>
		<title>Turk's Image</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="../static/jqcloud.css">
		
	</head>

	<body>
        <div id="WordCloudContainer" style="text-align: center;">
            <div id="JQWC" style="width: 650px; height: 450px; display: inline-block;" class="jqcloud"> 
            </div>
        </div>        

        <script type="text/javascript" src="../static/jquery-3.4.1.min.js"></script>
        <script type="text/javascript" src="../static/jqcloud-1.0.4.js"></script>
        <!-- <script type="text/javascript" src="static/index.js"></script> -->
        
    </body>
    
</html>
"""


def find_by_id(id):
    spanContents = ''
    id = id-1
    with open('client_data.csv',newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter = ',', quotechar='"')
        for i in range(id):
            next(reader)
        row = next(reader)
        # print(row)
        spanContents = row[-1]
    return spanContents


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {0} id'.format(sys.argv[0]))
        print('     Example: {0} 0'.format(sys.argv[0]))
        exit()
    id = sys.argv[1]

    soup = BeautifulSoup(receive_data, 'html.parser')
    mydiv = soup.findAll("div",{"class": "jqcloud"})[0]

    span_text = find_by_id(int(id))
    span_soup = BeautifulSoup(span_text,'html.parser')

    mydiv.insert(0,span_soup)
    print(soup)

    directory = os.path.join(os.getcwd(), 'results', '')

    result_id = 'result_' + id + '.html'
    with open(directory + result_id, "w") as file:
        file.write(str(soup))
