from bs4 import BeautifulSoup
import requests
import sqlite3
import re

conn = sqlite3.connect('PokemonShuffle.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS skill_table")

c.execute("""CREATE TABLE skill_table (
			name text,
			description text,
			addtional_info text,
			multiplier text,
			proc_rate text,
			skill_points text
			)""")
conn.commit()

source = requests.get(r'https://pkmnshuffle.fandom.com/wiki/Category:Skill').text
soup = BeautifulSoup(source, 'lxml')
tables = soup.find('div', class_= 'mw-content-ltr').find_all('table')

for table in tables:
	for row in table.find_all('tr'):
		if row.find('td').text.lower() == 'name':
			pass
		else:
			stats = []
			for i in row.find_all('td'):
			    stats.append(re.sub(r'[\n]', '', i.text).strip())
			if stats[0] == 'name':
				pass
			else:
				name, description, addtional_info, multiplier, proc_rate, skill_points, _ = stats
				c.execute("INSERT INTO skill_table VALUES(:name, :description, :addtional_info, :multiplier, :proc_rate, :skill_points)", {
				'name':name, 'description':description, 'addtional_info':addtional_info, 'multiplier':multiplier, 'proc_rate':proc_rate, 'skill_points':skill_points})

conn.commit()
conn.close()