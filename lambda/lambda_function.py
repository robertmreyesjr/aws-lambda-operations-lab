import json
import os
from datetime import datetime, timezone

def lambda_handler(event, context):
    fail_mode = os.environ.get("FAIL_MODE", "false").lower() == "true"

    response = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "function_name": context.function_name,
        "request_id": context.aws_request_id,
        "received_event": event,
        "status": "success"
    }

    print("Lambda execution started")
    print(json.dumps(response))

    if fail_mode:
        print("FAIL_MODE is enabled - raising an exception for monitoring test")
        raise Exception("Intentional failure for CloudWatch alarm validation")

    print("Health check passed")
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }