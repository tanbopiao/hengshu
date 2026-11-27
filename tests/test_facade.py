"""恒枢中枢门面单测：三算子合枢，原 guard 门面原样保留（只增不覆盖）。"""
import unittest

from hengshu import Hengshu, VerdictError


class TestFacade(unittest.TestCase):
    def setUp(self):
        self.h = Hengshu()

    def test_enroll_and_inspect_pass(self):
        self.h.enroll("recall", 0.9)
        self.h.enroll("latency_ms", 200, metric="lte")
        report = self.h.inspect({"recall": 0.95, "latency_ms": 150})
        self.assertTrue(report["passed"])

    def test_full_cycle_drift_to_discharge(self):
        """登记→退化→开案→修复→销账，全程留痕。"""
        self.h.enroll("recall", 0.9)
        report = self.h.inspect({"recall": 0.7})
        self.assertFalse(report["passed"])
        verdict = self.h.judge()  # 缺省裁最近一轮巡检
        self.assertEqual(len(verdict["opened"]), 1)
        rec = self.h.discharge("recall", action="回滚 recall 回归")
        self.assertEqual(rec["status"], "discharged")
        self.assertEqual(self.h.verdict.open_cases(), {})

    def test_judge_without_inspect_raises(self):
        with self.assertRaises(VerdictError):
            self.h.judge()

    def test_baseline_revision_affects_next_patrol(self):
        """基线修订走留痕，下一轮巡检按新标准裁。"""
        self.h.enroll("recall", 0.9)
        self.h.baseline.revise("recall", 0.6, reason="口径修正")
        self.assertTrue(self.h.inspect({"recall": 0.7})["passed"])

    def test_events_only_grow(self):
        """事件留痕只增不覆盖。"""
        n0 = len(self.h.events)
        self.h.enroll("recall", 0.9)
        self.h.guard({"acc": 1.0}, {"acc": 1.0})
        self.h.inspect({"recall": 0.9})
        self.h.judge()
        self.assertEqual(len(self.h.events), n0 + 4)

    def test_original_api_intact(self):
        """v1 原门面：describe/guard 行为不变。"""
        d = self.h.describe()
        self.assertEqual(d["cn"], "恒枢")
        ok = self.h.guard({"acc": 0.9}, {"acc": 0.95})
        self.assertTrue(ok["passed"])


if __name__ == "__main__":
    unittest.main()
