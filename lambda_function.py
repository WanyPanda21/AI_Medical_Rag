import json
from src.generator import generate_answer


def lambda_handler(event, context):

    try:
        body = json.loads(event.get("body") or "{}")

        query = body.get("query", "").strip()

        if not query:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Question cannot be empty"
                })
            }

        result = generate_answer(query)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(result)
        }

    except Exception as e:

        print(f"Error: {str(e)}")

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Internal server error"
            })
        }