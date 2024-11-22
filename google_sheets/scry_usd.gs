function scry_usd(name) {
  if (name == ""){ return "~" }
  var price = IMPORTJSON("https://api.scryfall.com/cards/named?fuzzy="+name, "prices/usd");

  if (Object.keys(price).length === 0){
    return 0;
  }
  else if (!isNaN(parseFloat(price))){
    return parseFloat(price);
  }
  else{
    return 0;
  }
}

// -- Testing --
//console.log(scry_usd("pact of negation"))