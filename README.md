# AWS Lambda Operations Lab

## Project Overview
This project is an operations-focused AWS Lambda lab built to demonstrate serverless monitoring, logging, alerting, and troubleshooting. Instead of focusing only on architecture, this lab shows how to operate and validate a Lambda workload in a way that aligns with cloud support and cloud operations responsibilities.

The lab includes:
- A Python-based AWS Lambda function
- Scheduled execution using EventBridge Scheduler
- CloudWatch Logs for operational visibility
- CloudWatch Alarm for Lambda errors
- SNS email notifications for alerting
- Failure simulation using an environment variable
- Recovery validation after resolving the issue

---

## Objectives
By completing this lab, I was able to:

- Deploy and configure an AWS Lambda function
- Use IAM role-based permissions for Lambda execution
- Schedule recurring Lambda runs with EventBridge Scheduler
- Review Lambda logs in CloudWatch Logs
- Simulate a production-style failure condition
- Monitor Lambda Errors metrics in CloudWatch
- Trigger an SNS alert from a CloudWatch alarm
- Restore the function to a healthy state
- Apply basic cost-conscious operational practices such as log retention

---

## AWS Services Used
- AWS Lambda
- AWS IAM
- Amazon EventBridge Scheduler
- Amazon CloudWatch Logs
- Amazon CloudWatch Alarms
- Amazon SNS

---

## Architecture / Flow
1. EventBridge Scheduler invokes the Lambda function on a recurring schedule.
2. The Lambda function writes execution details to CloudWatch Logs.
3. In normal mode, the Lambda returns a success response.
4. In failure mode, the Lambda raises an exception.
5. Lambda Errors metrics are sent to CloudWatch.
6. A CloudWatch alarm monitors the Errors metric.
7. When the threshold is breached, CloudWatch sends a notification to SNS.
8. SNS sends an email alert.

---

## Lambda Function Behavior
The Lambda function uses an environment variable called `FAIL_MODE`.

- `FAIL_MODE=false`  
  The function runs successfully and logs a healthy execution.

- `FAIL_MODE=true`  
  The function intentionally throws an exception so monitoring and alerting can be validated.

This approach made it possible to test both normal operations and incident handling.

---

## Lambda Code
File location:

`lambda/lambda_function.py`

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
