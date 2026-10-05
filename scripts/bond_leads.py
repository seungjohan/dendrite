#!/usr/bin/env python3
"""Bond leads for a bond pass: where two study notes meet, how, and why that might be a bond.

Constellate's linking algorithm, adapted to study notes (LINKING.md §6). In
Constellate an LLM writes a "thinking flow" for every saved web page and links
are found where two flows meet. Here the flow is already half-written: every
note answers the shadow question in its frontmatter (when, who, where), and
three fields give it a direction:

    causes        what made this happen             (Constellate's `up`)
    enables       what this made possible            (Constellate's `down`)
    competes_for  the resource it fought others for  (the minus: Nike ⇄ Nintendo on free time)

Two notes meet wherever they name the same thing, and *how* they name it is
the kind of lead — the Kind 2 sub-types of LINKING.md §1, plus Kind 1 concepts.
Era, people and place are context: they add weight but never make a lead on
their own, because "both are about Europe" fails the quality bar.

This script proposes. It never writes into a note: a lead becomes a bond only
when the bond pass can finish "connects because ___" with a mechanism.

    python3 scripts/bond_leads.py [--vault PATH] [--top 20]
"""

from __future__ import annotations

import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

# kind: (weight, can make a lead on its own)
KINDS = {
    "led-to": (1.0, True),          # A enabled X, and X is one cause of B
    "common-cause": (1.0, True),    # X caused both
    "competition": (0.9, True),     # both fought for X
    "same-mechanism": (0.8, True),  # both are cases of one concept atom (Kind 1)
    "shared-thread": (0.8, True),   # both sit on one hidden thread
    "complement": (0.7, True),      # both fed X
    "same-person": (0.5, False),
    "same-era": (0.3, False),
    "same-place": (0.3, False),
}

# The point of Dendrite is bonding *different* subjects (Burt's structural
# holes, LINKING.md §5): a lead inside one subject is the one you would have
# found anyway, so it is kept but ranked down.
SAME_SUBJECT = 0.5
DECAY = 0.7          # each extra note a storyline passes through is a little less sure
CONTEXT_PAIR = 2     # context-only leads need this many shared context names
STORY_SUBJECTS = 3   # a name in this many subjects is "secretly one story" (AGENTS bond pass step 7)

FIELDS = ("era", "people", "place", "threads", "concepts", "causes", "enables", "competes_for")
CONTEXT = {"era": "same-era", "people": "same-person", "place": "same-place"}
STOP = set("""about after again also because been before being between both could does doing during each
from have into just like made make many more most much only other over same some such than that their them
then there these they this those through very were what when where which while whom whose why with would
your it's don't""".split())


@dataclass
class Note:
    name: str
    subject: str
    fields: dict[str, list[str]]
    bonds: set[str]
    text: str
    bond_kinds: list[tuple[str, str, str]] = field(default_factory=list)  # (other, kind, found by)


@dataclass
class Lead:
    a: str
    b: str
    score: float = 0.0
    because: list[str] = field(default_factory=list)
    kinds: set[str] = field(default_factory=set)


def _links(value: str) -> list[str]:
    """Names in a frontmatter value: [[links]] (alias dropped) or bare words."""
    found = re.findall(r"\[\[([^\]|#]+)", value)
    if found:
        return [f.strip() for f in found]
    value = value.strip().strip("[]")
    return [v.strip().strip("\"'") for v in value.split(",") if v.strip().strip("\"'")]


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"\A---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).split("\n"):
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv:
            key = kv.group(1)
            out[key] = kv.group(2)
        elif key and re.match(r"^\s+-\s", line):
            out[key] += ", " + line.split("-", 1)[1].strip()
    return out


def key(name: str) -> str:
    """One spelling per thing, so `[[17th century]]` meets `[[1600s]]` and
    `[[The Printing Press]]` meets `[[printing press]]` — the "reuse before you
    mint" rule, checked rather than trusted."""
    k = name.lower().strip()
    k = re.sub(r"^the\s+", "", k)
    century = re.match(r"^(\d{1,2})(st|nd|rd|th)[\s-]century$", k)
    if century:
        k = f"{int(century.group(1)) - 1}00s"
    k = re.sub(r"[\s_-]+", " ", k)
    # Plurals only on ordinary words: "1600s", "Augustus", "physics", "press" keep their s.
    last = k.split(" ")[-1]
    if len(last) > 4 and last.endswith("s") and not last.endswith(("ss", "us", "is", "ics")) and not last[0].isdigit():
        k = k[:-1]
    return k


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {heading}.*?\n(.*?)(?=^## |^---|\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def typed_bonds(section: str) -> list[tuple[str, str, str]]:
    """Bond lines as (other note, kind, found by). LINKING.md §4's format is
    `- [[other]] · kind: connects because … (found by: me)`; a bond written
    before kinds existed reads as "untyped"."""
    out = []
    for line in section.split("\n"):
        m = re.match(r"^\s*-\s*\[\[([^\]|#]+)[^\]]*\]\]\s*(?:·\s*([^:]+))?:", line)
        if m:
            by = re.search(r"\(found by:\s*([^)]+)\)", line)
            out.append((m.group(1).strip(), (m.group(2) or "untyped").strip().lower(),
                        by.group(1).strip().lower() if by else "?"))
    return out


def load(vault: Path) -> list[Note]:
    notes = []
    for path in sorted((vault / "notes").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        bonds = _section(text, "🔗 Bonds")
        notes.append(Note(
            name=path.stem,
            subject=fm.get("category", "").strip() or "?",
            fields={f: _links(fm.get(f, "")) for f in FIELDS},
            bonds=set(re.findall(r"\[\[([^\]|#]+)", bonds)),
            text=re.sub(r"\A---\n.*?\n---", "", text, count=1, flags=re.S),
            bond_kinds=typed_bonds(bonds),
        ))
    return notes


def bond_kinds(notes: list[Note]) -> dict[str, dict[str, int]]:
    """{kind: {found by: count}}, each bond once though it is written on both notes."""
    names = {n.name for n in notes}
    seen: dict[frozenset, tuple[str, str]] = {}
    for n in notes:
        for other, kind, by in n.bond_kinds:
            if other in names and other != n.name:
                seen.setdefault(frozenset((n.name, other)), (kind, by))
    out: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for kind, by in seen.values():
        out[kind][by] += 1
    return {k: dict(v) for k, v in sorted(out.items())}


def idf(notes: list[Note]) -> dict[str, float]:
    df: dict[str, int] = defaultdict(int)
    for n in notes:
        for k in {key(v) for vs in n.fields.values() for v in vs}:
            df[k] += 1
    return {k: math.log((len(notes) + 1) / (c + 1)) + 1 for k, c in df.items()}


def _keys(note: Note, f: str) -> dict[str, str]:
    return {key(v): v for v in note.fields.get(f, [])}


def meet(a: Note, b: Note, weight: dict[str, float]) -> Lead:
    lead = Lead(a.name, b.name)

    def add(kind: str, k: str, sentence: str):
        w, _ = KINDS[kind]
        lead.score += w * weight.get(k, 1.0)
        lead.kinds.add(kind)
        lead.because.append(sentence)

    for first, second in ((a, b), (b, a)):
        for k, shown in _keys(first, "enables").items():
            if k in _keys(second, "causes"):
                add("led-to", k, f"{first.name} enabled [[{shown}]], one cause of {second.name}")
    pairs = (("causes", "common-cause", "[[{}]] caused both"),
             ("competes_for", "competition", "both fought for [[{}]]"),
             ("concepts", "same-mechanism", "both are cases of `{}`"),
             ("threads", "shared-thread", "both sit on the thread [[{}]]"),
             ("enables", "complement", "both fed [[{}]]"),
             ("people", "same-person", "same person, [[{}]]"),
             ("era", "same-era", "same era, [[{}]]"),
             ("place", "same-place", "same place, [[{}]]"))
    for f, kind, sentence in pairs:
        theirs = _keys(b, f)
        for k, shown in _keys(a, f).items():
            if k in theirs:
                add(kind, k, sentence.format(shown))
    if a.subject == b.subject:
        lead.score *= SAME_SUBJECT
    return lead


def shown(lead: Lead) -> bool:
    """A lead is worth a bond pass's time when one kind could carry a bond on
    its own, or when enough context lines up that a mechanism is worth looking for."""
    if any(KINDS[k][1] for k in lead.kinds):
        return True
    return len(lead.because) >= CONTEXT_PAIR


def leads(notes: list[Note]) -> tuple[list[Lead], list[Lead]]:
    """(new leads, leads that are already bonds) — best first, ties by name so
    two runs over the same notes print the same list."""
    weight = idf(notes)
    new, known = [], []
    for a, b in combinations(notes, 2):
        lead = meet(a, b, weight)
        if not lead.because or not shown(lead):
            continue
        (known if b.name in a.bonds or a.name in b.bonds else new).append(lead)
    order = lambda l: (-l.score, l.a, l.b)
    return sorted(new, key=order), sorted(known, key=order)


def storylines(notes: list[Note], max_notes: int = 4) -> list[tuple[float, list[str], list[str]]]:
    """Chains of notes where each one enabled a cause of the next, crossing at
    least two subjects: the dig, followed across the vault instead of inside one note."""
    by_name = {n.name: n for n in notes}
    nxt: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for a in notes:
        for b in notes:
            if a is b:
                continue
            for k, shown_name in _keys(a, "enables").items():
                if k in _keys(b, "causes"):
                    nxt[a.name].append((b.name, shown_name))
                    break
    out = []

    def walk(path: list[str], via: list[str]):
        if len(path) >= 3 and len({by_name[p].subject for p in path}) >= 2:
            out.append((DECAY ** (len(path) - 2), list(path), list(via)))
        if len(path) == max_notes:
            return
        for b, through in sorted(nxt[path[-1]]):
            if b not in path:
                walk(path + [b], via + [through])

    for n in sorted(by_name):
        walk([n], [])
    return sorted(out, key=lambda s: (-s[0], -len(s[1]), s[1]))


def one_story(notes: list[Note]) -> list[tuple[str, list[str]]]:
    """Names that pull in STORY_SUBJECTS or more subjects."""
    subjects: dict[str, set[str]] = defaultdict(set)
    shown_as: dict[str, str] = {}
    for n in notes:
        for vs in n.fields.values():
            for v in vs:
                subjects[key(v)].add(n.subject)
                shown_as.setdefault(key(v), v)
    hits = [(shown_as[k], sorted(s)) for k, s in subjects.items() if len(s) >= STORY_SUBJECTS]
    return sorted(hits, key=lambda h: (-len(h[1]), h[0]))


def variants(notes: list[Note]) -> list[list[str]]:
    """Different spellings of what is probably one name — to merge by hand."""
    spell: dict[str, set[str]] = defaultdict(set)
    for n in notes:
        for vs in n.fields.values():
            for v in vs:
                spell[key(v)].add(v)
    return sorted(sorted(s) for s in spell.values() if len(s) > 1)


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zà-ÿ]{4,}", text.lower()) if w not in STOP}


def open_questions(vault: Path, notes: list[Note]) -> list[tuple[str, str, str, list[str]]]:
    """Open questions in the Question log that a note may answer: shared words
    only, so a hint for the bond pass to read, not an answer."""
    path = vault / "logs" / "Question log.md"
    if not path.exists():
        return []
    out = []
    for row in path.read_text(encoding="utf-8").split("\n"):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.match(r"^Q\d+$", cells[0]) or cells[-1].lower() != "open":
            continue
        qid, subject, question = cells[0], cells[2], cells[3]
        words = _words(question)
        for n in notes:
            shared = sorted(words & _words(n.text))
            if len(shared) >= 2 and qid not in n.text:
                out.append((qid, question, n.name, shared))
    return sorted(out, key=lambda o: (-len(o[3]), o[0], o[2]))


def report(vault: Path, top: int = 20) -> str:
    notes = load(vault)
    new, known = leads(notes)
    subject = {n.name: n.subject for n in notes}
    lines = [f"# Bond leads — {len(notes)} notes, {len({n.subject for n in notes})} subjects", ""]
    if len(notes) < 2:
        lines += ["Nothing to meet yet: leads need two notes.", ""]
    lines += ["## Leads, best first", "Leads, not bonds. Write one only if you can finish *connects because ___* "
              "with a mechanism (LINKING.md §4).", ""]
    for l in new[:top]:
        tag = "" if any(KINDS[k][1] for k in l.kinds) else " · context only — look for a mechanism"
        lines.append(f"- {l.score:.2f} · [[{l.a}]] ({subject[l.a]}) ⇄ [[{l.b}]] ({subject[l.b]}){tag}")
        lines += [f"  - {s}" for s in l.because]
    if not new:
        lines.append("- none")
    names = {n.name for n in notes}
    bonded = {frozenset((n.name, o)) for n in notes for o in n.bonds if o in names and o != n.name}
    lines += ["", "## Bonds you already have",
              f"The fields see {len(known)} of your {len(bonded)} bonds; the rest were found some other way "
              "(a measure of what the fields miss, not a fault in the bond)." if bonded else "None yet.", ""]
    kinds = bond_kinds(notes)
    if kinds:
        lines += ["By kind, and who found them:", ""]
        lines += [f"- {k}: " + ", ".join(f"{by} {c}" for by, c in sorted(v.items())) for k, v in kinds.items()]
        lines.append("")
    stories = storylines(notes)
    if stories:
        lines += ["## Storylines", "Each note enabled one cause of the next.", ""]
        for score, path, via in stories[:5]:
            steps = f"[[{path[0]}]]" + "".join(f" —{v}→ [[{p}]]" for v, p in zip(via, path[1:]))
            lines.append(f"- {score:.2f} · {steps}")
        lines.append("")
    story = one_story(notes)
    if story:
        lines += ["## Secretly one story", f"Names in {STORY_SUBJECTS}+ subjects.", ""]
        lines += [f"- [[{name}]] — {', '.join(subs)}" for name, subs in story]
        lines.append("")
    spellings = variants(notes)
    if spellings:
        lines += ["## Same name, different spellings", "Merge to one (reuse before you mint).", ""]
        lines += ["- " + " · ".join(f"[[{v}]]" for v in group) for group in spellings]
        lines.append("")
    qs = open_questions(vault, notes)
    if qs:
        lines += ["## Open questions a note may touch", "Shared words only — read before claiming an answer.", ""]
        lines += [f"- {q} *{text}* ← [[{name}]] ({', '.join(shared)})" for q, text, name, shared in qs[:top]]
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> None:
    vault = Path(argv[argv.index("--vault") + 1]) if "--vault" in argv else Path(__file__).resolve().parent.parent
    top = int(argv[argv.index("--top") + 1]) if "--top" in argv else 20
    print(report(vault, top))


if __name__ == "__main__":
    main(sys.argv[1:])
