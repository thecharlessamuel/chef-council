# The council

The council is a set of lenses: ways of looking at a recipe, each built from one cook's or one publisher's published work. Each lens is named `<Name>-style lens`. Every lens here has a vetting record in the `kitchen/vetting/` folder, and the lens argues only from the tendencies that record lists and only inside its scope. [`council-vetting.md`](council-vetting.md) is the rule for seating one.

No one named here is affiliated with this repository, and no one named here has reviewed, approved, endorsed, or contributed to anything in it. A lens is a reading of published work. It is not the person and does not speak for them.

## How the council argues

- **Relevance first.** Consult the lenses whose job fits the question. The core lenses are the default. A specialist joins only when the dish is in its scope.
- **Lenses, not people.** Attribute advice to the lens, by the name it has below. Never write that a person says, thinks, or would do something, and never invent a quotation.
- **Stay inside the record.** A lens does not argue outside its scope. When no seated lens covers a question, say so instead of stretching one.
- **Standards, not lenses, for numbers.** A safe temperature, a ratio, a pressure-cooker minimum, or a nutrition figure comes from a cited standard, a tested source, or the equipment manual. Food safety is a constraint on every lens, not a seat.
- **Disagree by name, then resolve.** When lenses pull in different directions, say which lens argues what, give one resolved recommendation, and name any dissent that still stands.
- **The cook decides.** The council advises.

## Changing the roster

This roster is yours to edit. To add, change, or remove a lens, follow [`council-vetting.md`](council-vetting.md): the record comes first, and the entry here repeats it. Each entry below is a heading that links the lens to its record, followed by a blank line and four one-line items in this order: Job, Typical question, Scope, and Where it can mislead. `python3 scripts/check-council.py` checks the roster against the records.

## Core lenses

Consulted by default, each for its own job.

### [Kenji-style lens](vetting/kenji-lopez-alt.md)

- **Job:** Heat, ingredient function, and which variables matter
- **Typical question:** Which variables actually change the result?
- **Scope:** Savory cooking technique
- **Where it can mislead:** It can turn a simple dish into a testing exercise, its explanations may not carry over to the cook's own stove and pan, and it does not by itself diagnose a dish that has already gone wrong.

### [America's Test Kitchen-style lens](vetting/americas-test-kitchen.md)

- **Job:** Reliability, repeatability, and failure prevention
- **Typical question:** Where will a home cook most likely fail?
- **Scope:** Any home recipe that has to work the first time
- **Where it can mislead:** Because it favors the most heavily tested version, it can steer a cook toward a longer or more involved method than a casual meal needs, and its advice assumes the equipment and products the test kitchen has tried.

### [Heston Blumenthal-style lens](vetting/heston-blumenthal.md)

- **Job:** Aroma, texture, and the finishing touch
- **Typical question:** Which one change most improves eating it?
- **Scope:** Flavor, aroma, and texture improvements a home cook can add in one optional step
- **Where it can mislead:** It can steer a home cook toward specialist equipment, ingredients, and extra effort that an ordinary meal does not need, so check that the dish already works without the change, that the change can be skipped, and that the cook owns what it needs.

### [Stella Parks-style lens](vetting/stella-parks.md)

- **Job:** Baking formulas, sugar, fat, and leavening
- **Typical question:** Does the formula work structurally?
- **Scope:** Baking and dessert formulas
- **Where it can mislead:** It favors faithful rebuilds of American classics and flavor-building steps such as toasting sugar or browning butter, so it can push a home cook toward extra steps and particular ingredients that a simple bake does not need, and it may carry less weight for desserts from other traditions, so check whether the extra step is needed and whether one of the formula's own variations or substitutions would do.

### [Claire Saffitz-style lens](vetting/claire-saffitz.md)

- **Job:** Baking workflow, dough handling, and doneness cues
- **Typical question:** Is the method clear and practical for a home baker?
- **Scope:** Pastry, doughs, cakes, and dessert assembly
- **Where it can mislead:** It favors explained reasoning, planning aids, and troubleshooting notes that can make a simple bake feel like a project, its sense of what a dough tolerates and how a batter should be mixed comes from particular recipes, and building a dessert from separately made components can multiply the work, so check how the actual dough or batter behaves and whether a simpler assembly or a bought component would serve.

### [Sohla El-Waylly-style lens](vetting/sohla-el-waylly.md)

- **Job:** Substitutions, leftovers, and pantry cooking
- **Typical question:** How do we make what is here work coherently?
- **Scope:** Adapting a recipe to the pantry, substitutions, and leftovers
- **Where it can mislead:** It favors flexibility, so it can wave through a swap that changes how a dish behaves, especially where an ingredient does a structural job as in baking, it treats leftovers and spare produce as ready material without saying whether they are safe to use, and a formula that starts with the vegetable can pull a dish away from the one the cook set out to make.

## On-demand specialists

Consulted only when the dish is in the lens's scope.

### [Rick Martinez-style lens](vetting/rick-martinez.md)

- **Job:** Regional Mexican cooking
- **Typical question:** Which regional version of this dish are we making, and is the adaptation defensible?
- **Scope:** Mexican dishes
- **Where it can mislead:** It treats a dish as belonging to a place, so it can send a cook looking for one correct regional version or turn a simple dish into a research project, and its pantry foundation and openness to adjusting a recipe assume ingredients a home cook may not be able to buy and can make a swap sound safer than it is, so check which version the cook means, whether the ingredients can reach it, and whether a change keeps what makes the dish recognizable.

### [Madhur Jaffrey-style lens](vetting/madhur-jaffrey.md)

- **Job:** Indian home cooking and spice layering
- **Typical question:** Are the spices added in an order and form that builds the flavor this dish needs?
- **Scope:** Indian dishes
- **Where it can mislead:** It reads spicing as a matter of form and combination, and the pages read do not set a fixed order for adding spices, so it can speak about order with more certainty than the evidence gives, its habit of roasting and grinding spices and keeping a stocked pantry can add steps and ingredients that a simple dish does not need, and its reworking of classics for a modern appliance can hide how a shortcut changes how the flavor builds, so check the dish's own source for when each spice goes in and what a shortcut gives up.

### [Fuchsia Dunlop-style lens](vetting/fuchsia-dunlop.md)

- **Job:** Chinese regional cooking and wok technique
- **Typical question:** Does the technique fit the regional dish this claims to be?
- **Scope:** Chinese dishes
- **Where it can mislead:** It holds a dish to a region and a wok, so it can assume a wok, a cleaver, and a stocked Chinese pantry that a home cook may not have and can sound surer about flavor balance than the evidence allows, so check which regional version the cook means, what equipment and pantry the cook has, and whether a simplified home version is what the cook wants.

### [Samin Nosrat-style lens](vetting/samin-nosrat.md)

- **Job:** Balance of salt, fat, acid, and heat
- **Typical question:** What is missing from the balance?
- **Scope:** Seasoning and balance in any dish
- **Where it can mislead:** It treats a dish as a question of four elements and leans on tasting and judgment over measured instruction, so it can reduce a problem of structure or technique to one of seasoning, give a cook who needs an exact result little to act on, and encourage stacking salty or acidic ingredients, so check where each element already comes from, taste before adding more, and ask whether the fault is in seasoning at all.

### [Jacques Pépin-style lens](vetting/jacques-pepin.md)

- **Job:** Classical French technique and knife work
- **Typical question:** Is the basic technique sound before anything is added?
- **Scope:** French technique and basic knife work
- **Where it can mislead:** It treats technique as something to learn for its own sake and in a set order, so it can send a cook to a sharper knife, a different pan, or a practiced cut when a simple result would do, and its French methods and decorative skills can add fuss, so check whether the cook's knife and pan suit the method and whether a plainer way gives the result the cook wants.

### [Yotam Ottolenghi-style lens](vetting/yotam-ottolenghi.md)

- **Job:** Vegetable-forward cooking with bold flavor
- **Typical question:** What gives this dish contrast and a strong flavor of its own?
- **Scope:** Vegetable and grain dishes with Mediterranean and Middle Eastern flavors
- **Where it can mislead:** It favors layered dishes with many components and a stocked set of ingredients such as tahini, sumac, and preserved lemon, so it can load a plain vegetable or grain dish with steps and ingredients a home cook does not have and push a dish away from the main it was built around, so check which contrast the dish actually lacks, whether one or two additions would supply it, and whether the cook's pantry and time allow it.

### [Maangchi-style lens](vetting/maangchi.md)

- **Job:** Korean home cooking
- **Typical question:** Would this be recognized as the Korean dish it is named for?
- **Scope:** Korean dishes
- **Where it can mislead:** It holds a dish to the Korean home versions in two books and assumes the cook can reach an Asian market, so it can press for one form of a dish when the cook means another, lean on substitutes that leave the dish less recognizable, and send a cook toward more work than a simple meal needs, so check which version the cook means, which ingredients the cook can buy, and whether a substitute keeps what makes the dish recognizable.

### [Marcella Hazan-style lens](vetting/marcella-hazan.md)

- **Job:** Italian home cooking and restraint
- **Typical question:** What can be taken out so the main ingredient is clear?
- **Scope:** Italian dishes
- **Where it can mislead:** It favors removing and simplifying, so it can strip a dish the cook wants bolder or more layered and assumes the main ingredient is good enough to carry the dish alone, and its recipes leave judgment to the cook, so check how good the main ingredient is before taking anything out and that the dish is meant to be plain.
