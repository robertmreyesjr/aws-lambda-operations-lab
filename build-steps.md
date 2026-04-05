
---

## build-steps.md

```markdown
# AWS Lambda Operations Lab - Build Steps

## Goal
Build an operations-focused AWS Lambda project that demonstrates:
- Scheduled execution
- Logging
- Error monitoring
- Alerting
- Incident simulation
- Recovery validation

---

## Environment Notes
- AWS Region used: `________________`
- Lambda function name: `lambda-ops-healthcheck`
- SNS topic name: `lambda-ops-alerts`
- Alarm name: `lambda-ops-healthcheck-errors`
- Schedule name: `lambda-ops-every-5-min`

---

## Part 1 - Create the Lambda Function
1. Sign in to the AWS Management Console.
2. Navigate to **Lambda**.
3. Click **Create function**.
4. Select **Author from scratch**.
5. Configure:
   - Function name: `lambda-ops-healthcheck`
   - Runtime: `Python 3.x`
   - Architecture: default
6. Under permissions, choose **Create a new role with basic Lambda permissions**.
7. Click **Create function**.

### Screenshot
**File:** `01-lambda-function-created.png`  
Capture:
- Function name
- Runtime
- Execution role
- Region if visible

---

## Part 2 - Deploy the Lambda Code
1. In the code editor, replace the default code with the following:

```python
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