function scry_uri(name) {
  if (name == ""){ return "~" }
  var output = IMPORTJSON("https://api.scryfall.com/cards/named?fuzzy="+name, "scryfall_uri");
  return output
}

// -- Testing --
//console.log(scry_uri("pact of negation"))