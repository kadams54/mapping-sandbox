import json
from typing import Any

from jinja2 import Environment, PackageLoader


def mapper(input: dict[str, Any]) -> dict[str, Any]:
    """Normally the advice on using Jinja to generate JSON is: don't
    do it. Create a Python object and then dump it to JSON. The problem
    with that advice is that it assumes the desired JSON is a good
    representation of the underlying data model. When there's a high
    degree of mismatch between the data model and the JSON, you end up
    torturing the data to get it to fit the desired outcome. That's
    where Jinja comes back in: by decoupling the desired output from
    the data model, the mapping becomes much, much simpler again. Note
    this works because we're only outputing primitives in the template.

    Args:
        input (dict[str, Any]): employee info

    Returns:
        dict[str, Any]: employee info in output format
    """
    env = Environment(loader=PackageLoader("mapping_sandbox.jinja"))
    template = env.get_template("employee.json")
    return json.loads(template.render(**input))
    # LET'S GOOOOOOOOOOOO
