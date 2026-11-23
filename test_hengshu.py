"""恒枢（HENGSHU）算子骨架单测：名帖完整、桩位齐整、只增不覆盖。"""
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

    def test_guard_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.guard(None, None)


if __name__ == "__main__":
    unittest.main()
