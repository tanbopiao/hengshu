"""漂移巡检算子单测：逐项对照，缺项即漂移，不达即退化。"""
import unittest

from hengshu import Baseline, Patrol


class TestPatrol(unittest.TestCase):
    def setUp(self):
        self.b = Baseline()
        self.b.register("recall", 0.9)
        self.b.register("precision", 0.8)
        self.p = Patrol(self.b)

    def test_all_pass(self):
        report = self.p.inspect({"recall": 0.95, "precision": 0.8})
        self.assertTrue(report["passed"])
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["checked"], 2)

    def test_regression_found(self):
        report = self.p.inspect({"recall": 0.7, "precision": 0.9})
        self.assertFalse(report["passed"])
        f = report["findings"][0]
        self.assertEqual(f["capability"], "recall")
        self.assertEqual(f["kind"], "regression")
        self.assertEqual(f["baseline"], 0.9)
        self.assertEqual(f["observed"], 0.7)

    def test_missing_is_drift(self):
        """登记在册的能力观测缺失，视同漂移——能力消失也是退化。"""
        report = self.p.inspect({"recall": 0.95})
        self.assertFalse(report["passed"])
        f = report["findings"][0]
        self.assertEqual(f["capability"], "precision")
        self.assertEqual(f["kind"], "missing")
        self.assertIsNone(f["observed"])

    def test_lte_direction(self):
        b = Baseline()
        b.register("latency_ms", 200, metric="lte")
        p = Patrol(b)
        self.assertTrue(p.inspect({"latency_ms": 180})["passed"])
        report = p.inspect({"latency_ms": 250})
        self.assertFalse(report["passed"])
        self.assertEqual(report["findings"][0]["kind"], "regression")

    def test_rounds_recorded(self):
        self.p.inspect({"recall": 0.95, "precision": 0.9})
        self.p.inspect({"recall": 0.5, "precision": 0.9})
        self.assertEqual(len(self.p.rounds()), 2)
        self.assertFalse(self.p.rounds()[1]["passed"])

    def test_baseline_version_in_evidence(self):
        """巡检单附所依基线版本（该项登记/修订时的版本），判词可溯源。"""
        report = self.p.inspect({"recall": 0.1, "precision": 0.1})
        by_cap = {f["capability"]: f for f in report["findings"]}
        self.assertEqual(by_cap["recall"]["baseline_version"], 1)     # recall 于版本1登记
        self.assertEqual(by_cap["precision"]["baseline_version"], 2)  # precision 于版本2登记
        self.b.revise("recall", 0.5, reason="口径修正")
        report = self.p.inspect({"recall": 0.1, "precision": 0.1})
        by_cap = {f["capability"]: f for f in report["findings"]}
        self.assertEqual(by_cap["recall"]["baseline_version"], 3)      # 修订后版本
        self.assertEqual(by_cap["precision"]["baseline_version"], 2)   # 未修订仍原版本


if __name__ == "__main__":
    unittest.main()
