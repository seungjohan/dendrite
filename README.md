---
stage: general
category: system
---

> [!IMPORTANT] Key Takeaway
> **What this is:** A living log of everything I study, which grows connections between subjects so that all my learning becomes one connected experience.
> **Why it exists:** The more we live, the more we have to study. It never ends, so it should add up.
> **Start here:** [[index|Dendrite hub]] · [[AGENTS]] (how Claude works here) · [[LINKING]] (how notes connect)

# 🌿 Dendrite

*Grow a neuron web from everything you study.*

**Dendrites** are the branches of a neuron that take in signals from many other neurons, and they grow new branches as we learn. This project does the same thing: math, music, French and biology all feed in, and every new note is a chance for a new branch.

---

## ✨ The Spark

*Written down on 2026-09-17, in my own words:*

> I have one amazing experience while studying. I didn't recognize it, but when I studied biology, I was amazed by how the microscope was invented for a reason: to observe cells or even smaller things. On the other side, when I studied mathematics, I found out that they invented the logic of the integral. And when I studied art, they started to draw with a method of dots. It's not exactly the same era, but they started from similar generations.
>
> A different experience: when I started to study French, I found something weird. July and August don't match counting from one to ten. After that I found out the story is related to Julius Caesar, and that the number seven came from that. So it's not just a language. It's related to history, generations, era, interests, overall.
>
> Those examples are just my personal experiences that inspired the idea. The idea itself is **living logs of my study**, because the more we live, the more we have to study. It's an endless job if you care about personal development.

The origin entry is still in `curiosity-lab/wiki/stream.md` (2026-09-17, "subjects I study secretly talk to each other").

---

## 💡 Inspirations

The moments that made me want this. When a new one happens, add it here.

### 1. Microscope · Calculus · Dots in painting
- **Biology:** the microscope was invented to see the very small: cells and smaller things (Leeuwenhoek, 1670s).
- **Math:** calculus, the math of the infinitely small (Newton and Leibniz, 1660s–80s).
- **Art:** painting with dots, called pointillism (Seurat, 1880s).
- **What connects them:** the microscope and calculus really are the same generation. They share one hidden thread: an era obsessed with the infinitely small. Pointillism came about 200 years later, but it is still connected. Seurat built his dots on the science of his day about how the eye mixes color. The thread became *science changing how people see, and art following.*

### 2. French month names → Julius Caesar
- *Septembre, octobre, novembre, décembre* mean 7, 8, 9, 10, but they are months 9–12.
- The old Roman year started in **March**. Later, Julius Caesar (July) and Augustus (August) renamed months after themselves.
- **What it taught me:** a language isn't just vocabulary. A *why* question inside a subject is a door into history. → [[notes/French - Why September Means Seven]]

### 3. Math ⇄ Music
- They sound totally different, but they started as one thing. **Pythagoras** found that pleasing musical intervals are simple number ratios (octave 2:1, fifth 3:2).
- Medieval universities taught the **quadrivium** as one group: arithmetic, geometry, **music**, astronomy.
- Many mathematicians were also philosophers. Newton called his great work *Mathematical Principles of Natural Philosophy*.
- **What it taught me:** subjects are branches of one mainstream. They were split into departments fairly late, mostly in the 1800s. Dendrite reconnects what school split apart.

---

## 🎯 Goal

1. **A living log:** keep what I study for life, in one consistent format, no matter the subject.
2. **Study more efficiently:** new learning attaches to what I already know instead of starting from zero.
3. **Bond subjects into one experience:** find the common points (의외의 연결성, unexpected connections) so studying one thing makes everything else richer.

**What success looks like:** a few months from now, I'm studying something new and Dendrite shows me it connects to something I studied long ago, and that makes both stick.

---

## ⚙️ The System

### The loop
This is the one full copy of the loop. index points here.

1. **Log every session.** One row in [[Study log]]: what I studied today, note or not.
2. **Ask why.** Write down what doesn't add up as a *why* question (not a *what* question), even if I can't answer it yet. Each one goes in [[Question log]]. That's where connections start.
3. **Write a note when it's worth keeping.** One note per *thing worth keeping*, not per study session. Always use the `dendrite` template. Its 🕸 *Meets this note* footer shows other notes that share its context automatically.
4. **Tag the context.** `era`, `people`, `place` (and `threads`) are links. Notes from different subjects that share one meet automatically.
5. **Connect questions.** When a later study answers or touches an old question, record it in [[Connection log]].
6. **Bond pass (weekly).** Ask Claude to check notes that haven't been bonded yet. Every bond needs a reason: *"connects because ___"*. Each pass is recorded in [[Bond log]].
7. **Look back (monthly).** Which era, person or thread pulls in the most subjects? Which questions are still open? That's where my studies are secretly one story.

### The note template
Every note has the same sections, whatever the subject:

| Section | What goes there |
|---|---|
| **Key Takeaway** | One line, plus why it stuck |
| 📖 What I Studied | The facts, short |
| 🤔 The Question | A *why* question: what didn't add up or surprised me |
| 🧵 Where the Thread Led | Following the question out into history, people and other fields |
| 🔗 Bonds | Links to other notes, each with "connects because ___" |
| 💭 Reflection: {subtitle} | My own raw thinking, first person |
| 🕸 Meets this note | Automatic: other notes sharing an era, person, place, thread or concept |

### How notes connect
The full linking system is in [[LINKING]]. In short:
- **Kind 1, analogy:** two subjects share the same *mechanism* (e.g. ratios make harmony in both music and math). → `concepts:`
- **Kind 2, hidden shared variable:** two unlike subjects are wired to the *same third thing*: an era, a person, a place, a cause (e.g. microscope + calculus ← the 1600s). → `era` / `people` / `place` / `threads`
- **The dig:** a *why* question *inside* one subject that opens into history (e.g. why does September mean 7? → Caesar). → 🤔 The Question

### Folder layout
```
dendrite/
├── README.md        ← this file: spark, goal, system (read when I forget why)
├── AGENTS.md        ← rules for Claude
├── LINKING.md       ← the linking system
├── index.md         ← hub: all notes + where subjects meet
├── logs/            ← Study log · Question log · Connection log · Bond log
├── notes/           ← one note per thing worth keeping
├── concepts/        ← Kind-1 mechanisms (created only when 2+ notes share one)
└── resources/templates/dendrite.md
```
Era, people, place and thread pages (`[[1600s]]`, `[[Julius Caesar]]`) don't need to exist up front. An unresolved link still works as a meeting point in the graph. Create the page only once there's something to say about it.

---

## 🧭 Decisions (so I don't re-argue them)

| Date | Decision | Why |
|---|---|---|
| 2026-09-17 | **Obsidian first, not a product** | I don't know yet which way works best: connections that come to me, or me going looking. A few months of real logging will tell me. The real risk is whether I keep the habit, and Obsidian tests that almost for free. |
| 2026-09-17 | **Build a product only when…** | …I've logged for months, had real "wow" connections, and can say what a tool did that plain Obsidian couldn't. |
| 2026-09-17 | **Its own vault** | Moved out of curiosity-lab so study logs have their own space. |
| 2026-09-17 | **Name: Dendrite** | Chosen over *Soma* (the cell body where signals combine; it names the result, and the name is taken by other brands) and *Neuron Web* (clear but generic). Dendrite names the *process*: gathering, branching, growing. Also considered: Quadrivium, Septem, Polymath Log, Common Root. |
| 2026-09-17 | **One consistent template** | Whatever and however I study, the format stays the same, so notes can be compared and connected. |
| 2026-09-17 | **Three study logs, not only notes** | Study log (what I studied), Question log (questions only), Connection log (which question connects to which study). Not every session deserves a note, but every session and every question should leave a trace. Borrowed the quick-line idea from my seungjohan logbook. |
| 2026-09-17 | **Each vault holds one thing** | Dendrite = study and its bonds. seungjohan = daily activity and reference material. curiosity-lab = ideas and research. Link across vaults, don't copy. |

## ❓ Open Questions
- **Connections come to me, or I go looking?** Which one actually happens in practice? Watch for it.
- **Which hidden threads matter most for studying?** Era and people are obvious. What else: technology, war, trade, religion, a shared problem?
- **When does a note deserve to exist?** "Thing worth keeping" is a feeling for now. Sharpen it after 20 notes.
