---
stage: general
category: system
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** Connecting the dots (의외의 연결성) is the whole point of Dendrite. It isn't a personal knack. It's a well-studied field with named theories, and a system can do the remembering instead of luck.
> **How to use it:** Tag each note's context (`era`, `people`, `place`, `threads`) and mechanisms (`concepts`). Bonds need a reason. Kind 2 is the connection I want most.
> **Carried over from:** `curiosity-lab`: `LINKING.md`, `wiki/research/system/connecting_the_dot.md`, `wiki/research/system/two-kinds-of-connection.md`

# Linking System

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
| You find it by | going **up**: abstract until they meet | going **sideways**: what each touches (era, person, place, cause) | going **down**: "why is it like this?" |
| Study example | music intervals ≈ number ratios | microscope + calculus ← the 1600s | *septembre* = 7 → Roman calendar → Caesar |
| Field in the note | `concepts:` | `era` · `people` · `place` · `threads` | 🤔 The Question → 🧵 Where the Thread Led |

⭐ **Kind 2 is the connection I find most exciting, and similarity alone can never find it.** Unlike things aren't similar. Embeddings and "looks alike" put them far apart, so they only meet through the third thing they share. That's why every note records its context as links.

### Kind 2 sub-types
- **Common cause:** one thing sets off many effects. *The 1600s obsession with the infinitely small → microscope, calculus.* One upstream node, many subjects.
- **Complement:** two things rise together. *Printing press ⇄ spread of literacy.*
- **Substitute / competition:** two things fight over the same resource and move in opposite directions. *Nike ⇄ Nintendo, both compete for free time* (the original example from curiosity-lab).

### The "shadow" question (for finding Kind 2)
Don't ask *"what is this similar to?"* Ask what surrounds it:
> **When did it happen? Who made it? Where? What caused it? What did it enable? What did it replace or compete with?**

Two notes whose answers land on the **same node** are bonded, even if they look nothing alike. Era, people and place are the answers every note gets. `threads:` holds the rest, e.g. `[[the infinitely small]]`, `[[power writes itself into time]]`, `[[printing press]]`.

---

## 2. Frontmatter = the connection fields

```yaml
era: "[[1600s]]"                  # Kind 2: when
people: ["[[Isaac Newton]]"]      # Kind 2: who
place: "[[England]]"              # Kind 2: where
threads: ["[[the infinitely small]]"]  # Kind 2: hidden cause / resource / theme
concepts: [ratios-create-harmony] # Kind 1: shared mechanism
```

- Context values are **links**, so notes meet in the graph and in the hub's "Where Subjects Meet" table automatically.
- Pages for era, people, place and threads **don't need to exist**. Create one only when there's something to write.
- Use consistent names. Always `[[1600s]]`, never `[[17th century]]` in one note and `[[1600s]]` in another. **Reuse before you mint:** check the index's *🏷 Names in Use* table before inventing a new one.
- Every note's *🕸 Meets this note* footer lists other notes sharing any of these fields. Those are leads for a bond, not bonds.

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

## References
- Ronald Burt: [Structural Holes and Good Ideas (2004)](https://snap.stanford.edu/class/cs224w-readings/Burt04StructureHole.pdf)
- Dedre Gentner: [Structure-Mapping: A Theoretical Framework for Analogy (1983)](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog0702_3)
- Genrich Altshuller: [TRIZ 40 Inventive Principles](https://innovation-triz.com/TRIZ40/)
- Andy Matuschak: [Evergreen notes vs Zettelkasten](https://notes.andymatuschak.org/Similarities_and_differences_between_evergreen_note-writing_and_Zettelkasten)
