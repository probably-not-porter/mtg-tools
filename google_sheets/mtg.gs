// Get a price from Scryfall for card by name
function SCRYFALL_PRICE(name) {
  var price = IMPORTJSON("https://api.scryfall.com/cards/named?fuzzy="+name, "prices/usd");

  if (Object.keys(price).length === 0){ // if no price
    return 0;
  }
  else if (!isNaN(parseFloat(price))){ // if returns price
    return parseFloat(price);
  }
  else{ // other conditions
    return 0;
  }
}

function SCRYFALL_URI(name) {
  return IMPORTJSON("https://api.scryfall.com/cards/named?fuzzy="+name, "scryfall_uri")
}