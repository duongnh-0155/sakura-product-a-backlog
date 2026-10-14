"""Unit tests for score.py. Run: /usr/bin/python3 -m unittest test_score -v"""
from __future__ import annotations

import unittest

from score import (bucket, complexity_bucket, complexity_raw, scope_bucket, fib_ceil, parse_metrics, score_items, score_leaf, scope_raw,
                   select_samples)


def m(**kw):
    base = {"screens": 0, "apis": 0, "tables": 0, "states": 0, "rules": 0, "integrations": 0, "test_vectors": 0}
    base.update(kw)
    return base


class FibAndBucket(unittest.TestCase):
    def test_fib_ceil(self):
        for x, want in [(1, 1), (2, 2), (3, 3), (4, 5), (6, 8), (9, 13), (12, 13), (15, 21), (20, 21), (25, 34), (99, 34)]:
            self.assertEqual(fib_ceil(x), want, x)

    def test_scope_bucket_thresholds(self):
        for raw, want in [(0, 1), (2, 1), (2.5, 2), (4, 2), (4.5, 3), (7, 3), (7.5, 4), (11, 4), (11.5, 5), (40, 5)]:
            self.assertEqual(scope_bucket(raw), want, raw)

    def test_complexity_bucket_thresholds(self):
        for raw, want in [(0, 1), (2, 1), (2.5, 2), (5, 2), (5.5, 3), (9, 3), (9.5, 4), (14, 4), (14.5, 5), (40, 5)]:
            self.assertEqual(complexity_bucket(raw), want, raw)
        self.assertEqual(bucket(3), 2)  # default thresholds = scope


class RawFormulas(unittest.TestCase):
    def test_scope_raw(self):
        self.assertEqual(scope_raw(m(screens=1, apis=2, tables=2, integrations=1)), 1 * 2 + 2 + 3 + 2)

    def test_complexity_raw_with_constraint_and_type(self):
        base = complexity_raw(m(states=4, rules=3, integrations=1, test_vectors=6), "none", "fe")
        self.assertEqual(base, 4 + 4.5 + 2 + 3)
        self.assertEqual(complexity_raw(m(states=4, rules=3, integrations=1, test_vectors=6), "BR-INC-01", "tech"), base + 3)
        self.assertEqual(complexity_raw(m(), "なし", "migration"), 1)

    def test_parse_metrics(self):
        body = "## 概要\n<!-- swp-metrics: screens=1 apis=2 tables=2 states=4 rules=3 integrations=1 test_vectors=6 -->\n"
        self.assertEqual(parse_metrics(body), m(screens=1, apis=2, tables=2, states=4, rules=3, integrations=1, test_vectors=6))
        self.assertIsNone(parse_metrics("no metrics here"))
        self.assertEqual(parse_metrics("<!-- swp-metrics: screens=1 -->")["apis"], 0)


class LeafScoring(unittest.TestCase):
    def test_single_static_screen(self):
        r = score_leaf({"metrics": m(screens=1), "constraint": "none", "type": "fe"})
        self.assertEqual((r["scope"], r["complexity"], r["swp"]), (1, 1, 1))  # screens*2 = 2 -> scope 1 (static screen)

    def test_brief_example(self):
        # screens=1 apis=2 tables=2 states=4 rules=3 integrations=1 test_vectors=6, constraint none, type fe
        r = score_leaf({"metrics": m(screens=1, apis=2, tables=2, states=4, rules=3, integrations=1, test_vectors=6), "type": "fe"})
        self.assertEqual((r["scope"], r["complexity"]), (4, 4))  # raw 9 -> 4 ; raw 13.5 -> 4
        self.assertEqual(r["swp"], 21)  # 16 -> 21

    def test_typical_backend_issue(self):
        # apis=4 tables=2 states=2 rules=2 test_vectors=4 -> scope raw 7 (3), complexity raw 7 (3) -> 9 -> 13
        r = score_leaf({"metrics": m(apis=4, tables=2, states=2, rules=2, test_vectors=4), "type": "be"})
        self.assertEqual((r["scope"], r["complexity"], r["swp"]), (3, 3, 13))

    def test_missing_metrics_flagged(self):
        r = score_leaf({"body": "no metrics", "constraint": "BR-INC-01", "type": "tech"})
        self.assertTrue(r["missing"])
        self.assertEqual((r["scope"], r["complexity"], r["swp"]), (1, 1, 1))
        self.assertTrue(r["warnings"])

    def test_metrics_from_body_when_field_absent(self):
        r = score_leaf({"body": "<!-- swp-metrics: screens=2 apis=1 -->", "type": "fe"})
        self.assertFalse(r["missing"])
        self.assertEqual(r["scope"], 3)  # raw 5 -> scope 3


def tree():
    return [
        {"key": "E1", "title": "epic", "level": "Epic", "parent": None, "children": ["I1", "I2"]},
        {"key": "I1", "title": "issue with subs", "level": "Issue", "parent": "E1", "children": ["S1", "S2"],
         "metrics": m(screens=9), "type": "fe", "constraint": "none"},
        {"key": "S1", "title": "sub a", "level": "Sub-issue", "parent": "I1", "children": [], "metrics": m(screens=1), "type": "fe"},
        {"key": "S2", "title": "sub b", "level": "Sub-issue", "parent": "I1", "children": [], "metrics": m(states=3, rules=2), "type": "fe",
         "constraint": "business-day"},
        {"key": "I2", "title": "leaf issue", "level": "Issue", "parent": "E1", "children": [], "body": "<!-- swp-metrics: apis=4 tables=2 states=2 -->",
         "type": "be", "constraint": "none"},
    ]


class TreeScoring(unittest.TestCase):
    def test_parent_is_sum_and_not_scored_directly(self):
        s = score_items(tree())
        self.assertFalse(s["I1"]["is_leaf"])
        self.assertIsNone(s["I1"]["scope"])
        self.assertEqual(s["I1"]["swp"], s["S1"]["swp"] + s["S2"]["swp"])
        self.assertEqual(s["E1"]["swp"], s["I1"]["swp"] + s["I2"]["swp"])
        self.assertEqual(s["S2"]["epic"], "E1")

    def test_parent_pointer_only_relationship(self):
        items = tree()
        items[0]["children"] = []  # only parent pointers, no children lists
        items[1]["children"] = []
        s = score_items(items)
        self.assertEqual(s["E1"]["children"], ["I1", "I2"])
        self.assertEqual(s["E1"]["swp"], s["I1"]["swp"] + s["I2"]["swp"])

    def test_sample_selection_deterministic(self):
        s = score_items(tree())
        a, b = select_samples(s, n=30, seed=42), select_samples(s, n=30, seed=42)
        self.assertEqual(a, b)
        self.assertIn("S2", a)  # constrained leaf
        self.assertTrue(all(s[k]["is_leaf"] for k in a))
        self.assertEqual(len(select_samples(s, n=2, seed=42)), 2)


if __name__ == "__main__":
    unittest.main()
