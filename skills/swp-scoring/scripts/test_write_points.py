"""Unit tests for write_points.py (no network). Run: /usr/bin/python3 -m unittest test_write_points -v"""
from __future__ import annotations

import json
import os
import tempfile
import unittest

from write_points import final_swp, load_field_ids, plan_writes, reaggregate


def scores():
    return {
        "E": {"swp": 10, "children": ["I"], "item_id": "PVTI_e", "title": "epic"},
        "I": {"swp": 10, "children": ["a", "b"], "item_id": "PVTI_i", "title": "issue"},
        "a": {"swp": 8, "children": [], "item_id": "PVTI_a", "title": "a"},
        "b": {"swp": 2, "children": [], "item_id": "PVTI_b", "title": "b", "final_swp": 5, "reason": "過小"},
        "x": {"swp": 3, "children": [], "item_id": None, "title": "no item id"},
    }


class WritePoints(unittest.TestCase):
    def test_final_swp_priority(self):
        self.assertEqual(final_swp({"swp": 1, "reviewed_swp": 2, "final_swp": 3}), 3.0)
        self.assertEqual(final_swp({"swp": 1, "reviewed_swp": 2}), 2.0)
        self.assertIsNone(final_swp({}))

    def test_reaggregate_propagates_leaf_edits(self):
        s = reaggregate(scores())
        self.assertEqual(s["I"]["final_swp"], 13)
        self.assertEqual(s["E"]["final_swp"], 13)

    def test_plan_writes_marks_unchanged_and_skips(self):
        items = {"a": {"item_id": "PVTI_a", "fields": {"Point": 8}}}
        rows = {r["key"]: r for r in plan_writes(scores(), items)}
        self.assertEqual(rows["a"]["status"], "unchanged")
        self.assertEqual(rows["b"]["status"], "write")
        self.assertEqual(rows["b"]["value"], 5.0)
        self.assertEqual(rows["I"]["value"], 13.0)
        self.assertTrue(rows["x"]["status"].startswith("skip"))

    def test_load_field_ids(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "f.json")
            json.dump({"id": "PVT_x", "fields": {"nodes": [{"name": "Point", "id": "PVTF_p"}]}}, open(path, "w"))
            self.assertEqual(load_field_ids(path), {"project_id": "PVT_x", "field_id": "PVTF_p"})
            with self.assertRaises(ValueError):
                load_field_ids(path, "Hours")


if __name__ == "__main__":
    unittest.main()
