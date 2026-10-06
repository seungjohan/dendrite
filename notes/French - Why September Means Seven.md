---
stage: log
category: french
date: 2026-09-17
source: French class (month names)
range: Month names, janvier → décembre
era: "[[Ancient Rome]]"
people: ["[[Julius Caesar]]", "[[Augustus]]"]
place: "[[Rome]]"
threads: ["[[power writes itself into time]]"]
concepts: []
bonded: 
---

> [!IMPORTANT] Key Takeaway
> **In one line:** *Septembre* is month 9 but means "seven", because the Roman year used to start in March, and two rulers renamed months after themselves.
> **Why it stuck:** A word I was memorizing turned out to be a fossil of a 2,000-year-old calendar.

# French: Why September Means Seven

## 📖 What I Studied
French month names: *janvier, février, mars, avril, mai, juin, juillet, août, septembre, octobre, novembre, décembre*.

## 🤔 The Question
**Q1:** Why do *septembre, octobre, novembre, décembre* mean 7, 8, 9, 10 when they're months 9–12?

*Septembre, octobre, novembre, décembre* sound like *sept, huit (octo), neuf (novem), dix (decem)*: 7, 8, 9, 10. But they're months 9–12. The counting is off by two.

## 🧵 Where the Thread Led
- The early Roman calendar started the year in **March**, so month 7 really was September.
- January and February were added later, and the start of the year eventually moved to January 1, but the old number-names never got updated.
- The 5th and 6th months were *Quintilis* and *Sextilis*. Quintilis was renamed **July** for **Julius Caesar** (44 BC), and Sextilis became **August** for **Augustus** (8 BC).
- So a language quirk is really a record of **history, power and politics**: rulers literally writing themselves into time.

## 🔗 Bonds
- *(none yet, first note. Future candidates: anything else from Ancient Rome, or other words that still carry a dead system inside them.)*

## 💭 Reflection: A Language Is a Time Capsule, Not Just Vocabulary
I thought I was just memorizing month names. Then the mistake in the counting turned out to be the most interesting part. It led me straight to Julius Caesar. It's not just a language. It's connected to history, generations, the interests of an era. That's the moment that made me want every subject I study to connect like this.

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
