# 🔪 Hands-On Task: Automating Tests for AWS Lambda Function Writing to DynamoDB

## 🌟 Goal

Implement automated tests (Python + `pytest`) for an AWS Lambda function that stores user data in a DynamoDB table.

---

## 🛡️ Scenario

You have a simple AWS Lambda function (written in Python) that receives user data (e.g., first name, last name, email) and writes it to a DynamoDB table.

### Sample JSON event:
```json
{
  "first_name": "Jan",
  "last_name": "Kowalski",
  "email": "jan.kowalski@example.com"
}
```

---

## ✅ Tasks

### 1. Set up the testing environment (if not already provided):
- A DynamoDB table named `Users` (partition key: `email`)
- A Python-based Lambda function that writes incoming data to the table
- Proper IAM role for the Lambda function with `PutItem` permissions for the DynamoDB table

### 2. Implement automated tests:
- Use the `pytest` framework
- Use `boto3` within tests to interact with AWS and verify that the data was saved
- Tests should:
  - Trigger the Lambda function with valid input
  - Verify that the user record was inserted into DynamoDB
  - Cover negative cases, e.g., missing `email` field → expect validation error or Lambda failure

### 3. (Optional – More Advanced):
- Use AWS mocking library (like `moto`) to run tests locally without deploying to AWS
- Set up CI/CD (e.g., GitHub Actions) to run tests on push

---

## 🧰 Technologies

- Python 3.8+
- `pytest`
- `boto3`
- AWS CLI or `sam` / `serverless` framework (for deployment, if needed)
- (Optional) `moto` for AWS service mocking

---

## 📁 Suggested Project Structure

```
lambda_app/
├── lambda_function.py
tests/
├── test_lambda.py
requirements.txt
README.md
```


