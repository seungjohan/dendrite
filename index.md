---
stage: hub
category: system
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** The more we live, the more we study. This is the living log that bonds every subject into one connected experience.
> **How to use it:** Follow [[README#The loop|the loop]]. Log every session in [[Study log]], every question in [[Question log]], new notes from the `dendrite` template.
> **Remember why:** [[README]] · **How it connects:** [[LINKING]]

# 🌿 Dendrite

*Grow a neuron web from everything you study.*

## 📒 Logs
| Log | Holds |
|---|---|
| [[Study log]] | What I studied, every day |
| [[Question log]] | Questions only, open or answered |
| [[Connection log]] | Which question connects to which study |
| [[Bond log]] | Bond passes: when, and what they found |

## ❓ Questions
![[Question log#Log]]

## 🕰 Timeline
Every note in the order **its events happened** (`year`), not the order I studied them. The date index: a cause has to come before its effect, and notes from one historical moment meet more easily.
```dataview
TABLE WITHOUT ID year AS Year, file.link AS Note, category AS Subject, era AS Era
FROM "notes"
WHERE year
SORT year ASC
```

## 🗂 All Notes
```dataview
TABLE category AS Subject, era AS Era, date AS Date
FROM "notes"
SORT date DESC
```

## 📅 Studied This Week, Back Then
What I studied a month, three months and a year ago this week: the reminder Dendrite exists for.
```dataview
TABLE WITHOUT ID file.link AS Note, category AS Subject, date AS Studied
FROM "notes"
FLATTEN (date(today) - date).days AS ago
WHERE date AND ((ago >= 27 AND ago <= 33) OR (ago >= 88 AND ago <= 94) OR (ago >= 362 AND ago <= 368))
SORT date DESC
```

## 📚 By Subject
```dataview
TABLE length(rows) AS Notes, rows.file.link AS Titles
FROM "notes"
GROUP BY category
SORT length(rows) DESC
```

## 🧵 Where Subjects Meet (Kind 2)
Era, people, place, thread, cause, effect or contested resource shared by **2+ subjects**. Ranked, with the kind of meeting named: `python3 scripts/bond_leads.py`.
```dataview
TABLE WITHOUT ID key AS "Meets at", unique(rows.category) AS Subjects, rows.file.link AS Notes
FROM "notes"
FLATTEN flat(list(era, people, place, threads, causes, enables, competes_for)) AS node
WHERE node
GROUP BY node
WHERE length(unique(rows.category)) >= 2
SORT length(unique(rows.category)) DESC
```

## 🌱 One Cause, Many Subjects
The same cause behind notes from **2+ subjects**: candidates for a node page.
```dataview
TABLE WITHOUT ID key AS "Caused by", unique(rows.category) AS Subjects, rows.file.link AS Notes
FROM "notes"
FLATTEN causes AS node
WHERE node
GROUP BY node
WHERE length(unique(rows.category)) >= 2
SORT length(unique(rows.category)) DESC
```

## ⚔ Fought Over Across Subjects
The minus: notes from **2+ subjects** competing for the same resource.
```dataview
TABLE WITHOUT ID key AS "Fought over", unique(rows.category) AS Subjects, rows.file.link AS Notes
FROM "notes"
FLATTEN competes_for AS node
WHERE node
GROUP BY node
WHERE length(unique(rows.category)) >= 2
SORT length(unique(rows.category)) DESC
```

## 🧩 Shared Mechanisms (Kind 1)
Concepts shared by **2+ subjects**.
```dataview
TABLE WITHOUT ID key AS Concept, unique(rows.category) AS Subjects, rows.file.link AS Notes
FROM "notes"
FLATTEN concepts AS concept
WHERE concept
GROUP BY concept
WHERE length(unique(rows.category)) >= 2
```

## ⏳ Waiting for a Bond Pass
```dataview
TABLE category AS Subject, date AS Date
FROM "notes"
WHERE !bonded
SORT date ASC
```

## 🏷 Names in Use
Check here before creating a new era, person, place, thread, cause, effect or concept. Reuse a match.
```dataview
TABLE WITHOUT ID key AS Name, length(rows) AS Notes, unique(rows.category) AS Subjects
FROM "notes"
FLATTEN flat(list(era, people, place, threads, causes, enables, competes_for, concepts)) AS name
WHERE name
GROUP BY name
SORT length(rows) DESC
```
