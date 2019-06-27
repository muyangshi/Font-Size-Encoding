import csv
from bs4 import BeautifulSoup


receive_data = """
<!DOCTYPE html>
<html>
	<head>
		<title>WordCloud</title>
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

soup = BeautifulSoup(receive_data, 'html.parser')
print(soup.prettify())

mydiv = soup.findAll("div",{"class": "jqcloud"})[0]
print(mydiv)


span_text = """<span id="JQWC_word_0" class="w10 CloudWord" style="position: absolute; left: 253.498px; top: 193.993px;">Dates</span><span id="JQWC_word_1" class="w8 CloudWord" style="position: absolute; left: 219.226px; top: 134.928px;">Entawak</span><span id="JQWC_word_2" class="w8 CloudWord" style="position: absolute; left: 227.272px; top: 258.491px;">Farkleberry</span><span id="JQWC_word_3" class="w7 CloudWord" style="position: absolute; left: 183.627px; top: 312.585px;">Crab apples</span><span id="JQWC_word_4" class="w5 CloudWord" style="position: absolute; left: 419.551px; top: 207.266px;">Fig</span><span id="JQWC_word_5" class="w4 CloudWord" style="position: absolute; left: 105px; top: 210.063px;">Cucumbers</span><span id="JQWC_word_6" class="w2 CloudWord" style="position: absolute; left: 410.64px; top: 160.751px;">Honeydew melon</span><span id="JQWC_word_7" class="w2 CloudWord" style="position: absolute; left: 403.857px; top: 177.777px;">Cantaloupe</span><span id="JQWC_word_8" class="w2 CloudWord" style="position: absolute; left: 356.851px; top: 112.644px;">Indonesian Lime</span><span id="JQWC_word_9" class="w1 CloudWord" style="position: absolute; left: 131.021px; top: 244.125px;">Evergreen Huckleberry</span>"""

span_soup = BeautifulSoup(span_text,'html.parser')
print(span_soup)

mydiv.insert(0,span_soup)
print(mydiv)
print(soup)

soup.prettify(formatter=None)
print(soup)

spanContents = ''

def find_by_id(id):
    with open('client_data.csv',newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter = ',', quotechar='"')
        for i in range(id):
            next(reader)
        row = next(reader)
        spanContents = row[-1]
        print(spanContents)
        # render_html(spanContents)
        # flask.render_template('receive_data.html', cloud_info=the_cloud)

# def render_html(spanContents):
#     flask.render_template('receive_data.html', cloud_info = spanContents)
#     return 'Done'