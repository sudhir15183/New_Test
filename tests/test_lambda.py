import sys
import os
import boto3
import pytest
import csv
from moto import mock_dynamodb
from datetime import datetime, timezone

# Add lambda_app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lambda_app.lambda_function import lambda_handler

TABLE_NAME = "Users"

#Define the dynamodb mock fixture.
@pytest.fixture
def dynamodb_mock():
    with mock_dynamodb():
        # Setup mocked DynamoDB environment
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "email", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        yield dynamodb
        
#Test case Lambda success
def test_lambda_success(dynamodb_mock):
    event = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": "jan.kowalski@example.com"
    }

    response = lambda_handler(event, None)
    print("Response:", response)

    assert response["statusCode"] == 200
    assert response["body"] == "Data inserted and verified successfully."

    # Read the inserted item from DynamoDB
    table = dynamodb_mock.Table(TABLE_NAME)
    item = table.get_item(Key={"email": event["email"]}).get("Item")
    print("Inserted item:", item)

    # Write to CSV with timestamp
    if item:
        item["timestamp"] = datetime.now(timezone.utc).isoformat()
        output_file_path = os.path.abspath("output.csv")
        with open(output_file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=item.keys())
            writer.writeheader()
            writer.writerow(item)
        print(f"CSV written to: {output_file_path}")

    # Extra validation (optional redundancy, already in lambda)
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)
    result = table.get_item(Key={'email': event["email"]})
    assert 'Item' in result

def test_lambda_missing_email(dynamodb_mock):
    event = {
        "first_name": "Jan",
        "last_name": "Kowalski"
        # Missing 'email'
    }

    response = lambda_handler(event, None)
    print("Response:", response)

    assert response["statusCode"] == 400
    assert response["body"] == "Missing required fields."
