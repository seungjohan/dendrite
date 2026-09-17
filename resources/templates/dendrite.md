---
stage: log
category: 
date: {{date}}
source: 
range: 
era: 
people: []
place: 
threads: []
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
<!-- Only if you can finish "connects because ___". Format: - [[other note]]: connects because ___ -->


## 💭 Reflection: 
<!-- Your own raw thinking. First person, any length. -->


---
#### 🕸 Meets this note
<!-- Auto: other notes sharing an era, person, place, thread or concept. Leads to check, not bonds. -->
```dataview
TABLE WITHOUT ID file.link AS Note, category AS Subject, shared AS "Meets at"
FROM "notes"
FLATTEN flat(list(era, people, place, threads, concepts)) AS shared
WHERE shared AND file.path != this.file.path
  AND contains(flat(list(this.era, this.people, this.place, this.threads, this.concepts)), shared)
SORT category
```
