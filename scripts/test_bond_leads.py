"""Tests for bond_leads.py on a small made-up vault. Run: python3 -m unittest discover scripts"""

import tempfile
import unittest
from pathlib import Path

import bond_leads as bl


def note(subject, body="", bonds="", **fields):
    fm = "\n".join(f"{k}: {v}" for k, v in fields.items())
    return f"---\nstage: log\ncategory: {subject}\n{fm}\n---\n\n# x\n\n{body}\n\n## 🔗 Bonds\n{bonds}\n\n## 💭 Reflection: x\n"


VAULT = {
    "Physics - Lenses": note("physics", body="Lens grinding turned glass into a way to see tiny worlds.",
                             era='"[[1600s]]"', enables='["[[the infinitely small]]"]',
                             bonds="- [[Math - Calculus]] · led to: connects because lens-grinding showed the infinitely small (found by: me)"),
    "Math - Calculus": note("math", era='"[[17th century]]"', causes='["[[The Infinitely Small]]"]',
                            enables='["[[mechanical worldview]]"]'),
    "Biology - Cells": note("biology", causes='["[[the infinitely small]]"]', people='["[[Robert Hooke]]"]',
                           bonds="- [[Latin - Caesar]]: connects because an old bond, before kinds (found by: bond pass)"),
    "History - Clockmakers": note("history", causes='["[[mechanical worldview]]"]'),
    "Games - Nintendo": note("games", competes_for='["[[free time]]"]'),
    "Sport - Running": note("sport", competes_for='["[[free time]]"]', concepts="[habit-loops]"),
    "Sport - Swimming": note("sport", competes_for='["[[free time]]"]'),
    "French - Months": note("french", era='"[[Ancient Rome]]"', place='"[[Rome]]"', people='["[[Julius Caesar]]"]'),
    "Latin - Caesar": note("latin", era='"[[Ancient Rome]]"', place='"[[Rome]]"'),
    "Art - Mosaics": note("art", place='"[[Rome]]"'),
}
QUESTIONS = """| ID | Date | Subject | Question | Status |
| -- | ---- | ------- | -------- | ------ |
| Q2 | 2026-10-01 | physics | Why did grinding glass change what people could see? | open |
| Q1 | 2026-09-17 | french | Why does septembre mean seven? | answered |
"""


class BondLeads(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.vault = Path(cls.tmp.name)
        (cls.vault / "notes").mkdir()
        (cls.vault / "logs").mkdir()
        for name, text in VAULT.items():
            (cls.vault / "notes" / f"{name}.md").write_text(text, encoding="utf-8")
        (cls.vault / "logs" / "Question log.md").write_text(QUESTIONS, encoding="utf-8")
        cls.notes = bl.load(cls.vault)
        cls.new, cls.known = bl.leads(cls.notes)

    def pair(self, a, b, pool=None):
        for l in (pool if pool is not None else self.new):
            if {l.a, l.b} == {a, b}:
                return l
        return None

    def test_names_meet_across_spellings(self):
        self.assertEqual(bl.key("17th century"), bl.key("1600s"))
        self.assertEqual(bl.key("The Infinitely Small"), bl.key("the infinitely small"))
        for word in ("1600s", "Augustus", "physics", "press"):
            self.assertTrue(bl.key(word).endswith("s"), word)

    def test_led_to_names_the_direction(self):
        l = self.pair("Math - Calculus", "History - Clockmakers")
        self.assertIn("led-to", l.kinds)
        self.assertIn("Math - Calculus enabled [[mechanical worldview]], one cause of History - Clockmakers", l.because)

    def test_common_cause_across_spellings(self):
        l = self.pair("Math - Calculus", "Biology - Cells")
        self.assertIn("common-cause", l.kinds)

    def test_competition_is_the_minus(self):
        l = self.pair("Games - Nintendo", "Sport - Running")
        self.assertEqual(l.kinds, {"competition"})
        self.assertIn("both fought for [[free time]]", l.because)

    def test_same_subject_ranks_below_a_bridge(self):
        across = self.pair("Games - Nintendo", "Sport - Running")
        inside = self.pair("Sport - Running", "Sport - Swimming")
        self.assertLess(inside.score, across.score)

    def test_context_alone_needs_two_names(self):
        self.assertIsNotNone(self.pair("French - Months", "Latin - Caesar"))   # era + place
        self.assertIsNone(self.pair("Latin - Caesar", "Art - Mosaics"))        # place only
        self.assertFalse(any(bl.KINDS[k][1] for k in self.pair("French - Months", "Latin - Caesar").kinds))

    def test_existing_bonds_are_not_proposed_again(self):
        self.assertIsNone(self.pair("Physics - Lenses", "Math - Calculus"))
        self.assertIsNotNone(self.pair("Physics - Lenses", "Math - Calculus", self.known))

    def test_storyline_follows_enables_into_causes(self):
        paths = [p for _, p, _ in bl.storylines(self.notes)]
        self.assertIn(["Physics - Lenses", "Math - Calculus", "History - Clockmakers"], paths)

    def test_secretly_one_story(self):
        story = dict(bl.one_story(self.notes))
        self.assertEqual(story["the infinitely small"], ["biology", "math", "physics"])
        self.assertNotIn("free time", story)  # games and sport: two subjects, not three

    def test_spellings_to_merge(self):
        self.assertIn(["1600s", "17th century"], bl.variants(self.notes))

    def test_open_question_hint(self):
        hits = {(q, n): shared for q, _, n, shared in bl.open_questions(self.vault, self.notes)}
        self.assertEqual(hits[("Q2", "Physics - Lenses")], ["glass", "grinding"])
        self.assertFalse(any(q == "Q1" for q, _ in hits))  # answered questions are left alone

    def test_bonds_are_counted_by_kind_and_finder(self):
        self.assertEqual(bl.bond_kinds(self.notes), {"led to": {"me": 1}, "untyped": {"bond pass": 1}})

    def test_same_report_twice(self):
        self.assertEqual(bl.report(self.vault), bl.report(self.vault))

    def test_writes_nothing(self):
        before = {p: p.read_text() for p in (self.vault / "notes").glob("*.md")}
        bl.report(self.vault)
        self.assertEqual(before, {p: p.read_text() for p in (self.vault / "notes").glob("*.md")})


if __name__ == "__main__":
    unittest.main()
