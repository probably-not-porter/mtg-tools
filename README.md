# Misc MTG Scripts
Some other mtg related scripts and bits.

## mtg-download.py
Locate and download the newest bulk data from Scryfall.

`all-cards.json`  `default-cards.json`  `oracle-cards.json`  `rulings.json`  `unique-artwork.json`


```sh
python3 mtg-download.py -o /storage/datasets/mtg-tcg
```

## mtg-abc.py
Find the best combos for Now I Know My ABC's
```sh
python3 mtg-abc.py \
  -i /storage/datasets/mtg-tcg/oracle-cards.json \
  -n 10 \
  -v 1000000 \
  -m 5 \
  -c W U B R G
```

