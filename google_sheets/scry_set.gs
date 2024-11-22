// Requires a specific name. Misspelled or incomplete names will result
// in a #NAME error in the spreadsheet.

function scry_set(name) {
  if (name == ""){ return "~" }
  var setdata = IMPORTJSON("https://api.scryfall.com/cards/search?q=" + name + "+unique:prints", "data");
  var setarr = [];

  for (const item of setdata) {
    let setcode = item[1]["set"].toUpperCase()

    if (!setarr.includes(setcode)){
      setarr.push(setcode);
    }
  }
  return setarr.join(", ");
}

// -- Testing --
//console.log(scry_set("pact of negation"))