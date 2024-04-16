import urllib.request, json 
with urllib.request.urlopen("https://api.scryfall.com/bulk-data") as url:
    data = json.load(url)
    print(data)