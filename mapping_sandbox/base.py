from typing import Any

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
