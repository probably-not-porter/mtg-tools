# Download all sets of card data from scryfall API.
# python3 mtg-download.py -o /storage/datasets/mtg-tcg/
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request("https://api.scryfall.com/bulk-data", headers=headers)
    with urllib.request.urlopen(req) as url:
        data = json.load(url)
        for item in data['data']:
            name = item['name'].lower() + ".json"
            print("Downloading " + name + "...")
            download_req = urllib.request.Request(item['download_uri'], headers=headers)
            with urllib.request.urlopen(download_req) as url2:
                data2 = json.load(url2)
                with open(path + name.replace(" ", "-"), 'w') as f:
                    json.dump(data2, f)