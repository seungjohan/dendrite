# Dendrite: Agent Manual

Rules for any AI agent working in this vault. Read this file, [README.md](README.md) (the why) and [LINKING.md](LINKING.md) (the how) before touching notes.

## What this vault is

**Dendrite** is the user's lifelong study log. Every subject they study (math, music, French, biology, art, history, anything) goes into one consistent note format. The goal is to **bond different subjects into one connected experience** by surfacing unexpected connections (의외의 연결성) between them.

Your job: keep notes consistent, and **propose honest connections the user hasn't noticed**. You are a proposer of connections, not just a filer of notes.

## 📁 Structure

| Path | Purpose |
|---|---|
| `README.md` | Spark, inspirations, goal, system, decisions. The user's "don't forget why" page. |
| `AGENTS.md` | This file. |
| `LINKING.md` | The linking algorithm: Kind 1 / Kind 2 / the dig, the quality bar, and §6 how notes meet. |
| `index.md` | Hub with Dataview tables. Don't hand-write note lists here. |
| `logs/Study log.md` | One row per study session: what was studied, every day, note or not. |
| `logs/Question log.md` | Questions only, with IDs (`Q1`, `Q2`…) and status `open` / `answered`. |
| `logs/Connection log.md` | Which question connects to which study: `raised by` / `answered by` / `connects to`. |
| `logs/Bond log.md` | One row per bond pass, so the next pass knows where to start. |
| `logs/Decision log.md` | Decisions about how the system works, and what's still open on purpose. Check it before suggesting a change. |
| `notes/` | One note per thing worth keeping. Filename: `{Subject} - {Descriptive Title}.md` |
| `concepts/` | Kind-1 mechanism atoms. Create one only when **2+ notes** share it. |
| `resources/templates/dendrite.md` | The one note template. |
| `scripts/bond_leads.py` | Ranked bond leads for a bond pass. Prints only; never writes a note. Tests: `python3 -m unittest discover scripts`. |

Era, people, place and thread pages (`[[1600s]]`, `[[Julius Caesar]]`) are **not pre-created**. Unresolved links are fine and still work as meeting points. Create the page only when there's real content to put in it.

## 📝 Note format

Every note uses the `dendrite` template. Frontmatter order is strict:

```yaml
---
stage: log                 # log | concept | hub | general
category: french           # the subject, lowercase
date: 2026-09-17
source: French class       # book, course, video, conversation…
range: "Unit 4, p.52–55"   # the range the user studied
era: "[[Ancient Rome]]"    # link: when the content happened
people: ["[[Julius Caesar]]"]
place: "[[Rome]]"
threads: []                # links: hidden shared variables beyond era/people/place (Kind 2)
causes: []                 # links: what made this happen (LINKING.md §6)
enables: []                # links: what this made possible
competes_for: []           # links: what it fought others for (the minus)
concepts: []               # Kind-1 mechanism atoms, e.g. [ratios-create-harmony]
bonded: 2026-09-24         # set by the bond pass; blank until then
---
```

Every note ends with the template's **🕸 Meets this note** Dataview footer. Keep it; don't edit its output.

Sections, in this order, always:
1. `> [!IMPORTANT] Key Takeaway` with **In one line** and **Why it stuck**
2. `## 📖 What I Studied`
3. `## 🤔 The Question`: *why* questions, each as `**Q#:** Why …?` matching its [[Question log]] ID
4. `## 🧵 Where the Thread Led`
5. `## 🔗 Bonds`
6. `## 💭 Reflection: {Descriptive Subtitle}`. The subtitle always names the takeaway. Never plain "Thoughts".

## 📥 Logging input (user's rules, these take priority)

- **Input comes in any form:** text, pictures or files. Read all of it.
- **The user picks the range** they studied (from where to where). Log only that range. Ignore anything in the picture or file that's outside it.
- **Organize, don't add.** Don't exaggerate, overwork, or add information beyond what they studied. No extra explanations, background, examples or outside research in the note. If a section has nothing from the studied range, leave it empty.
- **Save new guidelines here.** When the user gives a rule like this for how to work, add it to this file.

### Two kinds of input

**1. A question or idea, with no study attached.** Something the user wondered about in daily life, on a walk or in passing, e.g. *"why is grass always green?"*. This is a living log entry, not a note.
- Goes in [[Question log]] only, in **their** words, status `open`.
- No note and no [[Study log]] row: nothing was studied yet.
- The purpose is the habit: don't stop at being curious. The open queue is what they come back to answer when they have time. When a later study answers one, add the [[Connection log]] row and flip the status to `answered`.

**2. Study material.** Notes, photos, files, media, any form. This becomes a note, following the range and "organize, don't add" rules above.

### Draft first, always
- **Nothing is written to the vault until the user confirms.** Both kinds of input come back as a draft **in chat** first. They check, fix and confirm; only then file it.
- **One draft per topic.** Several topics in one day means several separate drafts. Never merge two topics into one note, even from the same session.
- After drafting, say what's ready and stop. Don't file, don't log, don't set `bonded:`.

### The three logs (every time the user logs a study)
1. **[[Study log]]:** always add a row (date, subject, what, range, note link or blank), even if no note gets written.
2. **[[Question log]]:** add each question the user raised as a new row with the next ID. Use their question, not yours. Status `open` unless the studied range answered it.
3. **[[Connection log]]:** link the question to the study: `raised by` for where it came up, `answered by` when a study explains it (then set its status to `answered`), `connects to` when a later study turns out to matter for it. Each row needs a *"connects because ___"* reason.
- Before logging, **read the open questions.** If today's study answers or connects to one, add the Connection log row and tell the user.
- All logs: newest row on top, never reorder, never delete or rewrite past rows (only a question's Status changes).

## ✍️ Writing rules

- **The user's words are the record.** When they tell you about something they studied in chat, write the note for them. Put *their* thinking in 💭 Reflection with the wording lightly cleaned but their framing kept, including any Korean terms. Don't over-formalize.
- **Never make the user categorize or tidy.** They talk; you structure.
- **Facts must be correct.** Study notes are for learning. Verify dates and claims. If the user's memory of a fact is off, gently note the correction in the note, as the README does for pointillism being about 200 years after calculus. The corrected version is often the more interesting connection.
- **The Question may be empty**, but always ask about it or look for it. It's the doorway to connections.
- **Why, not what.** Keep *why* questions (why is it like this, why then, why there, why by them). A *what* question ("what's the passé composé?") is a lookup, not a question for this section or the Question log. If the user asks one, answer it in chat, or ask them what surprised them about it.

## 🔁 Bond pass (when the user asks, ideally weekly)

Start from the index's **⏳ Waiting for a Bond Pass** table (`bonded` blank) plus any note changed since the last date in [[Bond log]]. For each:

1. **Fill context links.** Make sure `era`, `people` and `place` are set where they honestly apply, and `causes`, `enables`, `competes_for` where the note itself says so (LINKING.md §6). Empty is fine; a guessed cause is a fake link. **Reuse before you mint:** check the index's **🏷 Names in Use** table and reuse an existing name when it fits. Create a new name only when nothing does.
2. **Run `python3 scripts/bond_leads.py`**, then **search the whole vault** anyway: the script only sees the fields. Look for real relationships, in the three kinds from [LINKING.md](LINKING.md):
   - **Kind 1, analogy:** same mechanism in a different subject → shared `concepts:` atom.
   - **Kind 2, hidden shared variable:** unlike subjects wired to the same era, person, place or cause → shared context link or a `threads:` entry. **This is the kind the user values most. Prioritize it.**
   - **The dig:** a *why* question that opens into another field → expand 🧵 Where the Thread Led.
3. **Write bonds** in 🔗 Bonds on *both* notes: `- [[other note]]: connects because {specific mechanism} (found by: bond pass)`. Bonds the user spots themselves get `(found by: me)`.
4. **Quality bar.** Only bond if you can finish *"connects because ___"* with a specific mechanism, not a shared topic. **A note with no honest bond gets none.** A fake bond is worse than no bond, because it poisons a graph the user is learning to trust.
5. **Check open questions.** Does any note in this pass answer or connect to an `open` question in [[Question log]]? Add a [[Connection log]] row.
6. **Record the pass.** Set `bonded:` to today on every note checked, and add a row to [[Bond log]].
7. **Report back briefly:** new bonds, and any era, person, thread or concept that now pulls in **3+ subjects**. Those are the "secretly one story" moments. Suggest, don't restructure unasked.

## 🗓 Monthly look-back (when asked)

Summarize from the logs: which subjects were studied ([[Study log]]), which hubs gained the most cross-subject notes, the most surprising bond of the month, and questions still `open` in [[Question log]].

## 🚫 Don'ts

- Don't create concept or hub pages for a single note.
- Don't hand-edit Dataview output or turn `index.md` into a manual list.
- Don't delete notes. If one turns out wrong, correct it and say what changed.
- Don't turn this into a product or add scripts unless the user asks. [[Decision log]] says Obsidian first. (`bond_leads.py` was asked for, 2026-10-05.)

## 🔗 Relationship to other vaults

Dendrite works alongside two other vaults in `~/Obsidian/`. Each holds a different thing. Don't file the same material twice.

| Vault | Holds | Example |
|---|---|---|
| **Dendrite** | Study: the thing worth keeping, its questions and its bonds | `French - Why September Means Seven` |
| **seungjohan** `seungjohan/logbook/` | Activity: what the user *did* today across domains | a row in `Language log`: `fr · months · French class` |
| **seungjohan** subject folders | Reference: material the user looks things up in | `language/français/la Grammaire/`, `music/harmony/Interval` |
| **curiosity-lab** | Ideation and research: startup/project ideas, the linking theory | `wiki/stream.md`, `wiki/research/system/` |

- **Link, don't copy.** Wikilinks don't cross vaults. Point to another vault with an Obsidian URI, e.g. `[Interval](obsidian://open?vault=seungjohan&file=music%2Fharmony%2FInterval)`.
- **Context, not bonds.** In a bond pass you may cite a seungjohan or curiosity-lab note as background ("see also"), but 🔗 Bonds and the logs only link Dendrite notes.
- **Idea → curiosity-lab.** If a study note becomes a startup or project idea, suggest capturing it in curiosity-lab's `wiki/stream.md`. Don't file ideation here.
- **Origin.** Dendrite was born in curiosity-lab. The linking theory in [LINKING.md](LINKING.md) comes from there (`LINKING.md`, `wiki/research/system/connecting_the_dot.md`, `wiki/research/system/two-kinds-of-connection.md`).
- **Don't edit other vaults from here.** Each has its own AGENTS rules. Suggest the change and let the user do it there.
