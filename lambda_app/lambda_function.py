
import boto3
import os

TABLE_NAME = "Users"

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)

    # Extract data from event
    first_name = event.get("first_name")
    last_name = event.get("last_name")
    email = event.get("email")

    # Validate required fields
    if not all([first_name, last_name, email]):
        return {
            "statusCode": 400,
            "body": "Missing required fields."
        }

    # Construct item
    item = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    # Insert into DynamoDB
    table.put_item(Item=item)

    # OPTIONAL: Confirm it was inserted
    result = table.get_item(Key={"email": email})
    if "Item" not in result:
        return {
            "statusCode": 500,
            "body": "Data insertion failed verification."
        }

    # Success response
    return {
        "statusCode": 200,
        "body": "Data inserted and verified successfully."
    }
