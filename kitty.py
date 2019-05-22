# bot id 577963510118481921
# token NTc3OTYzNTEwMTE4NDgxOTIx.XNszAg.qF9uMnrZhqa0RNbsUuuPP2o8uPM
# server id 577963058928812062

import discord
from discord.ext import commands
import sqlite3
from EmbedGenerator import EmbedGenerator
from QueryParser import QueryParser

setting = open('./settings.txt', 'r')
TOKEN = setting.readline().rstrip('\n')
owner_id = setting.readline().rstrip('\n')
setting.close()

bot = commands.Bot(command_prefix='?', owner_id=owner_id)

DB = sqlite3.connect('./data/PokemonShuffle.db')
EG = EmbedGenerator()
QP = QueryParser()
supported_queries = ['type', 'ap', 'maxap', 'skill', 'rml', 'rmls']

@bot.event
async def on_ready():
	print(f"{bot.user} is online!")


@bot.command()
async def shutdown(ctx):
	if ctx.author.id == bot.owner_id:
		await ctx.send('Bye ~')
		await bot.close()
	else:
		migi_gif = discord.File('./local_images/migi.gif', filename='migi.gif')
		await ctx.send(file=migi_gif)


def extract_pokemon(result):
	pokemon = {}
	pokemon['Name'] = result[0]
	pokemon['DexNum'] = result[1]
	pokemon['Type'] = result[2]
	pokemon['AP'] = result[3]
	pokemon['MaxAP'] = result[4]
	pokemon['RMLs'] = result[5]
	pokemon['Skill'] = result[6]
	pokemon['Skill2'] = result[7]
	pokemon['Skill3'] = result[8]
	pokemon['Skill4'] = result[9]
	pokemon['Skill5'] = result[10]
	pokemon['ImgURL'] = result[-1]
	return pokemon


@bot.command()
async def dex(ctx, *, name):
	c = DB.cursor()
	name = QP.parse_pokemon(name)
	result = c.execute("SELECT * FROM pokedex WHERE Name LIKE (?)", (name,)).fetchone()
	if len(result) > 0:
		pokemon = extract_pokemon(result)
		embed = EG.format_dex_embed(pokemon)
		await ctx.send(embed=embed)
	else:
		await ctx.send("Failed to find the queried pokemon, please use the correct format {Pokemon Form}")

def extract_skill(result):
	skill = {}
	skill['Name'] = result[0]
	skill['Description'] = result[1]
	skill['AdditionalInfo'] = result[2]
	skill['Multiplier'] = result[3]
	skill['ProcRate'] = result[4]
	skill['SkillPoints'] = result[5]
	return skill

@bot.command()
async def skill(ctx, *, name):
	c = DB.cursor()
	name = QP.parse_skill(name)
	result = c.execute("SELECT * FROM skill_table WHERE Name LIKE (?)", (name,)).fetchone()
	if len(result) > 0:
		print(result)
		skill = extract_skill(result)
		embed = EG.format_skill_embed(skill)
		await ctx.send(embed=embed)
	else:
		await ctx.send("Failed to find the queried skill.")


def get_query_result(valid_query):
	sqlite_query_str = "SELECT Name FROM pokedex WHERE "
	type_str, ap_str, maxap_str, skill_str, rml_str = None, None, None, None, None
	for q in valid_query:
		if q == 'type':
			valid_type = QP.parse_type(valid_query[q])
			type_str = f"type_='{valid_type}'"
		elif q == 'ap':
			valid_ap = QP.parse_number(valid_query[q])
			ap_str = f"ap={valid_ap}"
		elif q == 'maxap':
			valid_maxap = QP.parse_number(valid_query[q])
			maxap_str = f"maxap={valid_maxap}"
		elif q == 'skill':
			valid_skill = QP.parse_skill(valid_query[q])
			skill_str = f"(skill LIKE '{valid_skill}' OR skill2 LIKE '{valid_skill}' OR skill3 LIKE '{valid_skill}' OR skill4 LIKE '{valid_skill}' OR skill5 LIKE '{valid_skill}')"
		elif q == 'rml' or q == 'rmls':
			valid_rml = QP.parse_number(valid_query[q])
			rml_str = f"rml={valid_rml}"

	conditions = [cond for cond in [type_str, ap_str, maxap_str, skill_str, rml_str] if cond is not None]
	if len(conditions) > 1:
		condition_str = (' AND ').join(conditions)
	else:
		condition_str = conditions[0]

	sqlite_query_str += condition_str
	# always order by MaxAP for now
	sqlite_query_str += " ORDER BY MaxAP DESC"
	c = DB.cursor()
	query_result = c.execute(sqlite_query_str).fetchall()

	if query_result is not None:
		output_result = []
		for r in query_result:
			output_result.append(r[0])
		return ', '.join(output_result)
	else:
		return 'No matches were found.'

@bot.command()
async def query(ctx, *args):
	user_query = {}
	for arg in args:
		user_query[arg.split('=')[0].lower()] = arg.split('=')[1]

	valid_query = {}
	for query in list(user_query.keys()):
		if query in supported_queries:
			valid_query[query] = user_query[query]
		else:
			pass

	if len(valid_query) > 0:
		result = get_query_result(valid_query)
		await ctx.send(f'**Result**: {result}')
	else:
		await ctx.send('Please use supported keywords (type, ap, maxap, skill, rml or rmls)')	

bot.run(TOKEN)