import pandas as pd
import json
import numpy as np
import sqlite3
from itertools import combinations
from tqdm import tqdm

# --- CONFIGURATION ---
MIN_CARDS_PER_CELL = 1
DB_PATH = "mtg_relational_grids.db"
BATCH_SIZE = 50000 

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

# --- 1. DATA PREP ---
print("Loading dataset...")
df = pd.DataFrame(json.load(open("/storage/datasets/mtg-tcg/oracle-cards.json")))

cat_sets = {}
for item in tqdm(opt, desc="Building Sets"):
    key = f"{item['cat']}_{item['value']}"
    if item['cat'] == 'color':
        cat_sets[key] = set(df[df['colors'].apply(lambda x: isinstance(x, list) and item['value'] in x)]['name'])
    elif item['cat'] in ['type', 'subtype']:
        cat_sets[key] = set(df[df['type_line'].str.contains(item['value'], na=False, case=True)]['name'])
    elif item['cat'] == 'cmc':
        cat_sets[key] = set(df[df['cmc'] == item['value']]['name'])

n = len(opt)
matrix = np.zeros((n, n), dtype=bool)
for i in range(n):
    for j in range(i, n):
        k1, k2 = f"{opt[i]['cat']}_{opt[i]['value']}", f"{opt[j]['cat']}_{opt[j]['value']}"
        if len(cat_sets[k1] & cat_sets[k2]) >= MIN_CARDS_PER_CELL:
            matrix[i, j] = matrix[j, i] = True

def is_axis_valid(group_indices):
    cats = [opt[i]['cat'] for i in group_indices]
    for c in set(cats):
        if cats.count(c) > 1 and c in ['cmc']: return False
    return True

# --- 2. DATABASE INITIALIZATION ---
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA synchronous = OFF") # Speed boost for massive inserts
cursor.execute("PRAGMA journal_mode = MEMORY")

cursor.executescript("""
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS trios;
    DROP TABLE IF EXISTS compatible_pairs;

    CREATE TABLE categories (id INTEGER PRIMARY KEY, cat TEXT, value TEXT);
    CREATE TABLE trios (id INTEGER PRIMARY KEY, c1_idx INT, c2_idx INT, c3_idx INT);
    CREATE TABLE compatible_pairs (row_trio_id INT, col_trio_id INT);
""")

# Store Categories
cursor.executemany("INSERT INTO categories VALUES (?, ?, ?)", 
                   [(i, x['cat'], str(x['value'])) for i, x in enumerate(opt)])

# Store Valid Trios
raw_trios = list(combinations(range(len(opt)), 3))
valid_trios = [t for t in raw_trios if is_axis_valid(t)]
cursor.executemany("INSERT INTO trios (id, c1_idx, c2_idx, c3_idx) VALUES (?, ?, ?, ?)", 
                   [(i, t[0], t[1], t[2]) for i, t in enumerate(valid_trios)])
conn.commit()

# --- 3. EFFICIENT GRID SOLVER ---
def find_and_store_pairs():
    batch = []
    total_saved = 0
    
    print(f"Finding compatible pairs among {len(valid_trios):,} trios...")
    for r_id, r_trio in enumerate(tqdm(valid_trios)):
        for c_id, c_trio in enumerate(valid_trios):
            # 1. Axis Overlap Check
            if set(r_trio) & set(c_trio): continue
            
            # 2. Mutually Exclusive Categories (CMC vs CMC)
            conflict = False
            for ri in r_trio:
                for ci in c_trio:
                    if opt[ri]['cat'] == opt[ci]['cat'] and opt[ri]['cat'] == 'cmc':
                        conflict = True; break
                if conflict: break
            if conflict: continue

            # 3. Fast Matrix Check (All 9 cells must be True)
            if (matrix[r_trio[0], c_trio[0]] and matrix[r_trio[0], c_trio[1]] and matrix[r_trio[0], c_trio[2]] and
                matrix[r_trio[1], c_trio[0]] and matrix[r_trio[1], c_trio[1]] and matrix[r_trio[1], c_trio[2]] and
                matrix[r_trio[2], c_trio[0]] and matrix[r_trio[2], c_trio[1]] and matrix[r_trio[2], c_trio[2]]):
                
                batch.append((r_id, c_id))

                if len(batch) >= BATCH_SIZE:
                    cursor.executemany("INSERT INTO compatible_pairs VALUES (?, ?)", batch)
                    conn.commit()
                    total_saved += len(batch)
                    batch = []

    if batch:
        cursor.executemany("INSERT INTO compatible_pairs VALUES (?, ?)", batch)
        conn.commit()
        total_saved += len(batch)
    
    # Create an index for lightning fast random queries
    print("Creating index...")
    cursor.execute("CREATE INDEX idx_pairs ON compatible_pairs(row_trio_id, col_trio_id)")
    conn.close()
    print(f"Finished! Total compatible pairs saved: {total_saved:,}")

find_and_store_pairs()