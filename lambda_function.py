
import json
import logging

from src.generator import generate_answer

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    try:
        body = event.get("body", event)

        if isinstance(body, str):
            body = json.loads(body)

        if not isinstance(body, dict):
            return response(400, {
                "success": False,
                "error": "Invalid request"
            })

        question = body.get("question", "")

        if not isinstance(question, str) or not question.strip():
            return response(400, {
                "success": False,
                "error": "Please enter a valid question"
            })

        logger.info("Starting RAG retrieval and generation")

        result = generate_answer(
            query=question.strip(),
            top_k=5
        )

        return response(200, {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"]
        })

    except Exception:
        logger.exception("RAG processing failed")

        return response(500, {
            "success": False,
            "error": "Unable to process your question"
        })


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
