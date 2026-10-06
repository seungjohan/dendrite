---
stage: log
category: 
date: {{date}}
source: 
range: 
year: 
era: 
people: []
place: 
threads: []
causes: []
enables: []
weakens: []
competes_for: []
chain: []
concepts: []
bonded: 
---

> [!IMPORTANT] Key Takeaway
> **In one line:** 
> **Why it stuck:** 

# {{title}}

## 📖 What I Studied
<!-- The facts, short. Enough that future-you can rebuild it. Only the range you studied. -->


## 🤔 The Question
<!-- Ask WHY, not what. Why is it like this? Why doesn't it add up? Why did it happen then, there, by them?
Format: **Q#:** Why …? (same ID as in [[Question log]]). Leave blank if nothing, but look for it. -->


## 🧵 Where the Thread Led
<!-- Follow the question out of the subject: history, people, era, other fields. -->


## 🔗 Bonds
<!-- Only if you can finish "connects because ___". Format: - [[other note]] · {kind}: connects because ___ (found by: me | bond pass)
Kinds: led to · common cause · complement · competition · same mechanism · same thread · the dig · other -->


## 💭 Reflection: 
<!-- Your own raw thinking. First person, any length. -->


#### 🧭 Linked by the algorithm
%% AUTO-LINKS %%
- none yet
%% /AUTO-LINKS %%

---
#### 🕸 Meets this note
<!-- Auto: how other notes meet this one, by kind (LINKING.md §1). Leads to check, not bonds. Ranked: python3 scripts/bond_leads.py -->
```dataview
TABLE WITHOUT ID file.link AS Note, category AS Subject, ledHere AS "⬅ led here via", ledOn AS "➡ led on via", sameCause AS "🌱 same cause", fought AS "⚔ both fought for", against AS "⇅ pulls against", shares AS "also shares"
FROM "notes"
WHERE file.path != this.file.path
FLATTEN list(filter(default(enables, list()), (x) => contains(default(this.causes, list()), x))) AS ledHere
FLATTEN list(filter(default(causes, list()), (x) => contains(default(this.enables, list()), x))) AS ledOn
FLATTEN list(filter(default(causes, list()), (x) => contains(default(this.causes, list()), x))) AS sameCause
FLATTEN list(filter(default(competes_for, list()), (x) => contains(default(this.competes_for, list()), x))) AS fought
FLATTEN list(filter(flat(list(default(enables, list()), default(weakens, list()))), (x) => contains(flat(list(default(this.enables, list()), default(this.weakens, list()))), x) AND (contains(default(enables, list()), x) != contains(default(this.enables, list()), x)))) AS against
FLATTEN list(filter(flat(list(enables, threads, concepts, era, people, place)), (x) => x AND contains(flat(list(this.enables, this.threads, this.concepts, this.era, this.people, this.place)), x))) AS shares
WHERE length(ledHere) + length(ledOn) + length(sameCause) + length(fought) + length(against) + length(shares) > 0
SORT length(ledHere) + length(ledOn) + length(sameCause) + length(fought) + length(against) DESC, category
```
