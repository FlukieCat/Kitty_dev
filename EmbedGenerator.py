from discord import Embed
import re

class EmbedGenerator():
	"""docstring for EmbedGenerator"""
	def __init__(self):
		self.typecolor = {"Normal":0xa8a878, "Fire":0xf08030, "Water":0x6890f0, "Grass":0x78c850, "Electric":0xf8d030, "Ice":0x98d8d8, "Fighting":0xc03028, "Poison":0xa040a0, "Ground":0xe0c068, "Flying":0xa890f0, "Psychic":0xf85888, "Bug":0xa8b820, "Rock":0xb8a038, "Ghost":0x705898, "Dragon":0x7038f8, "Dark":0x705848, "Steel":0xb8b8d0, "Fairy":0xee99ac}
		return

	def format_dex_embed(self, pokemon):
		string = f"**Dex**: {pokemon['DexNum']}\n\
		    **Type**: {pokemon['Type']}\n\
		    **AP**: {pokemon['AP']}\n\
		    **Max AP**: {pokemon['MaxAP']}\n\
		    **Max RMLs**: {pokemon['RMLs']}\n\
		    **Skill(s)**: {pokemon['Skill']}"
		other_skills = [s for s in [pokemon['Skill2'], pokemon['Skill3'], pokemon['Skill4'], pokemon['Skill5']] if s is not None]
		if len(other_skills) > 0:
			string += f" ({', '.join(other_skills).strip()})"

		embed = Embed(title=pokemon['Name'], color=self.typecolor[pokemon['Type']], description=string)
		embed.set_thumbnail(url=f"https://raw.githubusercontent.com/FlukieCat/Kitty_dev/master/shuffle_icons/{pokemon['ImgURL']}.png")
		return embed

	def ___delete_empty_items(self, l):
		return [i for i in l if i is not '']

	def format_skill_embed(self, skill):
		p = re.compile(r'[^\d\.\d]')
		proc_list = self.___delete_empty_items(p.sub(' ', skill['ProcRate']).strip().split(' '))
		multi_list = self.___delete_empty_items(p.sub(' ', skill['Multiplier']).strip().split(' '))
		sp_list = self.___delete_empty_items(p.sub(' ', skill['SkillPoints']).strip().split(' '))
		if len(proc_list) > 3:
			string = f"**Description**: {skill['Description']}. {skill['AdditionalInfo']}\n\
						**Activation Rates (SL1)**:  {proc_list[0]}% / {proc_list[1]}% / {proc_list[2]}%\n\
						**SL2 Bonus**:  {proc_list[3]}% / {proc_list[4]}% / {proc_list[5]}%\n\
						**SL3 Bonus**:  {proc_list[6]}% / {proc_list[7]}% / {proc_list[8]}%\n\
						**SL4 Bonus**:  {proc_list[9]}% / {proc_list[10]}% / {proc_list[11]}%\n\
						**SL5 Bonus**:  {proc_list[12]}% / {proc_list[13]}% / {proc_list[14]}%\n\
						**Damage Multiplier**: x{multi_list[0]}\n\
						**Skill Points**: {sp_list[0]}/ {sp_list[1]}/ {sp_list[2]}/ {sp_list[3]} (Total: {sum([int(i) for i in sp_list])})"
		else:
			string = f"**Description**: {skill['Description']} {skill['AdditionalInfo']}\n\
						**Activation Rates**:  {proc_list[0]}% / {proc_list[1]}% / {proc_list[2]}%\n\
						**Damage Multiplier (SL1)**: x{multi_list[0]}\n\
						**SL2 Bonus**: x{multi_list[1]}\n\
						**SL3 Bonus**: x{multi_list[2]}\n\
						**SL4 Bonus**: x{multi_list[3]}\n\
						**SL5 Bonus**: x{multi_list[4]}\n\
						**Skill Points**: {sp_list[0]}/ {sp_list[1]}/ {sp_list[2]}/ {sp_list[3]} (Total: {sum([int(i) for i in sp_list])})"
		
		embed = Embed(title=skill['Name'], color=self.typecolor['Grass'], description=string)
		return embed
