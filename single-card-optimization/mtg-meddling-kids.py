# https://gatherer.wizards.com/pages/card/Discussion.aspx?multiverseid=74347

# Search for best words for Meddling Kids
# python3 mtg-meddling-kids.py -i /storage/datasets/mtg-tcg/oracle-cards.json
import json
from tqdm import tqdm
import argparse
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search for combos for Meddling Kids.")
    parser.add_argument('-i', '--input', help='Path to input dataset.', type=str, required=True)
    parser.add_argument('-l', '--length', help='Minimum word length', type=int, default=4)
    parser.add_argument('-n', '--num_results', help='Number of results to show', type=int, default=10)

    args = parser.parse_args()

    with open(args.input) as dataset:
        data = json.load(dataset)
        scores = {}
        total_cards = 0
        for item in tqdm(data):
            total_cards += 1
            alltext = ""
            if "oracle_text" in item: alltext += item['oracle_text'] + " "
            if "flavor_text" in item: alltext += item['flavor_text'] + " "

            alltext = re.sub(r'[^\w\s]', '', alltext)

            words_unfiltered = list(set(alltext.split()))

            for x in words_unfiltered:
                if x.isalpha() and len(x) > (args.length - 1):
                    word = x.lower()
                    if word in scores:
                        scores[word] += 1
                    else:
                        scores[word] = 1

        count = 0
        print("\n")
        for k, v in sorted(scores.items(), key=lambda k: k[1], reverse=True):
            if count == args.num_results: break
            else: count += 1
            print(f'#{count}. "{k}" - {str(round(v / total_cards * 100, 2))}% of cards')


        