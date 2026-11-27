"""漂移巡检：对当前观测逐项对照基线，缺项即漂移。

恒枢第二算子。巡检只认基线，不认口头承诺：
登记在册的能力，观测缺失视同漂移——能力消失也是退化；
实测不达判定标准视同退化。每轮巡检留痕，可回放。
"""


class Patrol:
    """漂移巡检官：逐项对照，缺项即漂移，不达即退化。"""

    def __init__(self, baseline):
        self._baseline = baseline
        self._rounds = []  # 巡检留痕，只追加

    def inspect(self, observed):
        """对当前观测逐项巡检，产出巡检单。

        observed: {capability: 实测值}——只报观测，不报解释。
        返回巡检单：passed / findings / checked。
        """
        findings = []
        items = self._baseline.items()
        for cap, rec in items.items():
            threshold, metric = rec["threshold"], rec["metric"]
            if cap not in observed:
                findings.append({
                    "capability": cap,
                    "kind": "missing",
                    "baseline": threshold,
                    "observed": None,
                    "metric": metric,
                    "baseline_version": rec["version"],
                })
                continue
            value = observed[cap]
            ok = value >= threshold if metric == "gte" else value <= threshold
            if not ok:
                findings.append({
                    "capability": cap,
                    "kind": "regression",
                    "baseline": threshold,
                    "observed": value,
                    "metric": metric,
                    "baseline_version": rec["version"],
                })
        report = {
            "passed": not findings,
            "findings": findings,
            "checked": len(items),
        }
        self._rounds.append(dict(report, findings=[dict(f) for f in findings]))
        return report

    def rounds(self):
        """历轮巡检留痕（副本）。"""
        return [dict(r, findings=[dict(f) for f in r["findings"]])
                for r in self._rounds]
