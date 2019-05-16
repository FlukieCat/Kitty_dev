from bs4 import BeautifulSoup
import requests
import os


url = r"https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_Pok%C3%A9mon_Shuffle_list_number"
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
imgs = soup.find_all('img', {'width':'32', 'height':'32'})

for img in imgs:
	imgName = img['alt']
	imgURL = 'http:' + img['src'].replace('32px', '128px')
	try:
		os.system(f'wget -O {imgName} {imgURL}')
	except Exception:
		print('request forbidden')
