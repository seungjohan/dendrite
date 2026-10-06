---
stage: general
category: log
---

# 🧭 Decision log

Choices about how Dendrite works, so I don't re-argue them. Append-only, newest on top. A decision can be replaced by a newer row, never deleted.

- **Open:** still undecided on purpose. Real use will answer it; when it does, add a new row that settles it.

## Log

| Date | Decision | Why |
|---|---|---|
| 2026-10-06 | **The algorithm's links live in the pages** | Asked for: "both two projects don't have their own product but only written down on Obsidian … make a link in each page … when you start to write a new page … add this kind of link". A regenerable *🧭 Linked by the algorithm* block in every note and the template; refreshed after each filed note and each bond pass. History in [[Linking log]]. |
| 2026-10-06 | **What I studied first, dates second** | Asked for: Dendrite's input is my study, each log a dot; the topic studied matters more than the date. Added *same study* (the studied words, across subjects) as evidence; the date boosts drop from ×1.25 to ×1.1. Cause-before-effect stays. Dayweb is where time leads. |
| 2026-10-05 | **Run the latest linking algorithm itself, with dates first** | Asked for: "use the latest version which I built for both projects … date index is more important then constellate". `scripts/flowlink.py` is the algorithm's core (the rules Constellate links by, tested against its output) and `bond_leads.py` feeds it each note's flow. New fields `year` (the date index), `weakens`, `chain`. Dates now decide links: a cause must come before its effect; common cause and complement are reasons inside one historical moment (≤ 50 years) and shared topics outside it; a note studied long ago counts more. Index gains *Timeline* and *Studied this week, back then*. |
| 2026-10-05 | **The linking structure shows the kind: typed footer, node pages, typed bonds** | Asked for: "adjust this algorithm … for improving their linking structure", not a copied script. Each Kind 2 sub-type now has its field (common cause = `causes`, complement = `enables`, competition = `competes_for`), so the vault itself can say *how* two notes meet: the footer has columns ⬅ led here · ➡ led on · 🌱 same cause · ⚔ both fought for; a node page (`resources/templates/node.md`) lists notes by role toward the third thing; every bond names its kind, so "who finds connections" can be counted by kind. LINKING.md rewritten in Dendrite's own terms. |
| 2026-10-05 | **Constellate's linking algorithm, adapted: three directed fields and a lead script** | Asked for: "adjust this linking algorithm to my projects in both dentrite, and dayweb… based on their type of resources". Constellate showed links come from where two things' causes and effects *meet*, and that the kind of meeting is the reason. Study notes already answer when/who/where; `causes`, `enables` and `competes_for` add the direction `threads` lacks. `scripts/bond_leads.py` ranks leads (rare names count more, a lead inside one subject counts half) and never writes. Left out on purpose: an LLM writing fields, signs on everything, summaries (see LINKING.md §6). Replaces nothing; "Hidden threads stay open" still holds. |
| 2026-09-30 | **Hidden threads stay open** | Era, people and place are obvious. Other candidates: technology, war, trade, religion, a shared problem. They stay candidates, not rules. The bond pass reports any thread that pulls in 3+ subjects, and that evidence decides which ones matter. |
| 2026-09-30 | **A note exists when there's something to bond** | Every session already gets a Study log row, and every question gets a Question log row. A note is for a takeaway worth finding again, or a *why* question. Facts alone with no question get only the log row. |
| 2026-09-30 | **Every bond records who found it** | To answer "do connections come to me, or do I go looking?" Each bond gets `found by: me` or `found by: bond pass`. After a few months, count them. |
| 2026-09-30 | **Decisions live in a log, not the README** | They're a dated record that grows, like the other logs. The README keeps only the why. |
| 2026-09-17 | **Obsidian first, not a product** | I don't know yet which way works best: connections that come to me, or me going looking. A few months of real logging will tell me. The real risk is whether I keep the habit, and Obsidian tests that almost for free. |
| 2026-09-17 | **Build a product only when…** | …I've logged for months, had real "wow" connections, and can say what a tool did that plain Obsidian couldn't. |
| 2026-09-17 | **Its own vault** | Moved out of curiosity-lab so study logs have their own space. |
| 2026-09-17 | **Name: Dendrite** | Chosen over *Soma* (the cell body where signals combine; it names the result, and the name is taken by other brands) and *Neuron Web* (clear but generic). Dendrite names the *process*: gathering, branching, growing. Also considered: Quadrivium, Septem, Polymath Log, Common Root. |
| 2026-09-17 | **One consistent template** | Whatever and however I study, the format stays the same, so notes can be compared and connected. |
| 2026-09-17 | **Three study logs, not only notes** | Study log (what I studied), Question log (questions only), Connection log (which question connects to which study). Not every session deserves a note, but every session and every question should leave a trace. Borrowed the quick-line idea from my seungjohan logbook. |
| 2026-09-17 | **Each vault holds one thing** | Dendrite = study and its bonds. seungjohan = daily activity and reference material. curiosity-lab = ideas and research. Link across vaults, don't copy. |
