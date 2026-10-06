---
stage: general
category: log
---

# 🧭 Linking log

How Dendrite's linking algorithm got to where it is, so I can follow up later. Newest on top.
Decisions behind each step are in [[Decision log]]; the rules themselves in [[LINKING]].

| Date | What changed | Where to look |
|---|---|---|
| 2026-10-06 | **Links written into every page.** Dendrite has no app, so `bond_leads.py --write` puts each note's top 5 links into a *🧭 Linked by the algorithm* block (between `%% AUTO-LINKS %%` markers) above the footer; the template carries the empty block; filing a note ends with that command. Leads, not bonds. | template, AGENTS bond pass 6b, LINKING §6 |
| 2026-10-06 | **What I studied first, dates second.** *Same study* (rare words of What I Studied, the question, the takeaway, across subjects) is evidence, a reason when clear; the date boosts go from ×1.25 to ×1.1. | LINKING §6, `bond_leads.py` |
| 2026-10-05 | **The latest algorithm itself, with a time layer.** `scripts/flowlink.py` is the core (Constellate's rules, tested against its output) copied from curiosity-lab's skill; each note is a flow (causes up; enables, weakens, competes_for down; chain; people). A cause must come before its effect; common cause and complement are reasons inside one historical moment. New `year`, `weakens`, `chain`; index *Timeline* and *Studied this week, back then*. | LINKING §2, §6; index |
| 2026-10-05 | **The structure shows the kind.** Each Kind 2 sub-type has its field; the footer shows notes by kind; the `node` template lists notes by role toward a third thing; bonds name their kind. | template, `node.md`, LINKING §1–§4 |
| 2026-10-05 | **First adaptation** of Constellate's algorithm: `causes`, `enables`, `competes_for` and `bond_leads.py`. Renamed "linking system" → "linking algorithm". | LINKING |

Where the algorithm comes from: Constellate's `LINKING-ALGORITHM.md`; the portable version is
curiosity-lab's `skills/linking-algorithm` (`core/flowlink.py`, `references/adapting.md`).

**To follow up:** fill `year`, `causes`, `enables` in notes as you go (the links are only as good
as the fields); after a few months, compare bonds `found by: me` with what the algorithm proposed.
