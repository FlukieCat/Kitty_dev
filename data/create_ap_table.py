from bs4 import BeautifulSoup, Tag
import requests
import re
import sqlite3


conn = sqlite3.connect('PokemonShuffle.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS ap_table")

c.execute("""CREATE TABLE ap_table (
	ap integer,
	lv1 integer,
	lv2 integer,
	lv3 integer,
	lv4 integer,
	lv5 integer,
	lv6 integer,
	lv7 integer,
	lv8 integer,
	lv9 integer,
	lv10 integer,
	lv11 integer,
	lv12 integer,
	lv13 integer,
	lv14 integer,
	lv15 integer,
	lv16 integer,
	lv17 integer,
	lv18 integer,
	lv19 integer,
	lv20 integer,
	lv21 integer,
	lv22 integer,
	lv23 integer,
	lv24 integer,
	lv25 integer,
	lv26 integer,
	lv27 integer,
	lv28 integer,
	lv29 integer,
	lv30 integer
	)""")

conn.commit()

lv_to_ap = {30: [30,35,39,42,45,47,49,51,53,55,61,67,73,79,85,88,91,94,97,100,102,104,106,108,110,112,114,116,118,120],
40: [40,43,46,48,50,52,54,56,58,60,66,72,78,84,90,93,96,99,102,105,107,109,111,113,115,117,119,121,123,125],
50: [50,53,56,58,60,62,64,66,68,70,75,80,85,90,100,103,106,109,112,115,116,117,118,119,120,122,124,126,128,130],
60: [60,63,66,68,70,72,74,76,78,80,84,88,92,96,105,108,111,114,117,120,121,122,123,124,125,127,129,131,133,135],
70: [70,73,76,78,80,82,84,86,88,90,93,96,99,102,110,113,116,119,122,125,126,127,128,129,130,132,134,136,138,140],
80: [80,83,86,88,90,92,94,96,98,100,102,104,106,108,115,118,121,124,127,130,131,132,133,134,135,137,139,141,143,145],
90: [90,93,96,98,100,102,104,106,108,110,112,114,116,118,120,123,126,129,132,135,136,137,138,139,140,142,144,146,148,150]}


for ap in [30, 40, 50, 60, 70, 80, 90]:
	c.execute("""INSERT INTO ap_table VALUES(
			:ap, :lv1, :lv2, :lv3, :lv4, :lv5, :lv6, :lv7, :lv8, :lv9, :lv10,
			:lv11, :lv12, :lv13, :lv14, :lv15, :lv16, :lv17, :lv18, :lv19, :lv20,
			:lv21, :lv22, :lv23, :lv24, :lv25, :lv26, :lv27, :lv28, :lv29, :lv30)
			""", {'ap': ap, 'lv1': lv_to_ap[ap][0], 'lv2': lv_to_ap[ap][1],
			'lv3': lv_to_ap[ap][2], 'lv4': lv_to_ap[ap][3], 'lv5': lv_to_ap[ap][4], 'lv6': lv_to_ap[ap][5],
			'lv7': lv_to_ap[ap][6], 'lv8': lv_to_ap[ap][7], 'lv9': lv_to_ap[ap][8], 'lv10': lv_to_ap[ap][9],
			'lv11': lv_to_ap[ap][10], 'lv12': lv_to_ap[ap][11],
			'lv13': lv_to_ap[ap][12], 'lv14': lv_to_ap[ap][13], 'lv15': lv_to_ap[ap][14], 'lv16': lv_to_ap[ap][15],
			'lv17': lv_to_ap[ap][16], 'lv18': lv_to_ap[ap][17], 'lv19': lv_to_ap[ap][18], 'lv20': lv_to_ap[ap][19],
			'lv21': lv_to_ap[ap][20], 'lv22': lv_to_ap[ap][21],
			'lv23': lv_to_ap[ap][22], 'lv24': lv_to_ap[ap][23], 'lv25': lv_to_ap[ap][24], 'lv26': lv_to_ap[ap][25],
			'lv27': lv_to_ap[ap][26], 'lv28': lv_to_ap[ap][27], 'lv29': lv_to_ap[ap][28], 'lv30': lv_to_ap[ap][29]})

conn.commit()
conn.close()