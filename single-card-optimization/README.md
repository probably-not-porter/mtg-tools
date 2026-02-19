# Single Card Optimizers
## `mtg-meddling-kids.py`
Find the most common words on all cards. Works best with the "all-cards" dataset. 

<img src='https://cards.scryfall.io/large/front/5/c/5c86f1b5-d95d-4f44-8078-4572101997b4.jpg?1562488401' height=250px>

```sh
python3 mtg-abc.py -i /storage/datasets/mtg-tcg/oracle-cards.json
```

```
#1. "this" - 64.78% of cards
#2. "creature" - 60.13% of cards
#3. "target" - 35.26% of cards
#4. "your" - 31.12% of cards
#5. "card" - 28.29% of cards
#6. "control" - 26.57% of cards
#7. "turn" - 25.35% of cards
#8. "that" - 23.76% of cards
#9. "with" - 22.5% of cards
#10. "when" - 21.84% of cards
```

## `mtg-abc.py`
Find the best combos for Now I Know My ABC's. Attempts to score every card based on the rarity of the letters its name contains, then match them up to create full alphabets. Includes letters from "Now I Know My ABC's" by default. WARNING: This can take a long time if you use a gigantic `v` value.

<img src='https://cards.scryfall.io/large/front/9/5/95c790e6-340f-42c2-af88-e458b7b9690c.jpg?1562488892' height=250px>


```sh
python3 mtg-abc.py \
  -i /storage/datasets/mtg-tcg/oracle-cards.json \
  -n 10 \
  -v 1000000 \
  -m 5 \
  -c W U B R G
```

```
╔═ Two Card Combos ════
╟ Score: -1.78
╟ Zimone, Quandrix Prodigy
╟ Javelin of Lightning
╠════
╟ Score: -2.27
╟ Zimone, Quandrix Prodigy
╟ Sigurd, Jarl of Ravensthorpe
╠════
╟ Score: -2.28
╟ Zimone, Quandrix Prodigy
╟ Varchild, Betrayer of Kjeldor
╠════

╔═ Three Card Combos ════
╟ Score: -0.79
╟ Tranquil Expanse
╟ Lazotep Quarry
╟ Sigurd, Jarl of Ravensthorpe
╠════
╟ Score: -1.46
╟ Tranquil Expanse
╟ Lazotep Quarry
╟ Fugitive of the Judoon
╠════
╟ Score: -1.12
╟ Tranquil Expanse
╟ Temple of the Dragon Queen
╟ Jolrael, Voice of Zhalfir
╠════
```