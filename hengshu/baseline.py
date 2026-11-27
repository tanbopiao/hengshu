"""基线登记：能力清单＋判定标准，登记即立约，修订留痕。

恒枢第一算子。凡系统已具备的基础能力，登记入册即为基线；
基线只增不覆盖：同名重复登记拒绝，修订走 revise 留新版本，
旧标准永不丢失，任何一次放宽都有据可查。
"""

_DIRECTION = ("gte", "lte")  # gte=不低于（能力下限）；lte=不高于（开销上限）


class BaselineError(Exception):
    """基线登记违规。"""


class Baseline:
    """基线登记册：登记即立约，约成不静改。"""

    def __init__(self):
        self._items = {}    # capability -> record（当前有效版本）
        self._history = []  # 登记与修订留痕，只追加
        self._version = 0

    def register(self, capability, threshold, metric="gte", note=""):
        """登记一项基础能力及其判定标准。同名重复登记即拒。"""
        if metric not in _DIRECTION:
            raise BaselineError(f"未知判定方向：{metric}（可用：{'/'.join(_DIRECTION)}）")
        if capability in self._items:
            raise BaselineError(
                f"能力已登记，基线只增不覆盖：{capability}（修订走 revise）"
            )
        self._version += 1
        record = {
            "capability": capability,
            "threshold": threshold,
            "metric": metric,
            "note": note,
            "version": self._version,
            "status": "active",
        }
        self._items[capability] = dict(record)
        self._history.append({"action": "register", **record})
        return dict(record)

    def revise(self, capability, threshold, reason):
        """修订判定标准：旧值留痕，版本递增，无理由不修订。"""
        if capability not in self._items:
            raise BaselineError(f"能力未登记，无可修订：{capability}")
        if not reason:
            raise BaselineError("修订必须附理由，无理由不修订")
        old = self._items[capability]
        self._version += 1
        record = dict(old, threshold=threshold, version=self._version)
        self._items[capability] = record
        self._history.append(
            {"action": "revise", "reason": reason,
             "old_threshold": old["threshold"], **record}
        )
        return dict(record)

    def items(self):
        """当前有效基线：能力 -> 判定标准（副本，防外改）。"""
        return {cap: dict(rec) for cap, rec in self._items.items()}

    def history(self):
        """登记与修订全量留痕（副本）。"""
        return [dict(h) for h in self._history]

    def version(self):
        """基线册当前版本号。"""
        return self._version
