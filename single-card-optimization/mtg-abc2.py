# https://gatherer.wizards.com/pages/card/Details.aspx?multiverseid=73959

# Search for combos for Now I Know My ABCs
# python3 mtg-abc.py -i /storage/datasets/mtg-tcg/all-cards.json
import json
from tqdm import tqdm
import argparse
alphabet = set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])

def find_combos(path):
    print("┌ Reading dataset file...")
    winners = {
        "A": {
            'count': 0,
            'name': None
        },
        "B": {
            'count': 0,
            'name': None
        },
        "C": {
            'count': 0,
            'name': None
        },
        "D": {
            'count': 0,
            'name': None
        },
        "E": {
            'count': 0,
            'name': None
        },
        "F": {
            'count': 0,
            'name': None
        },
        "G": {
            'count': 0,
            'name': None
        },
        "H": {
            'count': 0,
            'name': None
        },
        "I": {
            'count': 0,
            'name': None
        },
        "J": {
            'count': 0,
            'name': None
        },
        "K": {
            'count': 0,
            'name': None
        },
        "L": {
            'count': 0,
            'name': None
        },
        "M": {
            'count': 0,
            'name': None
        },
        "N": {
            'count': 0,
            'name': None
        },
        "O": {
            'count': 0,
            'name': None
        },
        "P": {
            'count': 0,
            'name': None
        },
        "Q": {
            'count': 0,
            'name': None
        },
        "R": {
            'count': 0,
            'name': None
        },
        "S": {
            'count': 0,
            'name': None
        },
        "T": {
            'count': 0,
            'name': None
        },
        "U": {
            'count': 0,
            'name': None
        },
        "V": {
            'count': 0,
            'name': None
        },
        "W": {
            'count': 0,
            'name': None
        },
        "X": {
            'count': 0,
            'name': None
        },
        "Y": {
            'count': 0,
            'name': None
        },
        "Z": {
            'count': 0,
            'name': None
        },
    }
    with open(path) as dataset:
        data = json.load(dataset)
        for item in data:
            cardname = item["name"].replace(" (cont'd)","")

            if cardname.split(" // ")[0] == cardname.split(" // ")[-1]:
                cardname = cardname.split(" // ")[0]
            if len(cardname.split(" // ")) == 4:
                if cardname.split(" // ")[0:1] == cardname.split(" // ")[2:3]:
                    cardname = " // ".join(cardname.split(" // ")[0:1])
            for letter in alphabet:
                occ = cardname.upper().count(letter.upper())
                if occ > winners[letter.upper()]['count']:
                    winners[letter.upper()]['count'] = occ
                    winners[letter.upper()]['name'] = cardname
    for entry in winners:
        print(f"{winners[entry]['count']}x {entry}: {winners[entry]['name']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search for combos for Now I Know My ABC's.")
    parser.add_argument('-i', '--input', help='Path to input dataset.', type=str)
    args = parser.parse_args()

    find_combos(path = args.input)
