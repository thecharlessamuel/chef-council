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

## On-demand specialists

Consulted only when the dish is in the lens's scope.
