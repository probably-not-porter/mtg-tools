# Misc MTG Scripts
Some other mtg related scripts and bits.

## `mtg-download.py`
Locate and download the newest bulk data from Scryfall.

`all-cards.json`  `default-cards.json`  `oracle-cards.json`  `rulings.json`  `unique-artwork.json`


```sh
python3 mtg-download.py -o /storage/datasets/mtg-tcg
```

## `mtg-abc.py`
Find the best combos for Now I Know My ABC's. Attempts to score every card based on the rarity of the letters its name contains, then match them up to create full alphabets. Includes letters from "Now I Know My ABC's" by default. WARNING: This can take a long time if you use a gigantic `v` value.
```sh
python3 mtg-abc.py \
  -i /storage/datasets/mtg-tcg/oracle-cards.json \
  -n 10 \
  -v 1000000 \
  -m 5 \
  -c W U B R G
```
## `mtg-meddling-kids.py`
Find the most common words on all cards. Works best with the "all-cards" dataset. 
```sh
python3 mtg-abc.py -i /storage/datasets/mtg-tcg/all-cards.json
```


# Sample Card

```json
{
    "object":"card",
    "id":"f3c92575-1c97-48bf-801b-22f34040cf9a",
    "oracle_id":"00d3fcdf-6959-4437-9bad-93a8625510a1",
    "multiverse_ids":[
       180498
    ],
    "mtgo_id":34370,
    "mtgo_foil_id":34371,
    "tcgplayer_id":33316,
    "cardmarket_id":21903,
    "name":"Guul Draz Vampire",
    "lang":"en",
    "released_at":"2009-10-02",
    "uri":"https://api.scryfall.com/cards/f3c92575-1c97-48bf-801b-22f34040cf9a",
    "scryfall_uri":"https://scryfall.com/card/zen/93/guul-draz-vampire?utm_source=api",
    "layout":"normal",
    "highres_image":true,
    "image_status":"highres_scan",
    "image_uris":{
       "small":"https://cards.scryfall.io/small/front/f/3/f3c92575-1c97-48bf-801b-22f34040cf9a.jpg?1562618316",
       "normal":"https://cards.scryfall.io/normal/front/f/3/f3c92575-1c97-48bf-801b-22f34040cf9a.jpg?1562618316",
       "large":"https://cards.scryfall.io/large/front/f/3/f3c92575-1c97-48bf-801b-22f34040cf9a.jpg?1562618316",
       "png":"https://cards.scryfall.io/png/front/f/3/f3c92575-1c97-48bf-801b-22f34040cf9a.png?1562618316",
       "art_crop":"https://cards.scryfall.io/art_crop/front/f/3/f3c92575-1c97-48bf-801b-22f34040cf9a.jpg?1562618316",
       "border_crop":"https://cards.scryfall.io/border_crop/front/f/3/f3c92575-1c97-48bf-801b-22f34040cf9a.jpg?1562618316"
    },
    "mana_cost":"{B}",
    "cmc":1.0,
    "type_line":"Creature — Vampire Rogue",
    "oracle_text":"As long as an opponent has 10 or less life, Guul Draz Vampire gets +2/+1 and has intimidate. (It can't be blocked except by artifact creatures and/or creatures that share a color with it.)",
    "power":"1",
    "toughness":"1",
    "colors":[
       "B"
    ],
    "color_identity":[
       "B"
    ],
    "keywords":[
       
    ],
    "legalities":{
       "standard":"not_legal",
       "future":"not_legal",
       "historic":"not_legal",
       "timeless":"not_legal",
       "gladiator":"not_legal",
       "pioneer":"not_legal",
       "explorer":"not_legal",
       "modern":"legal",
       "legacy":"legal",
       "pauper":"legal",
       "vintage":"legal",
       "penny":"legal",
       "commander":"legal",
       "oathbreaker":"legal",
       "standardbrawl":"not_legal",
       "brawl":"not_legal",
       "alchemy":"not_legal",
       "paupercommander":"legal",
       "duel":"legal",
       "oldschool":"not_legal",
       "premodern":"not_legal",
       "predh":"legal"
    },
    "games":[
       "paper",
       "mtgo"
    ],
    "reserved":false,
    "foil":true,
    "nonfoil":true,
    "finishes":[
       "nonfoil",
       "foil"
    ],
    "oversized":false,
    "promo":false,
    "reprint":false,
    "variation":false,
    "set_id":"eb16a2bd-a218-4e4e-8339-4aa1afc0c8d2",
    "set":"zen",
    "set_name":"Zendikar",
    "set_type":"expansion",
    "set_uri":"https://api.scryfall.com/sets/eb16a2bd-a218-4e4e-8339-4aa1afc0c8d2",
    "set_search_uri":"https://api.scryfall.com/cards/search?order=set&q=e%3Azen&unique=prints",
    "scryfall_set_uri":"https://scryfall.com/sets/zen?utm_source=api",
    "rulings_uri":"https://api.scryfall.com/cards/f3c92575-1c97-48bf-801b-22f34040cf9a/rulings",
    "prints_search_uri":"https://api.scryfall.com/cards/search?order=released&q=oracleid%3A00d3fcdf-6959-4437-9bad-93a8625510a1&unique=prints",
    "collector_number":"93",
    "digital":false,
    "rarity":"common",
    "flavor_text":"\"A creature\\'s bloodscent is a beacon that cannot be disguised.\"",
    "card_back_id":"0aeebaf5-8c7d-4636-9e82-8c27447861f7",
    "artist":"Steve Argyle",
    "artist_ids":[
       "a44ddda4-5331-4f83-aac9-3e00ed36bd7b"
    ],
    "illustration_id":"08d0c629-84f0-4d01-a98a-80ab9b57a2dd",
    "border_color":"black",
    "frame":"2003",
    "full_art":false,
    "textless":false,
    "booster":true,
    "story_spotlight":false,
    "edhrec_rank":16866,
    "penny_rank":4401,
    "prices":{
       "usd":"0.22",
       "usd_foil":"3.72",
       "usd_etched":"None",
       "eur":"0.20",
       "eur_foil":"1.57",
       "tix":"0.03"
    },
    "related_uris":{
       "gatherer":"https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=180498&printed=false",
       "tcgplayer_infinite_articles":"https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&trafcat=infinite&u=https%3A%2F%2Finfinite.tcgplayer.com%2Fsearch%3FcontentMode%3Darticle%26game%3Dmagic%26partner%3Dscryfall%26q%3DGuul%2BDraz%2BVampire",
       "tcgplayer_infinite_decks":"https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&trafcat=infinite&u=https%3A%2F%2Finfinite.tcgplayer.com%2Fsearch%3FcontentMode%3Ddeck%26game%3Dmagic%26partner%3Dscryfall%26q%3DGuul%2BDraz%2BVampire",
       "edhrec":"https://edhrec.com/route/?cc=Guul+Draz+Vampire"
    },
    "purchase_uris":{
       "tcgplayer":"https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F33316%3Fpage%3D1",
       "cardmarket":"https://www.cardmarket.com/en/Magic/Products/Singles/Zendikar/Guul-Draz-Vampire?referrer=scryfall&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
       "cardhoarder":"https://www.cardhoarder.com/cards/34370?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
    }
 }
```