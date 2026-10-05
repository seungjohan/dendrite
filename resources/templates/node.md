---
stage: hub
category: node
---

> [!IMPORTANT] Key Takeaway
> **What it is:** 
> **Why it's a node:** the third thing these notes meet through (LINKING.md §1). Make this page only once 2+ notes name it.

# {{title}}

## ➡ What it caused
Notes that name this in `causes`.
```dataview
TABLE WITHOUT ID file.link AS Note, category AS Subject, date AS Date
FROM "notes"
WHERE contains(default(causes, list()), this.file.link)
SORT date
```

## ⬅ What made it possible
Notes that name this in `enables`.
```dataview
TABLE WITHOUT ID file.link AS Note, category AS Subject, date AS Date
FROM "notes"
WHERE contains(default(enables, list()), this.file.link)
SORT date
```

## ⚔ Who fought over it
Notes that name this in `competes_for`: unlike things on opposite sides of one resource.
```dataview
TABLE WITHOUT ID file.link AS Note, category AS Subject, date AS Date
FROM "notes"
WHERE contains(default(competes_for, list()), this.file.link)
SORT category
```

## 🧵 In its time, place, hands, or thread
```dataview
TABLE WITHOUT ID file.link AS Note, category AS Subject, date AS Date
FROM "notes"
WHERE contains(flat(list(era, people, place, threads)), this.file.link)
SORT date
```

## 💭 What these have in common
<!-- My words, once the lists above say something. Not a summary of the notes. -->
