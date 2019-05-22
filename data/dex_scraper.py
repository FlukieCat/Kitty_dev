from bs4 import BeautifulSoup, Tag
import requests
import re
import sqlite3


conn = sqlite3.connect('PokemonShuffle.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS pokedex")

c.execute("""CREATE TABLE pokedex (
	name text,
	dex_number text,
	type_ text,
	ap integer,
	maxap integer,
	rml integer,
	skill text,
	skill2 text,
	skill3 text,
	skill4 text,
	skill5 text,
	img_url text
	)""")

conn.commit()

source = requests.get(r'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_Pok%C3%A9mon_Shuffle_list_number').text
soup = BeautifulSoup(source, 'lxml')
dex = soup.find('div', class_='mw-content-ltr').find('table', class_='sortable')
p_img_url = re.compile(r'\.(png)')
p_alt_form = re.compile(r'(Shuffle)[0-9]+')
p_dex_number = re.compile(r'[#\n]')
p_type = re.compile(r'background.*?')
p_content = re.compile(r'[\n]')
for entry in dex.find_all('tr', style=r'background:#FFF'):
	name = entry.find('td', style='text-align:left').a.text
	alt = entry.find('td', style=None).find('img')['alt']
	img_url = p_img_url.sub('', alt)

	if len(img_url) > len('Shuffle000'):
		if name.lower() == 'pikachu':
			alt_form = p_alt_form.sub('', img_url)
			name = f'{name} ({alt_form})'
		elif name.lower() == 'cherrim':
			if p_alt_form.sub('', img_url) == 'S':
				pass
			else:
				alt_form = entry.find('td', style='text-align:left').small.text
				name = f'{name} ({alt_form})'
		else:
			try:
				alt_form = entry.find('td', style='text-align:left').small.text
				name = f'{name} ({alt_form})'
			except Exception:
				print(entry)
	else:
		pass

	dex_number = p_dex_number.sub('', entry.find_all(
		'td', style='font-family:Monospace')[-1].text).strip()

	type_ = entry.find('td', style=p_type).a.span.text

	stats = []
	for i in entry.find_all('td', style=None):
		try:
			stats.append(i.contents)
		except Exception:
			print(i)
	_, ap, rml, skill, skillss = stats

	ap = int(p_content.sub('', ap[0]).strip())
	rml = int(p_content.sub('', rml[0]).strip())
	maxap = c.execute(f"SELECT lv{10+rml} FROM ap_table WHERE ap={ap}").fetchone()[0]
	skills = {1: None,
			2: None,
			3: None,
			4: None,
			5: None}
	skills[1] = p_content.sub('', skill[0]).strip()
	if skillss[0].strip() is r'N/A\n':
		pass
	else:
		if len(skillss) == 1:
			skills[2] = p_content.sub('', skillss[0]).strip()
		else:
			temp_skill = []
			for s in skillss:
				if not isinstance(s, Tag):
					temp_skill.append(p_content.sub('', s).strip())
			for i in range(len(temp_skill)):
				skills[i+2] = temp_skill[i]

	c.execute("""INSERT INTO pokedex VALUES(
		:name, :dex_number, :type_, :ap, :maxap, :rml, :skill,
		:skill2, :skill3, :skill4, :skill5, :img_url)
		""", {'name': name, 'dex_number': dex_number, 'type_': type_,
		'ap': ap, 'maxap': maxap, 'rml': rml, 'skill': skills[1], 'skill2': skills[2],
		'skill3': skills[3], 'skill4': skills[4], 'skill5': skills[5],
		'img_url': img_url})

conn.commit()
conn.close()
