"""恒枢 HENGSHU · VAL-03 防漂移：禁基础能力退化。

三算子：基线登记（Baseline）→ 漂移巡检（Patrol）→ 漂移裁决（Verdict）。
零第三方依赖，仅 Python 3.10+ 标准库。
"""

from .core import Hengshu, BaselineError, VerdictError
from .baseline import Baseline
from .patrol import Patrol
from .verdict import Verdict

__all__ = [
    "Hengshu",
    "Baseline",
    "Patrol",
    "Verdict",
    "BaselineError",
    "VerdictError",
]
__version__ = "0.1.0"
