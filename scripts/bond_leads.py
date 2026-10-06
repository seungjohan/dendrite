#!/usr/bin/env python3
"""Bond leads for a bond pass, from the latest linking algorithm (flowlink.py).

Every note is a thinking flow, read from its frontmatter (LINKING.md §1–§2):

    causes        → up      +1   what made it happen
    enables       → down    +1   what it made possible
    weakens       → down    −1   what it undermined
    competes_for  → down    −1   a budget it fought others for (marked limited: rivals)
    chain         → chain        "[[A]] -> [[B]]" (raises) or "[[A]] -| [[B]]" (lowers)
    people        → entities

flowlink finds where two flows meet — feeds, works against, rivals, pulls
against, opposite stakes — through chains of up to three steps, edges two notes
agree on, rarity and hubs, exactly as Constellate does.

**Dates count more here than in Constellate**, where they only read trends:

- *Historical time* (`year`, else `era`) orders cause and effect: a note that
  "led to" one whose events were over before it began is demoted to hindsight.
  And it decides the two Kind 2 sub-types Constellate counts only as weight —
  **common cause** (both caused by X) and **complement** (both fed X) — which
  are reasons here when the two notes sit in one historical moment (the 1600s
  obsession with the infinitely small behind microscope and calculus), and
  shared topics otherwise.
- *Study time* (`date`) is the reminder Dendrite exists for: a link to a note
  studied long ago counts more, and the report lists what was studied a month,
  three months and a year ago this week.

Kind 1 (`concepts`) and `threads` are Dendrite's own and are reasons; era,
people and place add weight only. A lead inside one subject counts half.

It prints. It never writes into a note: a lead becomes a bond only when the
bond pass can finish "connects because ___".

    python3 scripts/bond_leads.py [--vault PATH] [--top 20] [--today YYYY-MM-DD]
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flowlink as fl  # noqa: E402

FIELDS = ("era", "people", "place", "threads", "concepts", "causes", "enables", "weakens", "competes_for")

# Dendrite's own kinds, beside flowlink's: (weight, can make a lead alone)
OWN = {
    "same mechanism": (0.8, True),   # Kind 1: one concept atom
    "same thread": (0.8, True),
    "same person": (0.5, False),
    "same era": (0.3, False),
    "same place": (0.3, False),
}
# flowlink's ally kinds that become reasons inside one historical moment
SAME_MOMENT_KINDS = {"shared-exposure": "common cause", "co-drivers": "complement"}
SAME_MOMENT_YEARS = 50
# Dendrite is about *what* I studied; dates help but come second (N314), so
# they nudge rather than lift: Dayweb is the vault where time leads.
SAME_MOMENT = 1.1       # two notes in one historical moment
LONG_AGO_DAYS = 90
LONG_AGO = 1.1          # a link to something studied long ago: the reminder
SAME_SUBJECT = 0.5      # bridging subjects is the point (Burt, LINKING.md §5)
# What I studied, in my notes' own words (📖 What I Studied, the takeaway, the
# question): Constellate's summary similarity, here across subjects only — two
# notes of one subject sharing words is the subject itself.
W_STUDY = 1.0
STUDY_REASON = 0.25     # cosine at which shared study words carry a lead alone
CONTEXT_PAIR = 2        # context-only leads need this many shared context names
STORY_SUBJECTS = 3
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
    bond_kinds: list[tuple[str, str, str]] = field(default_factory=list)
    chain: list[tuple[str, str, int]] = field(default_factory=list)
    studied: date | None = None
    when: fl.When | None = None


@dataclass
class Lead:
    a: str
    b: str
    score: float = 0.0
    because: list[str] = field(default_factory=list)
    kinds: set[str] = field(default_factory=set)
    reason: bool = False


# ── reading notes ───────────────────────────────────────────────────────────

def _links(value: str) -> list[str]:
    found = re.findall(r"\[\[([^\]|#]+)", value)
    if found:
        return [f.strip() for f in found]
    value = value.strip().strip("[]")
    return [v.strip().strip("\"'") for v in value.split(",") if v.strip().strip("\"'")]


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"\A---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out, key_ = {}, None
    for line in m.group(1).split("\n"):
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv:
            key_ = kv.group(1)
            out[key_] = kv.group(2)
        elif key_ and re.match(r"^\s+-\s", line):
            out[key_] += ", " + line.split("-", 1)[1].strip()
    return out


def key(name: str) -> str:
    """One spelling per thing, so `[[17th century]]` meets `[[1600s]]` — the
    vault's merged names (flowlink's `same`), checked rather than trusted."""
    k = name.lower().strip()
    k = re.sub(r"^the\s+", "", k)
    century = re.match(r"^(\d{1,2})(st|nd|rd|th)[\s-]century$", k)
    if century:
        k = f"{int(century.group(1)) - 1}00s"
    k = re.sub(r"[\s_-]+", " ", k)
    last = k.split(" ")[-1]
    if len(last) > 4 and last.endswith("s") and not last.endswith(("ss", "us", "is", "ics")) and not last[0].isdigit():
        k = k[:-1]
    return k


def chain_of(value: str) -> list[tuple[str, str, int]]:
    """`[[A]] -> [[B]]` raises B, `[[A]] -| [[B]]` lowers it."""
    return [(a.strip(), b.strip(), 1 if arrow in ("->", "→") else -1)
            for a, arrow, b in re.findall(r"\[\[([^\]|#]+)[^\]]*\]\]\s*(->|-\||→|⊣)\s*\[\[([^\]|#]+)", value)]


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {heading}.*?\n(.*?)(?=^## |^---|\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def typed_bonds(section: str) -> list[tuple[str, str, str]]:
    """Bond lines as (other note, kind, found by); an older bond reads as "untyped"."""
    out = []
    for line in section.split("\n"):
        m = re.match(r"^\s*-\s*\[\[([^\]|#]+)[^\]]*\]\]\s*(?:·\s*([^:]+))?:", line)
        if m:
            by = re.search(r"\(found by:\s*([^)]+)\)", line)
            out.append((m.group(1).strip(), (m.group(2) or "untyped").strip().lower(),
                        by.group(1).strip().lower() if by else "?"))
    return out


def _date(value: str) -> date | None:
    try:
        return date.fromisoformat(value.strip()[:10])
    except ValueError:
        return None


def load(vault: Path) -> list[Note]:
    notes = []
    for path in sorted((vault / "notes").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        bonds = _section(text, "🔗 Bonds")
        fields = {f: _links(fm.get(f, "")) for f in FIELDS}
        era = fields["era"][0] if fields["era"] else None
        notes.append(Note(
            name=path.stem,
            subject=fm.get("category", "").strip() or "?",
            fields=fields,
            bonds=set(re.findall(r"\[\[([^\]|#]+)", bonds)),
            text=re.sub(r"\A---\n.*?\n---", "", text, count=1, flags=re.S),
            bond_kinds=typed_bonds(bonds),
            chain=chain_of(fm.get("chain", "")),
            studied=_date(fm.get("date", "")),
            when=fl.when(fm.get("year", "").strip()) or fl.when(era),
        ))
    return notes


def names_of(notes: list[Note]) -> dict[str, str]:
    """key → the spelling a note used first, so sentences read in the vault's words."""
    out: dict[str, str] = {}
    for n in notes:
        for vs in [*n.fields.values(), [x for a, b, _ in n.chain for x in (a, b)]]:
            for v in vs:
                out.setdefault(key(v), v)
    return out


def flow_of(n: Note, names: dict[str, str]) -> dict:
    nm = lambda v: names[key(v)]
    down = {nm(v): 1 for v in n.fields["enables"]}
    down.update({nm(v): -1 for v in n.fields["weakens"] + n.fields["competes_for"]})
    up = {nm(v): 1 for v in n.fields["causes"] if nm(v) not in down}
    return {"up": up, "down": down, "chain": [[nm(a), nm(b), s] for a, b, s in n.chain],
            "entities": [nm(p) for p in n.fields["people"]]}


def web_of(notes: list[Note]) -> fl.Web:
    names = names_of(notes)
    limited = {names[key(v)] for n in notes for v in n.fields["competes_for"]}
    return fl.Web({n.name: flow_of(n, names) for n in notes}, limited=limited,
                  when={n.name: n.when for n in notes if n.when})


# ── meeting ─────────────────────────────────────────────────────────────────

def _span(w: fl.When | None) -> str:
    if w is None:
        return "?"
    a, b = int(w.start), int(w.end) - 1
    show = lambda y: f"{-y} BC" if y < 0 else str(y)
    return show(a) if a >= b else f"{show(a)}–{show(b)}"


def study_vectors(notes: list[Note]) -> dict[str, dict[str, float]]:
    """TF-IDF over what each note says was studied."""
    import math
    docs = {}
    for n in notes:
        parts = [_section(n.text, "📖 What I Studied"), _section(n.text, "🤔 The Question")]
        take = re.search(r"\*\*In one line:\*\*(.*)", n.text)
        docs[n.name] = [w for w in re.findall(r"[a-zà-ÿ]{4,}", " ".join(parts + [take.group(1) if take else ""]).lower())
                        if w not in STOP]
    df: dict[str, int] = defaultdict(int)
    for ws in docs.values():
        for w in set(ws):
            df[w] += 1
    N = len(docs) or 1
    out = {}
    for name, ws in docs.items():
        tf: dict[str, int] = defaultdict(int)
        for w in ws:
            tf[w] += 1
        v = {w: (1 + math.log(c)) * math.log((N + 1) / df[w]) for w, c in tf.items() if df[w] >= 2}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        out[name] = {w: x / norm for w, x in v.items()}
    return out


def meet(a: Note, b: Note, web: fl.Web, study: dict | None = None) -> Lead:
    lead = Lead(a.name, b.name)
    if study and a.subject != b.subject:
        va, vb = study.get(a.name, {}), study.get(b.name, {})
        cos = sum(x * vb.get(w, 0.0) for w, x in va.items())
        if cos > 0:
            shared = sorted((w for w in va if w in vb), key=lambda w: -va[w] * vb[w])[:4]
            lead.score += W_STUDY * cos
            lead.kinds.add("same study")
            lead.reason |= cos >= STUDY_REASON
            lead.because.append(f"same study: both studied {', '.join(shared)}")
    gap = fl.years_apart(a.when, b.when)
    same_moment = gap is not None and gap <= SAME_MOMENT_YEARS
    for m in web.meet(a.name, b.name):
        if m.kind in SAME_MOMENT_KINDS:
            kind, reason = SAME_MOMENT_KINDS[m.kind], same_moment
            tail = "" if same_moment else " (not one historical moment: a shared topic)"
        else:
            kind, reason, tail = fl.label(m), fl.can_justify(m), ""
        lead.score += m.score
        lead.kinds.add(kind)
        lead.reason |= reason
        lead.because.append(f"{kind}: {m.sentence.replace('{A}', a.name).replace('{B}', b.name)}{tail}")
    for f, kind, sentence in (("concepts", "same mechanism", "both are cases of `{}`"),
                              ("threads", "same thread", "both sit on the thread [[{}]]"),
                              ("people", "same person", "same person, [[{}]]"),
                              ("era", "same era", "same era, [[{}]]"),
                              ("place", "same place", "same place, [[{}]]")):
        theirs = {key(v) for v in b.fields[f]}
        for v in a.fields[f]:
            if key(v) in theirs:
                w, alone = OWN[kind]
                lead.score += w
                lead.kinds.add(kind)
                lead.reason |= alone
                lead.because.append(sentence.format(v))
    if lead.because and same_moment:
        lead.score *= SAME_MOMENT
        lead.because.append(f"one historical moment ({_span(a.when)} · {_span(b.when)})")
    if lead.because and a.studied and b.studied and abs((a.studied - b.studied).days) >= LONG_AGO_DAYS:
        lead.score *= LONG_AGO
        lead.because.append(f"studied {abs((a.studied - b.studied).days)} days apart: a reminder")
    if a.subject == b.subject:
        lead.score *= SAME_SUBJECT
    return lead


def shown(lead: Lead) -> bool:
    return lead.reason or sum(1 for k in lead.kinds if k in OWN) >= CONTEXT_PAIR


def leads(notes: list[Note]) -> tuple[list[Lead], list[Lead]]:
    """(new leads, leads that are already bonds), best first, ties by name."""
    web, study = web_of(notes), study_vectors(notes)
    new, known = [], []
    for a, b in combinations(notes, 2):
        lead = meet(a, b, web, study)
        if not lead.because or not shown(lead):
            continue
        (known if b.name in a.bonds or a.name in b.bonds else new).append(lead)
    order = lambda l: (-l.score, l.a, l.b)
    return sorted(new, key=order), sorted(known, key=order)


# ── the vault in time ───────────────────────────────────────────────────────

def timeline(notes: list[Note]) -> list[Note]:
    """Notes in the order their events happened."""
    return sorted((n for n in notes if n.when), key=lambda n: (n.when.start, n.name))


def storylines(notes: list[Note], steps: int = 5) -> list[tuple[list[str], float]]:
    """The dig, followed through the vault in historical order: the chain of
    notes, each a lead with a reason to the next, whose weakest link is
    strongest (flowlink.storyline). Notes without a date sit this out."""
    dated = timeline(notes)
    web, study = web_of(notes), study_vectors(notes)
    weight = {}
    for i, a in enumerate(dated):
        for b in dated[i + 1:]:
            lead = meet(a, b, web, study)
            if lead.reason:
                weight[a.name, b.name] = lead.score
    chain, weak = fl.storyline([n.name for n in dated], weight, steps=steps)
    subject = {n.name: n.subject for n in notes}
    return [(chain, weak)] if len(chain) >= 3 and len({subject[c] for c in chain}) >= 2 else []


def studied_ago(notes: list[Note], today: date, slack: int = 3) -> list[tuple[str, Note]]:
    """Notes studied a year, three months or a month ago this week."""
    out = []
    for label_, days in (("a year ago", 365), ("three months ago", 91), ("a month ago", 30)):
        out += [(label_, n) for n in notes if n.studied and abs((today - n.studied).days - days) <= slack]
    return out


def one_story(notes: list[Note]) -> list[tuple[str, list[str]]]:
    subjects: dict[str, set[str]] = defaultdict(set)
    names = names_of(notes)
    for n in notes:
        for vs in n.fields.values():
            for v in vs:
                subjects[key(v)].add(n.subject)
    hits = [(names[k], sorted(s)) for k, s in subjects.items() if len(s) >= STORY_SUBJECTS]
    return sorted(hits, key=lambda h: (-len(h[1]), h[0]))


def variants(notes: list[Note]) -> list[list[str]]:
    spell: dict[str, set[str]] = defaultdict(set)
    for n in notes:
        for vs in n.fields.values():
            for v in vs:
                spell[key(v)].add(v)
    return sorted(sorted(s) for s in spell.values() if len(s) > 1)


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


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zà-ÿ]{4,}", text.lower()) if w not in STOP}


def open_questions(vault: Path, notes: list[Note]) -> list[tuple[str, str, str, list[str]]]:
    """Open questions a note may answer: shared words only, a hint to read."""
    path = vault / "logs" / "Question log.md"
    if not path.exists():
        return []
    out = []
    for row in path.read_text(encoding="utf-8").split("\n"):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.match(r"^Q\d+$", cells[0]) or cells[-1].lower() != "open":
            continue
        qid, question = cells[0], cells[3]
        words = _words(question)
        for n in notes:
            shared = sorted(words & _words(n.text))
            if len(shared) >= 2 and qid not in n.text:
                out.append((qid, question, n.name, shared))
    return sorted(out, key=lambda o: (-len(o[3]), o[0], o[2]))


def report(vault: Path, top: int = 20, today: date | None = None) -> str:
    today = today or date.today()
    notes = load(vault)
    new, known = leads(notes)
    subject = {n.name: n.subject for n in notes}
    lines = [f"# Bond leads — {len(notes)} notes, {len({n.subject for n in notes})} subjects", f"*{fl.VERSION}*", ""]
    if len(notes) < 2:
        lines += ["Nothing to meet yet: leads need two notes.", ""]
    lines += ["## Leads, best first", "Leads, not bonds. Write one only if you can finish *connects because ___* "
              "with a mechanism (LINKING.md §4).", ""]
    for l in new[:top]:
        tag = "" if l.reason else " · context only — look for a mechanism"
        lines.append(f"- {l.score:.2f} · [[{l.a}]] ({subject[l.a]}) ⇄ [[{l.b}]] ({subject[l.b]}){tag}")
        lines += [f"  - {s}" for s in l.because]
    if not new:
        lines.append("- none")
    names = {n.name for n in notes}
    bonded = {frozenset((n.name, o)) for n in notes for o in n.bonds if o in names and o != n.name}
    lines += ["", "## Bonds you already have",
              f"The fields see {len(known)} of your {len(bonded)} bonds; the rest were found some other way "
              "(a field to fill, not a fault in the bond)." if bonded else "None yet.", ""]
    kinds = bond_kinds(notes)
    if kinds:
        lines += ["By kind, and who found them:", ""]
        lines += [f"- {k}: " + ", ".join(f"{by} {c}" for by, c in sorted(v.items())) for k, v in kinds.items()]
        lines.append("")
    ago = studied_ago(notes, today)
    if ago:
        lines += ["## Studied this week, back then", ""]
        lines += [f"- {label_} ({n.studied}): [[{n.name}]]" for label_, n in ago]
        lines.append("")
    tl = timeline(notes)
    if tl:
        lines += ["## Timeline", "In the order the events happened (`year`, else `era`).", ""]
        lines += [f"- {_span(n.when)} · [[{n.name}]] ({n.subject})" for n in tl]
        lines.append("")
    for chain, weak in storylines(notes):
        lines += ["## Storyline", f"Each note a reason to the next, in historical order; weakest link {weak:.2f}.", "",
                  " → ".join(f"[[{c}]]" for c in chain), ""]
    story = one_story(notes)
    if story:
        lines += ["## Secretly one story", f"Names in {STORY_SUBJECTS}+ subjects: each deserves a node page.", ""]
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
    today = date.fromisoformat(argv[argv.index("--today") + 1]) if "--today" in argv else None
    print(report(vault, top, today))


if __name__ == "__main__":
    main(sys.argv[1:])
