"""漂移裁决算子单测：退化开案在册，销账留痕，无案不销。"""
import unittest

from hengshu import Baseline, Patrol, Verdict, VerdictError


def make_report(findings):
    return {"passed": not findings, "findings": findings, "checked": 2}


class TestVerdict(unittest.TestCase):
    def setUp(self):
        self.v = Verdict()

    def test_passed_report_opens_no_case(self):
        verdict = self.v.judge(make_report([]))
        self.assertTrue(verdict["passed"])
        self.assertEqual(verdict["opened"], [])
        self.assertEqual(self.v.open_cases(), {})

    def test_regression_opens_case(self):
        finding = {"capability": "recall", "kind": "regression",
                   "baseline": 0.9, "observed": 0.7,
                   "metric": "gte", "baseline_version": 1}
        verdict = self.v.judge(make_report([finding]))
        self.assertFalse(verdict["passed"])
        self.assertEqual(len(verdict["opened"]), 1)
        case = self.v.open_cases()["recall"]
        self.assertEqual(case["status"], "open")
        self.assertEqual(case["case_no"], 1)

    def test_same_capability_not_duplicated(self):
        """同案不重开：在案能力再次漂移不另立新案。"""
        finding = {"capability": "recall", "kind": "regression",
                   "baseline": 0.9, "observed": 0.6,
                   "metric": "gte", "baseline_version": 1}
        self.v.judge(make_report([finding]))
        verdict = self.v.judge(make_report([dict(finding, observed=0.5)]))
        self.assertEqual(verdict["opened"], [])
        self.assertEqual(verdict["open_total"], 1)

    def test_discharge(self):
        finding = {"capability": "recall", "kind": "missing",
                   "baseline": 0.9, "observed": None,
                   "metric": "gte", "baseline_version": 1}
        self.v.judge(make_report([finding]))
        rec = self.v.discharge("recall", action="恢复 recall 采集桩", note="巡检缺桩误报")
        self.assertEqual(rec["status"], "discharged")
        self.assertNotIn("recall", self.v.open_cases())

    def test_discharge_requires_action(self):
        finding = {"capability": "recall", "kind": "missing",
                   "baseline": 0.9, "observed": None,
                   "metric": "gte", "baseline_version": 1}
        self.v.judge(make_report([finding]))
        with self.assertRaises(VerdictError):
            self.v.discharge("recall", action="")

    def test_discharge_without_case(self):
        with self.assertRaises(VerdictError):
            self.v.discharge("ghost", action="凭空销账")

    def test_records_chain(self):
        """判词与销账全程留痕，可回放。"""
        finding = {"capability": "recall", "kind": "regression",
                   "baseline": 0.9, "observed": 0.7,
                   "metric": "gte", "baseline_version": 1}
        self.v.judge(make_report([finding]))
        self.v.discharge("recall", action="修复")
        kinds = [r.get("action") or r.get("status") for r in self.v.records()]
        self.assertEqual(kinds, ["open", "judge", "discharged"])


if __name__ == "__main__":
    unittest.main()
