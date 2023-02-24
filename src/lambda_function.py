from typing import Any


def lambda_handler(event: dict[str, Any], context: Any) -> int:
    print("Hello")
    return 200
