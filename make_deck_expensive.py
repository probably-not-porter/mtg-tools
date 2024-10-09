import json
from tqdm import tqdm
import argparse

def find_replacement(name,data):
        # get highest price version
        best_price = 0.0
        best_item = None
        worst_price = 12345678
        worst_item = None

        # list best printings
        item_list = []

        # iterate over items to find items with matching name
        for item in data:
            if item['name'] == name:
                
                item_list.append(item)

                # Find item with best price
                if item['prices']['usd'] != None:
                    if float(item['prices']['usd']) > best_price:
                        best_price  = float(item['prices']['usd'])
                        best_item = item
                if item['prices']['eur'] != None:
                    if float(item['prices']['eur']) > best_price:
                        best_price  = float(item['prices']['eur'])
                        best_item = item
                if item['prices']['usd_foil'] != None:
                    if float(item['prices']['usd_foil']) > best_price:
                        best_price  = float(item['prices']['usd_foil'])
                        best_item = item
                if item['prices']['eur_foil'] != None:
                    if float(item['prices']['eur_foil']) > best_price:
                        best_price  = float(item['prices']['eur_foil'])
                        best_item = item

                        # Find item with wrost price
                if item['prices']['usd'] != None:
                    if float(item['prices']['usd']) < worst_price:
                        worst_price  = float(item['prices']['usd'])
                        worst_item = item
                if item['prices']['eur'] != None:
                    if float(item['prices']['eur'])< worst_price:
                        worst_price  = float(item['prices']['eur'])
                        worst_item = item
                if item['prices']['usd_foil'] != None:
                    if float(item['prices']['usd_foil']) < worst_price:
                        worst_price  = float(item['prices']['usd_foil'])
                        worst_item = item
                if item['prices']['eur_foil'] != None:
                    if float(item['prices']['eur_foil']) < worst_price:
                        worst_price  = float(item['prices']['eur_foil'])
                        worst_item = item
        if worst_price == 12345678:
            worst_price = 0

        # check different printings for fullart, etc
        item_list_fullart = []
        item_list_textless = []
        item_list_promo = []
        for item in item_list:
            if (item['full_art'] == True):
                item_list_fullart.append(item)
            if (item['textless'] == True):
                item_list_textless.append(item)
            if (item['promo'] == True):
                item_list_promo.append(item)
        
        # Output
        print("---- " + name + " ----")
        print("Most expensive print of " + name + " is $" + str(best_price))
        print("Least expensive print of " + name + " is $" + str(worst_price))
        print("Total copies: " + str(len(item_list)))
        print("Fullart copies: " + str(len(item_list_fullart)))
        print("Textless copies: " + str(len(item_list_textless)))
        print("Promo copies: " + str(len(item_list_promo)))
        print("\n")
        return (best_item, best_price, worst_item, worst_price)

def load_deck(path):
    with open(path) as deck:
        lines = [line.rstrip().split(" ", 2) for line in deck]
        return lines
    
def write_deck(decklist,path):
    with open(path, "w") as deck:
        for line in decklist:
            deck.write(" ".join(line) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make a DCK file as expensive as it can be")
    parser.add_argument('-i', '--input', help='Path to input dck.', type=str, required=True)
    parser.add_argument('-o', '--output', help='Path to output dck.', type=str, required=True)
    args = parser.parse_args()


    fileread = load_deck(args.input)
    layout_lines = []
    decklist = []
    total_cost = 0.0
    min_cost = 0.0

    for line in fileread:
        if len(line) == 3 and line[0].isnumeric():
            decklist.append(line)
        if len(line) == 2 and line[0] == "LAYOUT": # grab layout lines for later
            layout_lines.append(line)

    with open('/storage/datasets/mtg-tcg/all-cards.json') as dataset:
        data = json.load(dataset)
        for card in decklist:
            r, p, r2, p2 = find_replacement(card[2],data)
            total_cost += p
            min_cost += p2
            if r != None:
                card[1] = "[" + r["set"].upper() + ":" + r["collector_number"] + "]"

    # Prepare for export
    #decklist.append(layout_lines)
    write_deck(decklist,args.output)
    print("Maximum possible Deck Cost: $" + str(total_cost))
    print("Minimum possible Deck Cost: $" + str(min_cost))