import json
import re
import sqlite3
import time


conn = sqlite3.connect('PokemonGo.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS pokedex")
c.execute("""CREATE TABLE pokedex (
    id text PRIMARY KEY,
    name text,
    dexNumber text,
    type1 text,
    type2 text,
    baseStamina integer,
    baseAttack integer,
    baseDefense integer,
    quickMoves text,
    cinematicMoves text,
    familyId text,
    form text
    )""")

conn.commit()

c.execute("DROP TABLE IF EXISTS moves")
c.execute("""CREATE TABLE moves (
    id text PRIMARY KEY,
    name text,
    dexNumber text,
    type text,
    power real,
    accuracyChance real,
    criticalChance real,
    staminaLossScalar real,
    durationMs integer,
    damageWindowStartMs integer,
    damageWindowEndMs integer,
    energyDelta integer
    )""")

conn.commit()

with open('GAME_MASTER.json', 'r') as f:
    GM = json.load(f)

GM = GM['itemTemplates']
dex_pattern = re.compile(r'(\d{4})')
pokemon_pattern = re.compile(r'^V\d{4}_POKEMON_[A-Z_]+')
move_pattern = re.compile(r'^V\d{4}_MOVE_[A-Z_]+')

tic = time.perf_counter()
for item in GM:
    if pokemon_pattern.search(item['templateId']) is not None:
        try:
            type2 = item['pokemonSettings']['type2']
        except KeyError:
            type2 = None

        try:
            form = item['form']
        except KeyError:
            form = None

        try:
            quickMoves = ','.join(item['pokemonSettings']['quickMoves'])
        except KeyError:
            quickMoves = '???'

        try:
            cinematicMoves = ','.join(item['pokemonSettings']['cinematicMoves'])
        except KeyError:
            cinematicMoves = '???'

        c.execute("""INSERT INTO pokedex VALUES(
        :id, :name, :dexNumber, :type1, :type2, :baseStamina, :baseAttack,
        :baseDefense, :quickMoves, :cinematicMoves, :familyId, :form)
        """, {'id': item['templateId'],
        'name': item['pokemonSettings']['pokemonId'],
        'dexNumber': dex_pattern.search(item['templateId']).group(),
        'type1': item['pokemonSettings']['type'],
        'type2': type2,
        'baseStamina': item['pokemonSettings']['stats']['baseStamina'],
        'baseAttack': item['pokemonSettings']['stats']['baseAttack'],
        'baseDefense': item['pokemonSettings']['stats']['baseDefense'],
        'quickMoves': quickMoves,
        'cinematicMoves': cinematicMoves,
        'familyId': item['pokemonSettings']['familyId'],
        'form': form})

        conn.commit()
    elif move_pattern.search(item['templateId']) is not None:
        try:
            criticalChance = item['moveSettings']['criticalChance']
        except KeyError:
            criticalChance = 0.0

        try:
            staminaLossScalar = item['moveSettings']['staminaLossScalar']
        except KeyError:
            staminaLossScalar = 0.0

        try:
            energyDelta = item['moveSettings']['energyDelta']
        except KeyError:
            energyDelta = 0

        try:
            power = item['moveSettings']['power']
        except KeyError:
            power = 0.0


        c.execute("""INSERT INTO moves VALUES(
        :id, :name, :dexNumber, :type, :power, :accuracyChance,
        :criticalChance, :staminaLossScalar, :durationMs,
        :damageWindowStartMs, :damageWindowEndMs, :energyDelta)
        """, {'id': item['templateId'],
        'name': item['moveSettings']['movementId'],
        'dexNumber': dex_pattern.search(item['templateId']).group(),
        'type': item['moveSettings']['pokemonType'],
        'power': power,
        'accuracyChance': item['moveSettings']['accuracyChance'],
        'criticalChance': criticalChance,
        'staminaLossScalar': staminaLossScalar,
        'durationMs': item['moveSettings']['durationMs'],
        'damageWindowStartMs': item['moveSettings']['damageWindowStartMs'],
        'damageWindowEndMs': item['moveSettings']['damageWindowEndMs'],
        'energyDelta': energyDelta})

        conn.commit()
    else:
        pass

conn.commit()
conn.close()

print(f'Data parsing finished in {time.perf_counter()-tic} seconds')
