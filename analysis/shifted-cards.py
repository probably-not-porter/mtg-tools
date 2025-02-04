# python3 shifted-cards.py -i /storage/datasets/mtg-tcg/all-cards.json

import json
from tqdm import tqdm
import argparse
from datetime import datetime

cardnames = {}

def main(path):
    print("name, first set, first rarity, first date, earliest non-common set, earliest non-common rarity, earliest non-common date, downshift set, downshift rarity, downshift date")
    with open(path) as dataset:
        data = json.load(dataset)

        for item in data:
            if item["name"] not in cardnames:
                cardnames[item["name"]] = []
            cardnames[item["name"]].append(item)

        for key, value in cardnames.items():
            if check_for_common(value) and check_for_non_common(value):
                check_for_downshift(value)




def check_for_common(cardlist):
    for card in cardlist:
        if "type_line" in card:
            if "Token" not in card["type_line"]:
                if card["rarity"] == "common":
                    return True
    return False

def check_for_non_common(cardlist):
    for card in cardlist:
        if "type_line" in card:
            if "Token" not in card["type_line"]:
                if card["rarity"] != "common":
                    return True
    return False

def check_for_downshift(cardlist):
    cardlist = sort_by_date(cardlist)
    card0 = cardlist[0]
    for card1 in cardlist:
        for card2 in cardlist:
            if "type_line" in card1 and "type_line" in card2:
                if "Token" not in card1["type_line"] and "Token" not in card2["type_line"]:
                    if compare_dates(card1["released_at"], card2["released_at"]):
                        if card1["rarity"] != "common" and card2["rarity"] == "common":
                            #print(card1["name"], card1["released_at"], card1["rarity"], card1["set_name"])
                            #print(card2["name"], card2["released_at"], card2["rarity"], card2["set_name"])
                            # 
                            print(f'{card0["name"]}, {card0["set_name"]}, {card0["rarity"]}, {card0["released_at"]}, {card1["set_name"]}, {card1["rarity"]}, {card1["released_at"]}, {card2["set_name"]}, {card2["rarity"]}, {card2["released_at"]},')
                            return True
    return False



def compare_dates(date1: str, date2: str) -> str:
    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)
    if d1 < d2:
        return True
    return False

def sort_by_date(items: list) -> list:
    return sorted(items, key=lambda x: datetime.strptime(x["released_at"], "%Y-%m-%d"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="new")
    parser.add_argument('-i', '--input', help='Path to input dataset.', type=str)

    args = parser.parse_args()

    main(path = args.input)
