import sys
from typing import Any, Callable

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

# =====================================================================
# The initial skeleton for the output data, provided for your
# convenience. `base_output` should not be changed, so you'll need to
# create a copy. Python's copy.deepcopy() should be helpful for that.
# =====================================================================
base_employee: dict[str, Any] = {
    "type": "namespace/employee",
    "attributes": {
        "ids": [{"value": {"type": [{"value": "hr_id"}]}}],
        "config_flag": [{"value": False}],
    },
    "metadata": [{"type": "namespace/source/name"}],
}

Mappable: TypeAlias = Callable[[dict[str, Any]], dict[str, Any]]
