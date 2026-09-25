"""SnapLink - redirect function.

Triggered by: GET /{code}  (API Gateway HTTP API)
Returns:      302 redirect to the original URL, or 404 if the code is unknown.

One UpdateItem call both increments the click counter and returns the item,
so each redirect costs a single database operation.
"""
import os

import boto3
from botocore.exceptions import ClientError

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def not_found():
    return {
        "statusCode": 404,
        "headers": {"Content-Type": "text/plain"},
        "body": "Sorry, this short link does not exist.",
    }


def lambda_handler(event, context):
    # 1. Get the code from the path, e.g. /aB3xK9q -> "aB3xK9q"
    code = (event.get("pathParameters") or {}).get("code", "")
    if not code.isalnum() or len(code) > 20:
        return not_found()

    # 2. Add 1 to clicks AND read the original URL in one call.
    #    The condition stops unknown codes from creating empty items.
    try:
        result = table.update_item(
            Key={"short_code": code},
            UpdateExpression="ADD clicks :one",
            ConditionExpression="attribute_exists(short_code)",
            ExpressionAttributeValues={":one": 1},
            ReturnValues="ALL_NEW",
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return not_found()
        raise

    # 3. 302 (temporary) so browsers don't cache it and every click is counted
    return {
        "statusCode": 302,
        "headers": {
            "Location": result["Attributes"]["long_url"],
            "Cache-Control": "no-store",
        },
    }
