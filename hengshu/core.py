"""恒枢（HENGSHU）· VAL-03 防漂移：禁基础能力退化。典出《周易·恒卦》「恒，久也」——守恒之枢机

道统出处：元极恒一·术语缩影表 T059 ｜ 第六批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：VAL-03 防漂移：禁基础能力退化。典出《周易·恒卦》「恒，久也」——守恒之枢机。

边界：本件为算子 v1——骨架桩已按命名映射补齐实现；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。

v0.1 生长（命名即种子）：恒者久也，枢者机也——恒定之枢机，守基不失。
逻辑本体：基础能力一旦具备即入基线锁，任何演化不得使其退化；
退化必须留痕、可裁决、可销账。架构三算子：
基线登记（Baseline）→ 漂移巡检（Patrol）→ 漂移裁决（Verdict）。
本类为恒枢之中枢：三算子在此合枢，原 guard 门面原样保留。
"""

from .baseline import Baseline, BaselineError
from .patrol import Patrol
from .verdict import Verdict, VerdictError

__all__ = ["Hengshu", "Baseline", "Patrol", "Verdict",
           "BaselineError", "VerdictError"]


class Hengshu:
    """恒枢（HENGSHU）算子 v1 → v0.1 中枢门面。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "HENGSHU"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕
        # v0.1：三算子合枢——枢者，众脉所会也
        self.baseline = Baseline()
        self.patrol = Patrol(self.baseline)
        self.verdict = Verdict()

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

    # ---- v0.1 新增：三算子门面（只增不覆盖） ----

    def enroll(self, capability, threshold, metric="gte", note=""):
        """登记基础能力入基线：登记即立约。"""
        record = self.baseline.register(capability, threshold, metric, note)
        self.events.append({"event": "enroll", "capability": capability})
        return record

    def inspect(self, observed):
        """漂移巡检：逐项对照基线，缺项即漂移，不达即退化。"""
        report = self.patrol.inspect(observed)
        self.events.append({"event": "inspect", "passed": report["passed"]})
        self._last_report = report
        return report

    def judge(self, report=None):
        """漂移裁决：退化开案在册，达标备案。缺省裁最近一轮巡检。"""
        if report is None:
            report = getattr(self, "_last_report", None)
            if report is None:
                raise VerdictError("尚无巡检单可裁：先 inspect 再 judge")
        verdict = self.verdict.judge(report)
        self.events.append({"event": "judge", "passed": verdict["passed"]})
        return verdict

    def discharge(self, capability, action, note=""):
        """销账：修复凭证据结案，留痕后闭案。"""
        record = self.verdict.discharge(capability, action, note)
        self.events.append({"event": "discharge", "capability": capability})
        return record
