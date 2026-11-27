"""漂移裁决：退化即报、修复可销账、判词留痕。

恒枢第三算子。巡检发现退化即开案在册，案不销不闭；
修复凭证据销账，判词与销账全程留痕，篡改无处遁形。
"""


class VerdictError(Exception):
    """裁决违规。"""


class Verdict:
    """漂移裁决官：开案在册，销账留痕。"""

    def __init__(self):
        self._open = {}     # capability -> 在案退化
        self._records = []  # 判词与销账全量留痕，只追加

    def judge(self, report):
        """对巡检单作判：退化开案，达标备案。"""
        opened = []
        for finding in report["findings"]:
            cap = finding["capability"]
            if cap not in self._open:
                case_no = len(self._records) + 1
                case = {
                    "case_no": case_no,
                    "capability": cap,
                    "kind": finding["kind"],
                    "baseline": finding["baseline"],
                    "observed": finding["observed"],
                    "baseline_version": finding["baseline_version"],
                    "status": "open",
                }
                self._open[cap] = case
                self._records.append(dict(case))
                opened.append(dict(case))
        verdict = {
            "passed": report["passed"],
            "opened": opened,
            "open_total": len(self._open),
        }
        self._records.append({"action": "judge", **verdict})
        return verdict

    def open_cases(self):
        """在案退化清单（副本）。"""
        return {cap: dict(case) for cap, case in self._open.items()}

    def discharge(self, capability, action, note=""):
        """销账：修复凭证据结案，留痕后闭案。无在案不可销。"""
        if capability not in self._open:
            raise VerdictError(f"无在案退化，无可销账：{capability}")
        if not action:
            raise VerdictError("销账必须附修复动作，空口不销账")
        case = self._open.pop(capability)
        record = dict(case, status="discharged", repair=action, note=note)
        self._records.append(record)
        return dict(record)

    def records(self):
        """判词与销账全量留痕（副本）。"""
        return [dict(r) for r in self._records]
