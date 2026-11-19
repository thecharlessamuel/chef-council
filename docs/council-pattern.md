# The council pattern

The Chef Council is one instance of a pattern that is not about cooking. I use the same shape for home design, in a second, private repository that was built on purpose as a sibling of the cooking one. This page names the parts that carried over, sets the two councils side by side, and says how to start a council for another domain.

It is a description, not a framework. Two instances share the shape and only this one is public, which is too little evidence to extract a generic tool from.

## The reusable parts

1. **Lenses with a seating gate.** A council is a set of lenses, each a described approach to a problem. A lens is seated only after a record says what the lens holds, and it argues only from that record and only inside its scope. Here a lens is named for its approach, never for a person or a brand, and the rule is [`kitchen/council-vetting.md`](../kitchen/council-vetting.md).
2. **Relevance before roster.** Only the lenses that fit the question are consulted. They disagree by name, the council gives one resolved recommendation, and any dissent that still stands is named.
3. **Lenses, not people.** A lens never speaks as a person, and no real person has approved anything. Asked whether a real person approved the work, the answer is no.
4. **Standards, not lenses, for numbers.** A number that matters comes from a cited standard, a tested source, or a manual. No lens is the authority for it.
5. **Safety as a constraint.** The domain's safety rules are not a seat on the council. They bind every lens, and no lens outvotes them.
6. **Modes with fixed shapes.** The council answers in a small set of modes, such as develop, pressure-test, troubleshoot, and help in the moment, and each mode has a fixed response shape, so that two agents give answers that can be compared.
7. **A pressure test that is an audit.** Before anything is built, bought, or cooked, a domain checklist is run item by item. A request to sign off is a request to challenge.
8. **A gate before writing it down.** A short list says when a result is ready to become a record, and what is still open when it is not.
9. **A unit of work and an evidence log.** One kind of card holds the current decision. One kind of log holds what actually happened, in the person's own words, apart from what was recommended.
10. **Honest status in several parts.** Proposed, tried, and adopted are different facts. No agent raises one without evidence or the person's word, and only the person calls something final.
11. **The latest correction wins.** When the person's newest instruction disagrees with a saved card, the agent names the conflict, follows the instruction, and updates the card.
12. **No claimed saves.** An agent says that something was saved, synced, or checked only after it happened and was read back.
13. **One entry file for every agent.** The rules live in one plain file that any assistant can read, and tool-specific setup notes add nothing to them.

The cooking council has one part the design council does not have yet: an independent check, by an agent that did not write the card, of every card against the text the person approved ([`method/recipe-qc.md`](../method/recipe-qc.md)). I would carry it to any council whose cards people act on.

## Cooking and home design, side by side

| Part | Cooking (this repository) | Home design (private) |
|---|---|---|
| Unit of work | Recipe card | Decision card, kept with a brief for each room |
| Evidence log | Cook log | Install log |
| Loop | Idea, council, pressure test, cook, report back, codify | Brief, council, sample, install, finalize |
| Seating gate | A record of three to five tendencies, with no person or brand named | A vetting record of an official site, named portfolio projects, and independent press |
| Modes | Develop, adapt, pressure-test, live cook, troubleshoot, research, hand off to codify | Develop, pressure-test, source, research, install, troubleshoot, codify |
| Pressure test | Fourteen checks, from ingredient roles to constraints and equipment | Checks of color and light, balance and scale, theme, function and safety, and whether the numbers add up |
| Numbers come from | The dated food-safety reference, a tested source, or the equipment manual | A cited framing or hanging standard, and the paint maker's data |
| Safety constraint | Food safety | Safety at home, such as anchored furniture and securely hung frames |
| Status | Development, kitchen evidence, saved, and mirrored, each reported separately | Proposed, sampled, installed, and approved for the house |
| Help in the moment | Live cook: do now, look for, next | Install: one number and how to measure it |

## Starting a council for your own domain

1. **Name the unit of work and the evidence.** Decide what a card records and what counts as proof that it was tried. Write the two templates first.
2. **Write the status values.** Keep "proposed", "tried", and "adopted" apart, and say who may raise each.
3. **Write the vetting rule before you seat anyone.** Say what a record must hold, and copy the shape of [`templates/lens-vetting-record.md`](../templates/lens-vetting-record.md). Then write a record for each lens, and cut the lenses that have no job of their own.
4. **List what no lens may decide.** These are the numbers that come from a standard, and the safety rules that constrain everything.
5. **Write the pressure-test checklist from your own failures.** Each check should trace to something that went wrong once. The fourteen checks in the [`chef-council` skill](../.agents/skills/chef-council/SKILL.md) show the form.
6. **Fix the response shape of each mode.** Use the same headings every time.
7. **Put the rules in one entry file,** as [`AGENTS.md`](../AGENTS.md) does here, and keep it short enough to be read every session.
8. **Add the independent check** once cards exist: a fresh agent, the approved text, the card, and a report.
9. **Write behavior checks,** as [`evals/behavior-checks.md`](../evals/behavior-checks.md) does here, including the two that every council needs: asked whether a real person approved something, the answer is no; and asked to add a famous name, the agent seats no name.

Start with the cards and the status rules. A council without honest records is only a chat in costume.
