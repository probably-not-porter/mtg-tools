# https://gatherer.wizards.com/pages/card/Discussion.aspx?multiverseid=74347

# Search for best words for Meddling Kids
# python3 mtg-meddling-kids.py -i /storage/datasets/mtg-tcg/all-cards.json
import json
from tqdm import tqdm
import argparse
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search for combos for Meddling Kids.")
    parser.add_argument('-i', '--input', help='Path to input dataset.', type=str)

    args = parser.parse_args()

    with open(args.input) as dataset:
        data = json.load(dataset)
        scores = {}
        for item in tqdm(data):
            alltext = ""
            if "oracle_text" in item: alltext += item['oracle_text'] + " "
            if "flavor_text" in item: alltext += item['flavor_text'] + " "

            alltext = re.sub(r'[^\w\s]', '', alltext)

            words_unfiltered = alltext.split()

            for x in words_unfiltered:
                if x.isalpha() and len(x) > 3:
                    word = x.lower()
                    if word in scores:
                        scores[word] += 1
                    else:
                        scores[word] = 1

        count = 0
        for k, v in sorted(scores.items(), key=lambda k: k[1], reverse=True):
            if count == 100: break
            else : count += 1

            cards_with = 0

            for item in data:
                alltext = ""
                if "oracle_text" in item: alltext += item['oracle_text'] + " "
                if "flavor_text" in item: alltext += item['flavor_text'] + " "

                if k in alltext.lower():
                    cards_with += 1

            print("Word: " + k + ", Score: " + str(v) + ", Cards with word: " + str(cards_with) + "/" + str(len(data)) + " (" + str(round(cards_with / len(data) * 100, 2)) + "%)")


        