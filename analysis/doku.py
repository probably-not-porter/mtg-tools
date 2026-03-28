import pandas as pd
import json
import numpy as np
import sqlite3
from itertools import combinations
from tqdm import tqdm

# --- CONFIGURATION ---
MIN_CARDS_PER_CELL = 1
DB_PATH = "mtg_grids.db"

opt = [
    {"cat": "color", "value": "W"}, {"cat": "color", "value": "U"},
    {"cat": "color", "value": "B"}, {"cat": "color", "value": "R"},
    {"cat": "color", "value": "G"}, {"cat": "type", "value": "Land"},
    {"cat": "type", "value": "Creature"}, {"cat": "type", "value": "Artifact"},
    {"cat": "type", "value": "Enchantment"}, {"cat": "type", "value": "Planeswalker"},
    {"cat": "type", "value": "Instant"}, {"cat": "type", "value": "Sorcery"},
    {"cat": "cmc", "value": 0}, {"cat": "cmc", "value": 1},
    {"cat": "cmc", "value": 2}, {"cat": "cmc", "value": 3},
    {"cat": "cmc", "value": 4}, {"cat": "cmc", "value": 5},
    {"cat": "cmc", "value": 6}, {"cat": "cmc", "value": 7},
    {"cat": "cmc", "value": 8}, {"cat": "cmc", "value": 9},
    {"cat": "cmc", "value": 10},
    {"cat": "subtype", "value": "Human"}, {"cat": "subtype", "value": "Warrior"},
    {"cat": "subtype", "value": "Wizard"}, {"cat": "subtype", "value": "Soldier"},
    {"cat": "subtype", "value": "Spirit"}, {"cat": "subtype", "value": "Elf"},
    {"cat": "subtype", "value": "Elemental"}, {"cat": "subtype", "value": "Cleric"},
    {"cat": "subtype", "value": "Zombie"}, {"cat": "subtype", "value": "Rogue"},
    {"cat": "subtype", "value": "Goblin"}, {"cat": "subtype", "value": "Beast"},
    {"cat": "subtype", "value": "Knight"}, {"cat": "subtype", "value": "Phyrexian"},
    {"cat": "subtype", "value": "Shaman"}, {"cat": "subtype", "value": "Bird"},
    {"cat": "subtype", "value": "Dragon"}, {"cat": "subtype", "value": "Vampire"},
    {"cat": "subtype", "value": "Druid"}, {"cat": "subtype", "value": "Cat"},
    {"cat": "subtype", "value": "Horror"}, {"cat": "subtype", "value": "Merfolk"},
    {"cat": "subtype", "value": "Insect"}, {"cat": "subtype", "value": "Angel"},
    {"cat": "subtype", "value": "Scout"}, {"cat": "subtype", "value": "Artificer"},
    {"cat": "subtype", "value": "Construct"}, {"cat": "subtype", "value": "Giant"},
    {"cat": "subtype", "value": "Dinosaur"}, {"cat": "subtype", "value": "Demon"},
    {"cat": "subtype", "value": "Ally"}, {"cat": "subtype", "value": "Noble"},
    {"cat": "subtype", "value": "Warlock"}, {"cat": "subtype", "value": "Eldrazi"},
    {"cat": "subtype", "value": "Mutant"}, {"cat": "subtype", "value": "Lizard"},
    {"cat": "subtype", "value": "Snake"}, {"cat": "subtype", "value": "Pirate"},
    {"cat": "subtype", "value": "Faerie"}, {"cat": "subtype", "value": "Monk"},
    {"cat": "subtype", "value": "Shapeshifter"}, {"cat": "subtype", "value": "Golem"},
    {"cat": "subtype", "value": "Advisor"}, {"cat": "subtype", "value": "Wall"},
    {"cat": "subtype", "value": "Avatar"}, {"cat": "subtype", "value": "Assassin"},
    {"cat": "subtype", "value": "Dog"}, {"cat": "subtype", "value": "Berserker"},
    {"cat": "subtype", "value": "Dwarf"}, {"cat": "subtype", "value": "Spider"},
    {"cat": "subtype", "value": "Ogre"}, {"cat": "subtype", "value": "Ninja"},
    {"cat": "subtype", "value": "Rat"}, {"cat": "subtype", "value": "Treefolk"},
    {"cat": "subtype", "value": "Wurm"}, {"cat": "subtype", "value": "Robot"},
    {"cat": "subtype", "value": "Sliver"}, {"cat": "subtype", "value": "Minotaur"},
    {"cat": "subtype", "value": "Archer"}, {"cat": "subtype", "value": "Orc"},
    {"cat": "subtype", "value": "Illusion"}, {"cat": "subtype", "value": "Citizen"},
    {"cat": "subtype", "value": "Drake"}, {"cat": "subtype", "value": "Plant"},
    {"cat": "subtype", "value": "Nightmare"}, {"cat": "subtype", "value": "Wolf"}
]

# --- DATA LOADING ---
print("Loading dataset...")
df = pd.DataFrame(json.load(open("/storage/datasets/mtg-tcg/oracle-cards.json")))

cat_sets = {}
print("Building category sets...")
for item in tqdm(opt):
    key = f"{item['cat']}_{item['value']}"
    if item['cat'] == 'color':
        cat_sets[key] = set(df[df['colors'].apply(lambda x: isinstance(x, list) and item['value'] in x)]['name'])
    elif item['cat'] in ['type', 'subtype']:
        cat_sets[key] = set(df[df['type_line'].str.contains(item['value'], na=False, case=True)]['name'])
    elif item['cat'] == 'cmc':
        cat_sets[key] = set(df[df['cmc'] == item['value']]['name'])

n = len(opt)
matrix = np.zeros((n, n), dtype=bool)

print("Building Intersection Matrix...")
for i in range(n):
    for j in range(i, n):
        k1, k2 = f"{opt[i]['cat']}_{opt[i]['value']}", f"{opt[j]['cat']}_{opt[j]['value']}"
        if len(cat_sets[k1] & cat_sets[k2]) >= MIN_CARDS_PER_CELL:
            matrix[i, j] = matrix[j, i] = True

def is_axis_valid(group_indices):
    cats = [opt[i]['cat'] for i in group_indices]
    for c in set(cats):
        if cats.count(c) > 1 and c not in ['subtype', 'type', 'color']:
            return False
    return True

def save_to_sqlite(grids):
    print(f"Saving {len(grids):,} results to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("DROP TABLE IF EXISTS valid_grids")
    cursor.execute("""
        CREATE TABLE valid_grids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            r1 TEXT, r2 TEXT, r3 TEXT,
            c1 TEXT, c2 TEXT, c3 TEXT
        )
    """)
    
    # Batch insert for speed
    cursor.executemany("""
        INSERT INTO valid_grids (r1, r2, r3, c1, c2, c3) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, grids)
    
    conn.commit()
    conn.close()
    print("Done!")

def find_and_store_grids():
    raw_candidates = list(combinations(range(len(opt)), 3))
    filtered = [c for c in raw_candidates if is_axis_valid(c)]
    
    batch_results = []
    print(f"Searching {len(filtered)**2:,} combinations...")

    for r in tqdm(filtered):
        for c in filtered:
            if set(r) & set(c): continue
            
            conflict = False
            exclusive = ['cmc'] 
            for r_idx in r:
                for c_idx in c:
                    if opt[r_idx]['cat'] == opt[c_idx]['cat'] and opt[r_idx]['cat'] in exclusive:
                        conflict = True
                        break
                if conflict: break
            
            if conflict: continue

            if (matrix[r[0], c[0]] and matrix[r[0], c[1]] and matrix[r[0], c[2]] and
                matrix[r[1], c[0]] and matrix[r[1], c[1]] and matrix[r[1], c[2]] and
                matrix[r[2], c[0]] and matrix[r[2], c[1]] and matrix[r[2], c[2]]):
                
                # We store the raw strings for the database
                batch_results.append((
                    f"{opt[r[0]]['cat']}:{opt[r[0]]['value']}",
                    f"{opt[r[1]]['cat']}:{opt[r[1]]['value']}",
                    f"{opt[r[2]]['cat']}:{opt[r[2]]['value']}",
                    f"{opt[c[0]]['cat']}:{opt[c[0]]['value']}",
                    f"{opt[c[1]]['cat']}:{opt[c[1]]['value']}",
                    f"{opt[c[2]]['cat']}:{opt[c[2]]['value']}"
                ))
                
    save_to_sqlite(batch_results)

# --- EXECUTION ---
find_and_store_grids()