# Search for combos for Now I Know My ABCs
# https://gatherer.wizards.com/pages/card/Details.aspx?multiverseid=73959
# python3 mtg-abc.py -i /storage/datasets/mtg-tcg/all-cards.json
import json
from tqdm import tqdm
import argparse

MAX_SEARCH = 10000000
alphabet = set(['d', 'e', 'f', 'g', 'h', 'j', 'l', 'p', 'q', 'r', 't', 'u', 'v', 'x', 'z'])

def ispangram(input_string):
    return set(input_string.lower()) >= alphabet

def ispermanent(card):
    if 'type_line' in card.keys():
        if "creature" in card['type_line'].lower():
            return True
        if "land" in card['type_line'].lower():
            return True
        if "enchantment" in card['type_line'].lower():
            return True
        if "artifact" in card['type_line'].lower():
            return True
        if "planeswalker" in card['type_line'].lower():
            return True
        if "battle" in card['type_line'].lower():
            return True
    return False

def print_combos(comboset):
    if len(comboset) == 0:
        print("╟ No Combos found")
        print("╠════")
    for item in comboset:
        print("╟ Score: " + str(round(item['value'], 2)))
        for x in item['cards']:
            print("╟ " + x)
        print("╠════")

def filter_data(data, cmcmax, colors):

    outdata = []
    for item in data:
        if ispermanent(item) and item["cmc"] <= cmcmax:
             if set(item['color_identity']) <= set(colors):
                if "//" not in item['name']:                # maybe 
                    outdata.append(item)
    return outdata

def find_combos(n, cmcmax, colors, path):
    print("┌ Reading dataset file...")
    with open(path) as dataset:
        data = json.load(dataset)
        print("├ Dataset loaded!")
        print('├ Filtering...')
        data = filter_data(data, cmcmax, colors)
        scores = {}

        letters = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, 
                   "g": 0, "h": 0, "i": 0, "j": 0, "k": 0, "l": 0, 
                   "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, 
                   "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, 
                   "y": 0, "z": 0
        }
        print('├ Tallying alph characters...')
        for item in data:
            for alph in list(alphabet):
                if alph in item["name"].lower():
                    letters[alph] += 1

        print('├ Scoring...')
        for item in data:
            item_score = 0
            for alph in list(alphabet):
                if alph in item["name"].lower():
                    item_score += 1000 / letters[alph] 
            item_score -= int(item['cmc'])
            scores[item["name"]] = item_score

        count = 1
        print("├ Top ten most valuable cards:")
        for k, v in sorted(scores.items(), key=lambda k: k[1], reverse=True):
            if count == 11: break
            else:
                print("├─── Num #" + str(count) + ": " + str(k) + " --- " + str(round(v, 4)))
                count += 1


        print("├ Searching...")
        single_combos = find_single(scores,n)
        double_combos = find_double(scores,n)
        triple_combos = find_triple(scores,n)
        
        print("\n╔═ One Card Combos ════")
        print_combos(single_combos)
        print("\n╔═ Two Card Combos ════")
        print_combos(double_combos)
        print("\n╔═ Three Card Combos ════")
        print_combos(triple_combos)

        return 0

def find_single(scores,n):
    print('├─ Searching single cards')
    combos = []
    pbar = tqdm(total=min([len(scores.items()), MAX_SEARCH]), leave=False)
    count = 0
    for k, v in sorted(scores.items(), key=lambda k: k[1], reverse=True):
        if count > MAX_SEARCH: return combos
        count += 1
        pbar.update(1)
        if ispangram(k):
            combos.append({
                "cards": [k], 
                "value": v
            })
            if len(combos) == n:
                return combos
    return combos

def find_double(scores,n):
    print('├─ Searching double cards')
    combos = []
    pbar = tqdm(total=min([len(scores.items())**2, MAX_SEARCH]), leave=False)
    count = 0
    for k, v in sorted(scores.items(), key=lambda k: k[1], reverse=True):
        for k2, v2 in sorted(scores.items(), key=lambda k: k[1], reverse=True):
            if count > MAX_SEARCH: return combos
            count += 1
            pbar.update(1)
            if ispangram(k+k2):
                combos.append({
                    "cards": [k,k2], 
                    "value": (v+v2) / 2
                })
                if len(combos) == n:
                    return combos
    return combos

def find_triple(scores,n):
    print('├─ Searching triple cards')
    combos = []
    pbar = tqdm(total=min([len(scores.items())**3, MAX_SEARCH]), leave=False)
    count = 0
    for k, v in sorted(scores.items(), key=lambda k: k[1], reverse=True):
        for k2, v2 in sorted(scores.items(), key=lambda k: k[1], reverse=True):
            for k3, v3 in sorted(scores.items(), key=lambda k: k[1], reverse=True):
                if count > MAX_SEARCH: return combos
                count += 1
                pbar.update(1)
                if ispangram(k+k2+k3):
                    combos.append({
                        "cards": [k,k2,k3], 
                        "value": (v+v2+v3) / 3
                    })
                    if len(combos) == n:
                        return combos
    return combos

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search for combos for Now I Know My ABC's.")
    parser.add_argument('-i', '--input', help='Path to input dataset.', type=str)
    parser.add_argument('-n', '--num', help='Number of results to generate in each catagory.', type=int)
    parser.add_argument('-v', '--volume', help='Volume of results to check.', type=int)
    parser.add_argument('-m', '--maxcmc', help='Maximum CMC of cards to search for.', type=int)
    parser.add_argument('-c', '--colors', help='Color of cards to search for.', nargs='+', default=[])
    args = parser.parse_args()

    if args.volume != None:
        MAX_SEARCH = args.volume

    if set(args.colors) <= set(['U','W','B','R','G']):
        find_combos(n = args.num, cmcmax = args.maxcmc, colors = args.colors, path = args.input)
    else:
        print("Something wrong with the colors...")