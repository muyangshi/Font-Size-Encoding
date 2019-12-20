import requests
from bs4 import BeautifulSoup
import csv
import json
dict_file = {}

websites = []

result = requests.get("https://enchantedlearning.com/wordlist/")
src = result.content
soup = BeautifulSoup(src,'lxml')
links = soup.find_all('a')
# print(links)

for link in links:
	# print(link.attrs['href'])
	if '/wordlist' in link.attrs['href'] and '.shtml' in link.attrs['href'] and 'index' not in link.arrts['href']:
		websites.append('https://enchantedlearning.com/'+link.attrs['href'])
print(*websites,sep='\n')

# for website in websites:
# 	result = requests.get(website)
# 	src = result.content
# 	# print(src)

# 	soup = BeautifulSoup(src,'lxml')
# 	# words_div = soup.find_all('div',class_='wordlist-item')
# 	# print(words_div)
# 	topic = soup.find('h1',class_='body-title__title').text
# 	topic = topic[1:len(topic)-1].replace(' Word List','').replace(' Vocabulary','').replace(' ','_')
# 	print(topic)
# 	words = []
# 	for word in soup.find_all('div',class_='wordlist-item'):
# 		words.append(word.text)

# 	with open(topic+'.csv','w') as csvfile:
# 		writer = csv.writer(csvfile,delimiter=',',quotechar='"')
# 		writer.writerow(words)
# 	dict_file[topic] = words

# json_file = json.dumps(dict_file)
# f = open("dict.json","w")
# f.write(json_file)
# f.close()