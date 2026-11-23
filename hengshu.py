"""恒枢（HENGSHU）· VAL-03 防漂移：禁基础能力退化。典出《周易·恒卦》「恒，久也」——守恒之枢机

道统出处：元极恒一·术语缩影表 T059 ｜ 第六批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：VAL-03 防漂移：禁基础能力退化。典出《周易·恒卦》「恒，久也」——守恒之枢机。

边界：本件为算子 v1——骨架桩已按命名映射补齐实现；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class Hengshu:
    """恒枢（HENGSHU）算子 v1。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "HENGSHU"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕

    def describe(self):
        """构件名帖：名、代号、职责、铭文、体系锚。"""
        return {
            "repo": "hengshu",
            "cn": "恒枢",
            "code": self.CODE,
            "duty": "VAL-03 防漂移：禁基础能力退化。典出《周易·恒卦》「恒，久也」——守恒之枢机",
            "mingwen": "恒守其基，枢而不失",
            "anchor": self.ANCHOR,
        }

    def guard(self, baseline, candidate):
        """恒守其基：候选对基线回归，退化即拦。"""
        regressions = []
        for k, v in baseline.items():
            if k in candidate and candidate[k] < v:
                regressions.append({"metric": k, "baseline": v, "candidate": candidate[k]})
        verdict = {"passed": not regressions, "regressions": regressions}
        self.events.append({"event": "guard", "passed": verdict["passed"]})
        return verdict
