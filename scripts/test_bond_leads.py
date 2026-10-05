"""Tests for bond_leads.py on a small made-up vault. Run: cd scripts && python3 -m unittest"""

import tempfile
import unittest
from datetime import date
from pathlib import Path

import bond_leads as bl


def note(subject, body="", bonds="", **fields):
    fm = "\n".join(f"{k}: {v}" for k, v in fields.items())
    return f"---\nstage: log\ncategory: {subject}\n{fm}\n---\n\n# x\n\n{body}\n\n## 🔗 Bonds\n{bonds}\n\n## 💭 Reflection: x\n"


VAULT = {
    "Physics - Lenses": note("physics", body="Lens grinding turned glass into a way to see tiny worlds.",
                             year="1590-1610", date="2026-01-10", enables='["[[the infinitely small]]"]',
                             bonds="- [[Math - Calculus]] · led to: connects because lenses showed the infinitely small (found by: me)"),
    "Math - Calculus": note("math", year="1665-1687", date="2026-05-01", era='"[[17th century]]"',
                            causes='["[[The Infinitely Small]]"]', enables='["[[mechanical worldview]]"]'),
    "Biology - Cells": note("biology", year="1665", date="2026-05-02", era='"[[1600s]]"',
                            causes='["[[the infinitely small]]"]', people='["[[Robert Hooke]]"]',
                            bonds="- [[Latin - Caesar]]: connects because an old bond, before kinds (found by: bond pass)"),
    "History - Clockmakers": note("history", year="1700s", causes='["[[mechanical worldview]]"]'),
    "Myth - Old Clocks": note("myth", year="5th century BC", causes='["[[mechanical worldview]]"]'),
    "Games - Nintendo": note("games", competes_for='["[[free time]]"]'),
    "Sport - Running": note("sport", competes_for='["[[free time]]"]', concepts="[habit-loops]"),
    "Sport - Swimming": note("sport", competes_for='["[[free time]]"]'),
    "Print - Press": note("print", year="1450", enables='["[[literacy]]"]'),
    "Church - Monopoly": note("church", year="1400s", weakens='["[[literacy]]"]'),
    "Optics - Glass": note("optics", enables='["[[glass]]"]', chain='["[[glass]] -> [[lens making]]"]'),
    "Astronomy - Telescopes": note("astronomy", causes='["[[lens making]]"]'),
    "French - Months": note("french", era='"[[Ancient Rome]]"', place='"[[Rome]]"', people='["[[Julius Caesar]]"]'),
    "Latin - Caesar": note("latin", date="2025-10-05", era='"[[Ancient Rome]]"', place='"[[Rome]]"'),
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
        return next((l for l in (pool if pool is not None else self.new) if {l.a, l.b} == {a, b}), None)

    def test_a_cause_led_forward_in_time_feeds(self):
        l = self.pair("Math - Calculus", "History - Clockmakers")
        self.assertIn("feeds", l.kinds)
        self.assertTrue(l.reason)
        self.assertIn("feeds: Math - Calculus → more mechanical worldview → feeds History - Clockmakers", l.because)

    def test_a_cause_running_backwards_in_time_is_hindsight(self):
        self.assertIsNone(self.pair("Math - Calculus", "Myth - Old Clocks"))  # hindsight is no reason

    def test_common_cause_is_a_reason_inside_one_historical_moment(self):
        l = self.pair("Math - Calculus", "Biology - Cells")
        self.assertIn("common cause", l.kinds)
        self.assertTrue(l.reason)
        self.assertTrue(any(s.startswith("one historical moment") for s in l.because))

    def test_common_cause_across_two_thousand_years_is_a_shared_topic(self):
        self.assertIsNone(self.pair("History - Clockmakers", "Myth - Old Clocks"))

    def test_competition_is_the_minus(self):
        l = self.pair("Games - Nintendo", "Sport - Running")
        self.assertEqual(l.kinds, {"rivals"})

    def test_weakens_against_enables_pulls_against(self):
        l = self.pair("Print - Press", "Church - Monopoly")
        self.assertIn("pulls against", l.kinds)

    def test_a_chain_carries_a_cause_further(self):
        l = self.pair("Optics - Glass", "Astronomy - Telescopes")
        self.assertIn("feeds", l.kinds)

    def test_same_subject_ranks_below_a_bridge(self):
        self.assertLess(self.pair("Sport - Running", "Sport - Swimming").score,
                        self.pair("Games - Nintendo", "Sport - Running").score)

    def test_context_alone_needs_two_names(self):
        self.assertIsNotNone(self.pair("French - Months", "Latin - Caesar"))   # era + place
        self.assertIsNone(self.pair("Latin - Caesar", "Art - Mosaics"))        # place only
        self.assertFalse(self.pair("French - Months", "Latin - Caesar").reason)

    def test_existing_bonds_are_counted_not_proposed(self):
        self.assertIsNone(self.pair("Physics - Lenses", "Math - Calculus"))
        self.assertIsNotNone(self.pair("Physics - Lenses", "Math - Calculus", self.known))
        self.assertEqual(bl.bond_kinds(self.notes), {"led to": {"me": 1}, "untyped": {"bond pass": 1}})

    def test_studied_long_ago_counts_more(self):
        l = self.pair("Physics - Lenses", "Biology - Cells")
        self.assertTrue(any("days apart: a reminder" in s for s in l.because))

    def test_timeline_and_storyline_run_in_historical_order(self):
        order = [n.name for n in bl.timeline(self.notes)]
        self.assertEqual(order[0], "Myth - Old Clocks")
        self.assertLess(order.index("Physics - Lenses"), order.index("Math - Calculus"))
        chains = [c for c, _ in bl.storylines(self.notes)]
        self.assertTrue(any(c[-1] == "History - Clockmakers" and "Math - Calculus" in c for c in chains), chains)

    def test_studied_a_year_ago_this_week(self):
        hits = bl.studied_ago(self.notes, date(2026, 10, 7))
        self.assertEqual([(w, n.name) for w, n in hits], [("a year ago", "Latin - Caesar")])

    def test_spellings_to_merge(self):
        self.assertIn(["1600s", "17th century"], bl.variants(self.notes))

    def test_open_question_hint(self):
        hits = {(q, n): shared for q, _, n, shared in bl.open_questions(self.vault, self.notes)}
        self.assertEqual(hits[("Q2", "Physics - Lenses")], ["glass", "grinding"])
        self.assertFalse(any(q == "Q1" for q, _ in hits))

    def test_same_report_twice_and_nothing_written(self):
        before = {p: p.read_text() for p in (self.vault / "notes").glob("*.md")}
        self.assertEqual(bl.report(self.vault, today=date(2026, 10, 5)), bl.report(self.vault, today=date(2026, 10, 5)))
        self.assertEqual(before, {p: p.read_text() for p in (self.vault / "notes").glob("*.md")})


if __name__ == "__main__":
    unittest.main()
