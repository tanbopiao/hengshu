"""恒枢端到端示例：登记→演化引入漂移→巡检→裁决→修复销账。

运行：python3 examples/demo_drift.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hengshu import Hengshu

h = Hengshu()

# 1) 基线登记：基础能力一旦具备，登记即立约
h.enroll("recall", 0.90, note="召回下限")
h.enroll("precision", 0.80, note="精度下限")
h.enroll("latency_ms", 200, metric="lte", note="延迟上限")
print("基线登记 3 项，版本", h.baseline.version())

# 2) 正常演化：全部达标
report = h.inspect({"recall": 0.93, "precision": 0.85, "latency_ms": 180})
print("第一轮巡检：", "通过" if report["passed"] else "发现漂移")

# 3) 某次重构引入漂移：recall 退化，且 latency 观测缺失
report = h.inspect({"recall": 0.72, "precision": 0.86})
print("第二轮巡检：", "通过" if report["passed"] else "发现漂移")
for f in report["findings"]:
    print(f"  漂移项 {f['capability']}：{f['kind']}，基线 {f['baseline']}，实测 {f['observed']}")

# 4) 漂移裁决：退化开案在册
verdict = h.judge()
print("裁决：开案", len(verdict["opened"]), "件，在案", verdict["open_total"], "件")

# 5) 修复后销账：凭证据结案，留痕可回放
h.discharge("recall", action="回滚引入漂移的重构", note="recall 恢复 0.93")
h.discharge("latency_ms", action="补齐 latency 观测桩", note="缺桩误报，观测恢复")
print("销账后：在案", len(h.verdict.open_cases()), "件；留痕", len(h.verdict.records()), "条")

sys.exit(0 if not h.verdict.open_cases() else 1)
