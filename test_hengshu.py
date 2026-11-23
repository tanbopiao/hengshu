"""恒枢（HENGSHU）算子单测：名帖完整、行为达标、只增不覆盖。"""
import unittest

from hengshu import Hengshu


class TestHengshu(unittest.TestCase):
    def setUp(self):
        self.op = Hengshu()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "hengshu")
        self.assertEqual(d["code"], "HENGSHU")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_guard(self):
        ok = self.op.guard({"acc": 0.9}, {"acc": 0.95})
        self.assertTrue(ok["passed"])
        bad = self.op.guard({"acc": 0.9}, {"acc": 0.8})
        self.assertFalse(bad["passed"])
        self.assertEqual(bad["regressions"][0]["metric"], "acc")


if __name__ == "__main__":
    unittest.main()
