# hengshu
恒枢·VAL-03 防漂移：禁基础能力退化。典 | HENGSHU · ZONGYUAN-ROOT Daotong Component

## 命名映射（命名即种子）

**恒枢**——典出《周易·恒卦》「恒，久也」；枢者，户枢也、中枢也。
恒者，守基不失；枢者，众脉所会。合而言之：**恒定之枢机，为系统的基础能力立基线锁**。

- **逻辑本体**：基础能力一旦具备即入基线；任何演化不得使其退化；退化必须留痕、可裁决、可销账。
- **架构**：基线登记（Baseline）→ 漂移巡检（Patrol）→ 漂移裁决（Verdict），三算子合于恒枢（Hengshu）一门面。
- **算子**：`register / revise / items`（登记即立约，修订留痕）；`inspect`（逐项对照，缺项即漂移）；`judge / discharge / records`（退化开案，凭证据销账，判词全程留痕）。

## 架构

```
Baseline 基线登记册          Patrol 漂移巡检官           Verdict 漂移裁决官
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ register 登记即立约 │   │ inspect 逐项对照    │   │ judge   退化开案    │
│ revise  修订留痕    │──▶│ · 不达即退化       │──▶│ discharge 凭据销账  │
│ items   当前基线    │   │ · 缺项即漂移       │   │ records 判词留痕    │
└──────────────────┘   └──────────────────┘   └──────────────────┘
                 合枢于 Hengshu 门面（enroll / inspect / judge / discharge）
```

三条铁律：
1. **基线只增不覆盖**——同名重复登记即拒，修订走 `revise` 留新版本，旧标准永不丢失。
2. **缺项即漂移**——登记在册的能力观测缺失视同退化，能力消失与能力变差同罪。
3. **无案不销、空口不销**——销账必须附修复动作，判词与销账全程留痕。

## Install

零第三方依赖，仅 Python 3.10+ 标准库。

```bash
git clone https://github.com/tanbopiao/hengshu.git
cd hengshu
python3 -m unittest discover -s tests -v   # 运行测试套件
python3 examples/demo_drift.py             # 端到端示例
```

## Usage

```python
from hengshu import Hengshu

h = Hengshu()

# 基线登记：能力名 + 判定标准（gte=下限，lte=上限）
h.enroll("recall", 0.90)
h.enroll("latency_ms", 200, metric="lte")

# 漂移巡检：逐项对照，缺项即漂移，不达即退化
report = h.inspect({"recall": 0.72, "precision": 0.86})  # latency 缺失→漂移
print(report["passed"])   # False
print(report["findings"]) # 漂移清单，附基线值、实测值、所依基线版本

# 漂移裁决：退化开案在册
verdict = h.judge()
print(verdict["opened"])  # 开案清单

# 修复销账：凭证据结案，留痕可回放
h.discharge("recall", action="回滚引入漂移的重构")
```

v1 门面原样保留：`describe()`（名帖）与 `guard(baseline, candidate)`（度量字典回归拦截）行为不变。

## 自测方法

```bash
python3 -m unittest discover -s tests -v
```

覆盖：基线登记（重复即拒、修订留痕）、漂移巡检（缺项即漂移、lte 方向）、
漂移裁决（开案、销账、无案不销）、中枢门面（三算子合枢、v1 门面不回归）。

## License

MIT
