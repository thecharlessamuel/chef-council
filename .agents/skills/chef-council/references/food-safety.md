# Food safety reference

- **Checked on:** 2026-11-18
- **Refresh by:** 2027-11-18
- **Locale:** United States. The numbers below are US federal consumer guidance. See the [locale note](#locale-note) before using them anywhere else.

Food safety is a constraint on every lens of the council. No lens, recipe, or preference changes a number in this file. Every safety number here is in a table row that has an ID and names its source, and the skill's other files carry no safety numbers of their own. Outside those rows, the only numbers in this file are the two dates above, what the Sources table holds, the IDs of rows, the numbering of lists, and 165°F where the poultry sections name the default.

This file is a summary for home cooking, not medical advice. For anything it does not cover, go to the sources.

## How to use this file

1. Find the food or the action in the tables and give the number with its source.
2. Read the `higher_risk_diners` line of `kitchen/profile.md`. On `yes`, apply [Stricter endpoints for higher-risk diners](#stricter-endpoints-for-higher-risk-diners). On `unknown`, ask before giving a number.
3. Measure with a food thermometer, in the way row K9 says.
4. Give temperatures in the units the profile asks for. Each temperature is given in both.

## Sources

Each source was opened and read on the checked-on date. The pages on foodsafety.gov and fsis.usda.gov refused the page-fetch tool that day, so they were read from the Internet Archive copies linked here, which are copies of the official pages.

| Key | Source | Read as |
|---|---|---|
| `FSG-TEMPS` | FoodSafety.gov, *Cook to a Safe Minimum Internal Temperature* (reviewed November 21, 2024): https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures | Archive copy of 2026-11-17: https://web.archive.org/web/20261117204720/https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures |
| `FSG-STEPS` | FoodSafety.gov, *4 Steps to Food Safety* (reviewed September 18, 2023): https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety | Archive copy of 2026-11-15: https://web.archive.org/web/20261115093715/https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety |
| `FSG-RISK` | FoodSafety.gov, *People at Risk of Food Poisoning* (reviewed August 14, 2025): https://www.foodsafety.gov/people-at-risk | Archive copy of 2026-11-10: https://web.archive.org/web/20261110115704/https://www.foodsafety.gov/people-at-risk |
| `FSIS-LEFTOVERS` | USDA Food Safety and Inspection Service, *Leftovers and Food Safety* (updated July 31, 2020): https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety | Archive copy of 2026-11-18: https://web.archive.org/web/20261118055844/https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety |
| `FSIS-APPA` | USDA Food Safety and Inspection Service, *FSIS Cooking Guideline for Meat and Poultry Products (Revised Appendix A)*, December 2021, document FSIS-GD-2021-14, Tables 3 and 4: https://www.fsis.usda.gov/sites/default/files/media_file/2021-12/Appendix-A.pdf | Archive copy of 2025-12-06: https://web.archive.org/web/20251206170948/https://www.fsis.usda.gov/sites/default/files/media_file/2021-12/Appendix-A.pdf |
| `FDA-HANDLING` | US Food and Drug Administration, *Safe Food Handling* (current as of March 5, 2024): https://www.fda.gov/food/buy-store-serve-safe-food/safe-food-handling | The page itself |
| `FSIS-HEAT` | USDA Food Safety and Inspection Service, *How Temperatures Affect Food* (updated October 19, 2020): https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/how-temperatures-affect-food | Archive copy of 2026-11-03: https://web.archive.org/web/20261103202835/https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/how-temperatures-affect-food |
| `FSIS-REFRIG` | USDA Food Safety and Inspection Service, *Refrigeration & Food Safety* (updated March 23, 2015): https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/refrigeration | Archive copy of 2026-11-03: https://web.archive.org/web/20261103202835/https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/refrigeration |
| `FSIS-DATING` | USDA Food Safety and Inspection Service, *Food Product Dating* (updated April 23, 2025): https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-product-dating | Archive copy of 2026-11-03: https://web.archive.org/web/20261103202832/https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-product-dating |
| `CDC-STAPH` | US Centers for Disease Control and Prevention, *About Staph Food Poisoning* (updated April 16, 2024): https://www.cdc.gov/staph-food-poisoning/about/index.html | The page itself |

## Cooking endpoints

These are the defaults. Each is a minimum internal temperature, measured with a food thermometer.

| ID | Food | Cook to | Source |
|---|---|---|---|
| C1 | All poultry: whole birds, breasts, legs, thighs, wings, ground poultry, giblets, poultry sausage, and stuffing cooked inside a bird | 165°F (74°C) | `FSG-TEMPS`, `FDA-HANDLING` |
| C2 | Ground meat and sausage made from beef, bison, veal, goat, lamb, or pork | 160°F (71°C) | `FSG-TEMPS` |
| C3 | Steaks, roasts, and chops of beef, bison, veal, goat, lamb, or pork | 145°F (63°C), then a rest of 3 minutes | `FSG-TEMPS` |
| C4 | Fish, whole or fillet | 145°F (63°C), or until the flesh is no longer translucent and separates easily with a fork | `FSG-TEMPS` |
| C5 | Shellfish | Shrimp, lobster, crab, and scallops until the flesh is pearly or white and opaque; clams, oysters, and mussels until the shells open | `FSG-TEMPS` |
| C6 | Eggs and egg dishes | Eggs until the yolk and white are firm; egg dishes such as frittata and quiche to 160°F (71°C) | `FSG-TEMPS` |
| C7 | Casseroles, with or without meat, and leftovers of any kind | 165°F (74°C) | `FSG-TEMPS` |
| C8 | Ham | Raw ham to 145°F (63°C), then a rest of 3 minutes; precooked ham reheated to 165°F (74°C), or to 140°F (60°C) when it was packaged in a USDA-inspected plant | `FSG-TEMPS` |
| C9 | Rabbit and venison | 160°F (71°C) | `FSG-TEMPS` |

A minimum is not a target for texture. A braise can pass its endpoint and still be tough, and that is a cooking question, not a safety one.

## Poultry: 165°F is the default

Some kitchen advice tells cooks to take chicken breast off the heat at a lower temperature than the consumer charts give. This file settles that conflict:

- The endpoint for all poultry is row C1. The consumer charts of FoodSafety.gov and the FDA both give it, with no lower alternative, and it is what this skill gives whenever a cook asks when poultry is done.
- A lower temperature is safe only when the meat is held at that temperature for a set time. The only lower numbers this skill may give are the holds in the next section, labeled as holds, with their conditions.
- When a cook's recipe or another source gives a lower poultry temperature with no hold, say that it is below the endpoint in row C1 and give row C1.
- Dry poultry is a cooking problem, and `troubleshooting.md` covers it without lowering the endpoint.

## Labeled exception: poultry held at a lower temperature

This section is an exception, never a default. Offer it only when the cook asks for it or the cook's recipe already depends on it, and always with its label and its conditions.

The FSIS cooking guideline lists how long chicken and turkey must stay at a given internal temperature to get the same reduction in Salmonella that row C1 gets at once.

| ID | Poultry | Internal temperature, and how long the meat must stay at it | Source |
|---|---|---|---|
| H1 | Which column these rows use | The column for 12 percent fat, which the guideline says may be used for products with more fat or with unknown fat content | `FSIS-APPA`, the key question after Table 4 |
| H2 | Chicken | 150°F (65.6°C) for 4.2 minutes; 155°F (68.3°C) for 54.4 seconds; 160°F (71.1°C) for 16.9 seconds | `FSIS-APPA`, Table 3 |
| H3 | Turkey | 150°F (65.6°C) for 4.9 minutes; 155°F (68.3°C) for 1.3 minutes; 160°F (71.1°C) for 26.9 seconds | `FSIS-APPA`, Table 4 |
| H4 | Chicken and turkey | At 165°F (73.9°C) the holding time in both tables is 0 seconds | `FSIS-APPA`, Tables 3 and 4 |

Conditions, all of which apply:

- **It is a hold, not a pull temperature.** The whole piece, measured at its coldest point, must stay at or above the temperature for the full time. Taking meat off the heat when it first touches the number is not a hold.
- **It was written for food plants, not home kitchens.** The guideline is for establishments that make ready-to-eat products, and it treats humidity during cooking and the time the meat takes to heat up as conditions of the tables. A home kitchen cannot verify those conditions, so say so every time.
- **It needs equipment that can do it.** Use a hold only when the cook can keep the meat at a steady temperature and measure it for the whole time, for example in a temperature-controlled water bath with a thermometer the cook trusts. An oven or a pan with a single reading does not qualify.
- **Never for higher-risk diners.** When `higher_risk_diners` is `yes` or `unknown`, do not offer a hold. Use row C1.
- **Other poultry.** For poultry other than chicken or turkey, do not offer a hold. Use row C1.

Always give row C1 next to a hold, so the cook sees the default.

## Stricter endpoints for higher-risk diners

When `higher_risk_diners` in `kitchen/profile.md` is `yes`, these rows apply on top of the defaults, to every dish served to the whole table.

| ID | Rule | Source |
|---|---|---|
| R1 | The groups at higher risk are adults 65 and older, children younger than 5, people whose immune systems are weakened by illness or medical treatment, and people who are expecting a child | `FSG-RISK` |
| R2 | No raw or undercooked meat or poultry. Cook each to its endpoint in the table above, with no hold from rows H2 and H3 | `FSG-RISK` |
| R3 | No raw or undercooked fish or shellfish, and no cold-smoked fish. Cook seafood to 145°F (63°C), and reheat previously cooked seafood to 165°F (74°C) | `FSG-RISK` |
| R4 | No foods that contain raw or undercooked eggs. Use pasteurized eggs or egg products when a recipe calls for raw or undercooked eggs | `FSG-RISK` |
| R5 | Reheat hot dogs, luncheon meats, and deli meats until steaming hot or to 165°F (74°C) | `FSG-RISK` |
| R6 | No raw sprouts, no unpasteurized milk, no cheese made from unpasteurized milk unless it is heated to 165°F (74°C) or until steaming hot, and no unwashed fresh vegetables | `FSG-RISK` |

The source lists further foods to avoid, such as some fresh soft cheeses and refrigerated pâtés. Read it when a dish uses them.

In practice, for a higher-risk table:

- For fish, use the thermometer number in row C4, not its visual alternative. Eggs are cooked until firm as row C6 says, or are pasteurized as row R4 says, and egg dishes go to the number in row C6.
- Do not offer a doneness below an endpoint, whatever the cook usually prefers. Protect texture another way: gentler heat, even thickness, and taking the food off the heat as soon as it reaches the endpoint.
- When only some diners are at higher risk, the stricter rows still apply to anything those diners will eat.

## Holding, cooling, storing, and reheating

| ID | Rule | Source |
|---|---|---|
| K1 | Bacteria that cause food poisoning multiply fastest between 40°F (4°C) and 140°F (60°C) | `FSG-STEPS` |
| K2 | Keep hot food at 140°F (60°C) or above until it is served | `FSG-STEPS` |
| K3 | Refrigerate perishable food within 2 hours, or within 1 hour when it has been in temperatures above 90°F (32°C). Throw away perishable food that was left out longer | `FSG-STEPS`, `FSIS-LEFTOVERS` |
| K4 | Keep the refrigerator at 40°F (4°C) or below and the freezer at 0°F (-18°C) or below | `FSG-STEPS` |
| K5 | Cool food quickly: divide large amounts into shallow containers and cut large pieces into smaller ones. Hot food can go straight into the refrigerator, or be chilled first in an ice bath or a cold-water bath | `FSIS-LEFTOVERS` |
| K6 | Use refrigerated leftovers within 3 to 4 days. Frozen leftovers keep their quality for 3 to 4 months | `FSIS-LEFTOVERS` |
| K7 | Reheat leftovers to 165°F (74°C), and bring sauces, soups, and gravies to a rolling boil | `FSIS-LEFTOVERS`, `FSG-TEMPS` |
| K8 | Thaw in the refrigerator, in cold water, or in the microwave, never on the counter. Marinate in the refrigerator | `FSIS-LEFTOVERS`, `FSG-STEPS` |
| K9 | Put the thermometer in the thickest part of the food, not touching bone, fat, or gristle | `FSG-STEPS` |

A recipe step that says to cool food before assembling, packing, or freezing it must carry the limit in row K3 and the method in row K5.

## Mishandled food, spoiled food, and smell

Each row gives a rule, what its source says, and the source. The words in italics are quoted exactly from the page. Any words before them in the same cell are this file's description of the text around the quotation.

| ID | Rule | What the source says | Source |
|---|---|---|---|
| K10 | Cooking cannot be relied on to make raw meat or poultry safe once it was left too long in the temperature range of row K1. Bacteria may grow there and produce toxins, the toxins that are heat resistant are not destroyed by cooking, and the meat may not be safe to eat even when it is then cooked properly | The page first says that when raw meats are left too long in the temperature range of row K1, bacteria may grow and produce toxins which can cause foodborne illness. Then: *Those toxins that are heat resistant are not destroyed by cooking. Therefore, even though cooked, meat and poultry mishandled in the raw state may not be safe to eat even after proper preparation.* | `FSIS-HEAT` |
| K11 | Cooked food held in the temperature range of row K1 can also be risky. Cooking can kill Staph bacteria, but it does not destroy the toxin they have made in the food | *Foods that are cooked also can be risky if held at unsafe temperatures (between 40°F and 140°F). Even though cooking can kill Staph, it does not destroy the toxin in the food.* | `CDC-STAPH` |
| K12 | A normal smell, taste, or look does not show that food is safe. The bacteria that cause foodborne illness do not generally change how food smells, tastes, or looks, and food left too long on the counter may be dangerous and still look fine | The page says of the bacteria that cause foodborne illness that they can grow rapidly in the temperature range of row K1, and then: *they do not generally affect the taste, smell, or appearance of a food. In other words, one cannot tell that a pathogen is present.* And: *Food that has been left too long on the counter may be dangerous to eat, but could look fine.* | `FSIS-REFRIG` |
| K13 | Food that has developed an off odor, flavor, or texture has spoiled and should not be eaten | *Spoiled foods will develop an off odor, flavor or texture due to naturally occurring spoilage bacteria. If a food has developed such spoilage characteristics, it should not be eaten.* | `FSIS-DATING` |

How far these rows reach:

- Rows K10 and K11 are about food that spent too long in the temperature range of row K1. Row K10's source speaks of raw meat and poultry, and row K11's of the toxin of Staph bacteria. Neither says that every toxin survives cooking, or speaks of every food, so do not say either.
- Row K12 is about the bacteria that cause illness. An off smell is a sign of spoilage, which row K13 covers. A normal smell does not show that those bacteria are absent.
- Row K13 is the source's instruction not to eat spoiled food. It is not a statement of how likely spoiled food is to cause illness.

When food was left out past the limit in row K3, do not offer more cooking as a fix. Give row K3, which says to throw the food away and covers all perishable food. Add row K10 or row K11 only for the food or the toxin that row names, as the reason cooking cannot be relied on there. When safety depends on how food was handled, ask for the history and apply the rows of this file.

## What this file does not cover

Home canning, fermenting, curing, and smoking; raw-milk products beyond row R6; wild game beyond row C9; foraged food; allergen cross-contact; infant feeding; and any commercial or volume cooking. For these, go to the agencies named under Sources, and say that this file does not cover the question. Do not extend a row to a food it does not name.

## Locale note

These numbers are US federal consumer guidance, in degrees Fahrenheit with degrees Celsius beside them. Other countries publish their own endpoints and holding rules, and they are not all the same. If you cook somewhere else, replace the tables with your own food-safety authority's numbers, cite its pages in the Sources table, and update the dates at the top. Keep the structure: a default endpoint for each food, lower temperatures only as labeled holds from a cited table, and stricter rules for higher-risk diners. Never mix numbers from two authorities in one answer.

## Refreshing this file

Guidance changes and links move. This file is evidence as of its checked-on date. On or after the refresh-by date, or sooner when an agency announces a change:

1. Open every link in the Sources table again and compare each row with its source.
2. Change any row that no longer matches, and say in the commit message which row changed and why.
3. Set a new checked-on date, and a refresh-by date one year after it.

A row may be added only with a source that was opened and read. A number that cannot be traced to a source does not go in this file.
