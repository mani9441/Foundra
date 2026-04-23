# ============================================================
# File: phase2_validation/utils/test_json_parser.py
# ============================================================

from pprint import pprint
from utils.json_parser import extract_json


samples = [
    '{"decision":"PROCEED","score":91}',

    """
    ```json
    {
      "decision":"PIVOT",
      "score":72
    }
    ```
    """,

    """
    Here is your result:

    {
      "decision":"REJECT",
      "score":25
    }

    Thank you.
    """,

    """
    {
      "decision":"PROCEED",
      "score":88,
    }
    """,

    "Not JSON output"
]

for i, sample in enumerate(samples, 1):
    print(f"\n===== TEST {i} =====")
    pprint(extract_json(sample))