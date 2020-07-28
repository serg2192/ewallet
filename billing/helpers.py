import json
from functools import partial


json_dumps = partial(
    json.dumps,
    ensure_ascii=False
)
