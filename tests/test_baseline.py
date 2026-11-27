"""基线登记算子单测：登记即立约，重复即拒，修订留痕。"""
import unittest

from hengshu import Baseline, BaselineError


class TestBaseline(unittest.TestCase):
    def test_register(self):
        b = Baseline()
        rec = b.register("recall", 0.9, note="召回下限")
        self.assertEqual(rec["capability"], "recall")
        self.assertEqual(rec["threshold"], 0.9)
        self.assertEqual(rec["metric"], "gte")
        self.assertEqual(rec["version"], 1)

    def test_register_rejects_duplicate(self):
        b = Baseline()
        b.register("recall", 0.9)
        with self.assertRaises(BaselineError):
            b.register("recall", 0.8)  # 只增不覆盖：同名重复登记即拒

    def test_register_rejects_unknown_metric(self):
        b = Baseline()
        with self.assertRaises(BaselineError):
            b.register("recall", 0.9, metric="approx")

    def test_lte_metric(self):
        """lte=开销上限：实测不高于阈值才算达标。"""
        b = Baseline()
        rec = b.register("latency_ms", 200, metric="lte")
        self.assertEqual(rec["metric"], "lte")

    def test_revise_keeps_history(self):
        b = Baseline()
        b.register("recall", 0.9)
        rec = b.revise("recall", 0.85, reason="压测口径修正")
        self.assertEqual(rec["threshold"], 0.85)
        self.assertEqual(rec["version"], 2)
        hist = b.history()
        self.assertEqual(hist[0]["action"], "register")
        self.assertEqual(hist[1]["action"], "revise")
        self.assertEqual(hist[1]["old_threshold"], 0.9)  # 旧标准留痕

    def test_revise_requires_reason(self):
        b = Baseline()
        b.register("recall", 0.9)
        with self.assertRaises(BaselineError):
            b.revise("recall", 0.85, reason="")

    def test_revise_unknown_capability(self):
        b = Baseline()
        with self.assertRaises(BaselineError):
            b.revise("ghost", 0.5, reason="无此能力")

    def test_items_snapshot(self):
        b = Baseline()
        b.register("recall", 0.9)
        items = b.items()
        items["recall"]["threshold"] = 0.1  # 外改副本不伤正册
        self.assertEqual(b.items()["recall"]["threshold"], 0.9)

    def test_version_monotonic(self):
        b = Baseline()
        b.register("a", 1)
        b.register("b", 2)
        b.revise("a", 3, reason="r")
        self.assertEqual(b.version(), 3)


if __name__ == "__main__":
    unittest.main()
