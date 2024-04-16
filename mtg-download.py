import urllib.request, json 
from tqdm import tqdm
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download MTG json files from scryfall")
    parser.add_argument('-o', '--output', help='Filesystem path for all json files to be saved to', type=str, required=True)
    args = parser.parse_args()

    path = args.output
    if path[:-1] != "/":
        path += "/"

    with urllib.request.urlopen("https://api.scryfall.com/bulk-data") as url:
        data = json.load(url)
        for item in data['data']:
            name = item['name'].lower() + ".json"
            print("Downloading " + name + "...")
            with urllib.request.urlopen(item['download_uri']) as url2:
                data2 = json.load(url2)
                with open(path + name.replace(" ", "-"), 'w') as f:
                    json.dump(data2, f)