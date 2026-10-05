---
stage: general
category: system
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Connecting the dots (의외의 연결성) is the whole point of Dendrite. It isn't a personal knack. It's a well-studied field with named theories, and a system can do the remembering instead of luck.
> **How to use it:** Tag each note's context (`era`, `people`, `place`, `threads`), its direction (`causes`, `enables`, `competes_for`) and mechanisms (`concepts`). Bonds need a reason and a kind. Kind 2 is the connection I want most.
> **Carried over from:** `curiosity-lab`: `LINKING.md`, `wiki/research/system/connecting_the_dot.md`, `wiki/research/system/two-kinds-of-connection.md`

# Linking Algorithm

## The core question

> How do I *deliberately* find a valuable, unexpected connection between two things I studied, instead of waiting to happen to remember both at the same time?

Memory is the enemy. The connection between a French note and a biology note only happens if both are in my head at once, which is rare and gets rarer the more I study. **The goal is to make the structure do the remembering.**

The mindset shift:
> Don't treat the vault as a **store for connections I already made**. Treat it as a **proposer of connections I didn't make.**

---

## 1. Three ways notes connect

| | **Kind 1: Analogy** | **Kind 2: Hidden shared variable** ⭐ | **The dig** |
|---|---|---|---|
| The link is | same abstract *shape / mechanism* | wired to the same *third thing* | a *why* question *inside* one subject that opens into another field |
| The two things are | alike underneath | often totally unlike | one subject, many layers |
| You find it by | going **up**: abstract until they meet | going **sideways**: what each touches, and which way (what caused it, what it made possible, what it fought for) | going **down**: "why is it like this?" |
| Study example | music intervals ≈ number ratios | microscope + calculus ← the 1600s | *septembre* = 7 → Roman calendar → Caesar |
| Field in the note | `concepts:` | direction: `causes` · `enables` · `competes_for`; context: `era` · `people` · `place` · `threads` | 🤔 The Question → 🧵 Where the Thread Led |

⭐ **Kind 2 is the connection I find most exciting, and similarity alone can never find it.** Unlike things aren't similar. Embeddings and "looks alike" put them far apart, so they only meet through the third thing they share. That's why every note records its context as links.

### Kind 2 sub-types, and the field each one lives in
Each sub-type is a *direction* through the third thing, so each has its own field. Two notes that
name the same thing in the same field meet as that sub-type, and the vault can say so.

| Sub-type | Shape | Fields that meet | Example |
|---|---|---|---|
| **Common cause** | one thing sets off many effects | both `causes: X` | *the 1600s obsession with the infinitely small → microscope, calculus* |
| **Led to** | one note made possible what caused the other | A `enables: X`, B `causes: X` | *lens grinding → the infinitely small → cell biology* |
| **Complement** | two things fed the same outcome | both `enables: X` | *printing press, schooling → literacy* |
| **Competition** (the minus) | two things fought over the same resource | both `competes_for: X` | *Nike ⇄ Nintendo, both fight for free time* |
| Context | same when, who, where, or theme | `era` · `people` · `place` · `threads` | a lead, not yet a reason |

The minus matters most: things that *compete* look nothing alike and never share words. It is
the original curiosity-lab example, and the one similarity will never find.

### The "shadow" question (for finding Kind 2)
Don't ask *"what is this similar to?"* Ask what surrounds it:
> **When did it happen? Who made it? Where? What caused it? What did it enable? What did it replace or compete with?**

Each question has its field, so the answer is written down *with its direction*:

| Question | Field |
|---|---|
| When? Who? Where? | `era` · `people` · `place` |
| What caused it? | `causes` |
| What did it enable? | `enables` |
| What did it replace or compete with? | `competes_for` (name the *resource* fought over: `[[free time]]`, not `[[Nintendo]]`) |
| What else runs through it? | `threads` |

Two notes whose answers land on the **same node** meet, even if they look nothing alike; *which*
fields they meet in says how.

---

## 2. Frontmatter = the connection fields

```yaml
era: "[[1600s]]"                  # Kind 2: when
people: ["[[Isaac Newton]]"]      # Kind 2: who
place: "[[England]]"              # Kind 2: where
threads: ["[[the infinitely small]]"]  # Kind 2: a theme that runs through it
causes: ["[[the infinitely small]]"]   # Kind 2, direction: what made it happen
enables: ["[[germ theory]]"]           # Kind 2, direction: what it made possible
competes_for: ["[[free time]]"]        # Kind 2, the minus: what it fought others for
concepts: [ratios-create-harmony] # Kind 1: shared mechanism
```

- Context values are **links**, so notes meet in the graph and in the hub's "Where Subjects Meet" table automatically.
- Pages for era, people, place and threads **don't need to exist**. Create one only when there's something to write.
- Use consistent names. Always `[[1600s]]`, never `[[17th century]]` in one note and `[[1600s]]` in another. **Reuse before you mint:** check the index's *🏷 Names in Use* table before inventing a new one.
- Leave a direction field empty when nothing honest fits. A guessed cause is a fake link.
- Every note's *🕸 Meets this note* footer lists the other notes it meets **by kind**: *⬅ led
  here via* (they enabled one of its causes), *➡ led on via* (it enabled one of theirs), *🌱 same
  cause*, *⚔ both fought for*, and *also shares* for the rest. Leads for a bond, not bonds.

### Pages for the third thing
When a node earns a page (`[[free time]]`, `[[1600s]]`), make it from the `node` template. It
lists every note by its **role** toward that node: what it caused, what made it possible, who
fought over it, what sits in it. The third thing is where unlike subjects meet, so its page is
the bridge itself made visible (Burt, §5): one page shows that French, astronomy and politics
were all moved by the same thing.

---

## 3. Writing a concept atom (Kind 1)

A **concept atom** is the underlying *mechanism* a note is an example of, not its topic. It lives in `concepts/`, one short file per atom, and is created only when **2+ notes from different subjects** share it.

- **Name a relation, not a noun.** `ratios-create-harmony` ✓ · `music` ✗. If the atom name is a topic, it's wrong. If it's a relation, it's right. (Gentner)
- **Keep the vocabulary small and reused.** An atom with one instance is a *candidate*, not a link yet.
- **Atoms get better over time.** When a new note instances one, re-read it and sharpen it. (Matuschak)

```markdown
---
stage: concept
category: system
---

# Ratios create harmony
Simple whole-number relationships feel "right" to people, in sound, in space, in proportion.
```

---

## 4. The quality bar

Only write a bond, or share a concept or thread, if you can finish:

> "This connects because **[specific mechanism]**, not just because they share a topic."

- "Both are about Europe" → too vague, skip.
- "Both were made possible by lens-grinding advances in the 1600s" → that's a bond.

**A note with no honest connection gets none.** A fake link is worse than an empty one, because it poisons the graph I'm learning to trust.

### Every bond names its kind
```
- [[other note]] · common cause: connects because ___ (found by: me | bond pass)
```
Kinds: **led to** · **common cause** · **complement** · **competition** · **same mechanism** ·
**same thread** · **the dig** · **other**. The kind makes the bond a typed edge, so the vault can
count what kind of connection I actually find, and whether I find it or the bond pass does
([[Decision log]]: "every bond records who found it").

---

## 5. The theory behind it

I built this on instinct, then found out I'd reinvented four established ideas. Each one gives Dendrite something concrete.

### 1. Structural holes: *where* the value is
**Ronald Burt** (*Structural Holes and Good Ideas*, 2004) showed on real organizational networks that good ideas come disproportionately from people who **bridge otherwise-disconnected groups**. The gap between two groups that don't know about each other is a "structural hole", and bridging it shows options neither side can see. This is the academic name for 의외의 연결성.
- **For Dendrite:** the most valuable notes are the ones that bridge distant subjects, not the ones deep inside one subject.

### 2. Structure-mapping: *how* to write a concept
**Dedre Gentner** (*Structure-Mapping*, 1983): a productive analogy aligns **relations**, not surface features. "Water waves → sound waves" works because the relational structure matches.
- **For Dendrite:** concept atoms name mechanisms, never topics. It's also the *limit* of Kind 1: similarity can't see Kind 2.

### 3. TRIZ: the same solution in unrelated fields
**Genrich Altshuller** studied a huge number of patents and found that inventions repeat across industries: the same abstract solution solves unrelated concrete problems. TRIZ's method: **abstract the problem → find where it was already solved in another field → translate it back.** Its ideas of *resources* and *contradiction* also underlie Kind 2.
- **For Dendrite:** when a subject solves a problem, ask where else that problem was solved.

### 4. Zettelkasten / evergreen notes: the note discipline
**Niklas Luhmann's** slip-box and **Andy Matuschak's** evergreen notes: **atomic, concept-oriented, densely linked, and revised over years.**
- **For Dendrite:** one note per thing worth keeping, and notes and atoms improve over time instead of just piling up.

### Similarity vs. relationships
> Vector embeddings capture *similarity* but not explicit relationships. A link graph captures *relationships* but can't infer unseen ones. They complement each other.

Dendrite has both halves. **Smart Connections** (installed) finds semantically similar notes, which covers Kind 1 candidates. The **context links** (era, people, place, threads) form the relationship graph, which covers Kind 2. The best proposals come from checking one against the other: two notes that are *similar but not bonded*, or *bonded through a hidden node but not similar*.

### Graph methods for later, when there are enough notes
| Technique | What it finds | For Dendrite |
|---|---|---|
| Common neighbors / link prediction | Pairs that *should* be linked | Notes sharing 2+ context links but no bond yet |
| Community detection | Natural clusters | My real subject groupings, and the gaps between them |
| Betweenness centrality | "Broker" nodes | The era, person or thread that bridges the most subjects |

Don't build any of this until the vault has enough notes to need it (see [[Decision log]]).

---

## 6. How the vault proposes

The rules above make every note a small map of what moved it and what it moved. Proposing is
then a matter of finding where two maps touch, saying how, and putting the rare touches first.

**In Obsidian, always on:** the footer's typed columns, the node pages, and the index tables
*🌱 One cause, many subjects* and *⚔ Fought over across subjects*.

**For a bond pass:** `python3 scripts/bond_leads.py` ranks every pair, and never writes a note:

- **Weight.** Each meeting counts by its kind (led to and common cause 1.0, competition 0.9,
  same mechanism and same thread 0.8, complement 0.7) and by how **rare** the node is: a node
  on most notes says little. Era, people and place add weight (0.3–0.5) but never make a lead
  alone; two of them together make a lead flagged *context only*.
- **Distance.** A lead inside one subject counts half. Bridging subjects is the point (§5).
- **Storylines.** Notes chained by *enables → causes* across subjects: the dig, followed through
  the vault instead of inside one note.
- **Secretly one story.** Nodes in 3+ subjects, the ones that deserve a node page.
- **Same name, different spellings**, to merge (`[[17th century]]` ⇄ `[[1600s]]`); leads already
  treat them as one.
- **Open questions** a note may touch (shared words only).
- **The test.** Bonds `found by: me` are the truth the fields are checked against: how many of
  them the fields can see, and the kinds of all bonds, by who found them. A bond the fields miss
  is a field to fill, not a fault in the bond.

The idea came from Constellate (my media archive), where links are found where two resources'
causes and effects meet; this section is how it fits study notes, which already answer the
shadow question.

---

## References
- Ronald Burt: [Structural Holes and Good Ideas (2004)](https://snap.stanford.edu/class/cs224w-readings/Burt04StructureHole.pdf)
- Dedre Gentner: [Structure-Mapping: A Theoretical Framework for Analogy (1983)](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog0702_3)
- Genrich Altshuller: [TRIZ 40 Inventive Principles](https://innovation-triz.com/TRIZ40/)
- Andy Matuschak: [Evergreen notes vs Zettelkasten](https://notes.andymatuschak.org/Similarities_and_differences_between_evergreen_note-writing_and_Zettelkasten)
