import json
import logging
import os
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from backend.medical_rag.src.generator import generate_answer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_dynamodb = boto3.resource("dynamodb")
_table = _dynamodb.Table(os.environ["MEDICAL_REQUESTS_TABLE"])


def _now():
    return datetime.now(timezone.utc).isoformat()


def _response(code, data):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": os.getenv("CORS_ALLOW_ORIGIN", "*"),
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        },
        "body": json.dumps(data, default=str),
    }


def _get_request(request_id):
    if not request_id:
        raise ValueError("request_id is required")
    item = _table.get_item(Key={"request_id": request_id}).get("Item")
    if not item:
        raise ValueError("Request not found")
    return item


def _patient_query(body):
    patient_id = body.get("patient_id")
    patient_info = body.get("patient_info", {})
    query = body.get("query")

    if not isinstance(patient_id, str) or not patient_id.strip():
        raise ValueError("patient_id is required")
    if not isinstance(patient_info, dict):
        raise ValueError("patient_info must be an object")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query is required")

    rag = generate_answer(query=query.strip(), top_k=5)
    answer = rag.get("answer")
    sources = rag.get("sources", [])
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("AI response was empty")

    request_id = str(uuid.uuid4())
    timestamp = _now()
    item = {
        "request_id": request_id,
        "patient_id": patient_id.strip(),
        "patient_info": patient_info,
        "patient_query": query.strip(),
        "ai_answer": answer,
        "sources": sources,
        "doctor_review": {},
        "status": "PENDING_DOCTOR_REVIEW",
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    _table.put_item(Item=item, ConditionExpression="attribute_not_exists(request_id)")
    return {
        "request_id": request_id,
        "status": item["status"],
        "message": "Your request has been submitted for doctor review.",
    }


def _patient_status(request_id):
    item = _get_request(request_id)
    return {"request_id": request_id, "status": item["status"], "created_at": item["created_at"]}


def _doctor_pending():
    items = []
    kwargs = {"FilterExpression": Attr("status").eq("PENDING_DOCTOR_REVIEW")}
    while True:
        page = _table.scan(**kwargs)
        for item in page.get("Items", []):
            items.append({
                "request_id": item["request_id"],
                "patient_id": item["patient_id"],
                "patient_info": item.get("patient_info", {}),
                "patient_query": item["patient_query"],
                "ai_answer": item["ai_answer"],
                "sources": item.get("sources", []),
                "status": item["status"],
                "created_at": item["created_at"],
            })
        key = page.get("LastEvaluatedKey")
        if not key:
            break
        kwargs["ExclusiveStartKey"] = key
    return {"total_requests": len(items), "requests": items}


def _doctor_review(request_id, body):
    decision = body.get("decision")
    doctor_id = body.get("doctor_id")
    comments = body.get("review_comments")
    if decision not in ("APPROVED", "REJECTED"):
        raise ValueError("decision must be APPROVED or REJECTED")
    if not isinstance(doctor_id, str) or not doctor_id.strip():
        raise ValueError("doctor_id is required")
    if not isinstance(comments, str) or not comments.strip():
        raise ValueError("Doctor review comments are required")

    reviewed_at = _now()
    review = {
        "doctor_id": doctor_id.strip(),
        "decision": decision,
        "review_comments": comments.strip(),
        "reviewed_at": reviewed_at,
    }
    try:
        result = _table.update_item(
            Key={"request_id": request_id},
            UpdateExpression="SET #status = :decision, doctor_review = :review, updated_at = :updated",
            ConditionExpression="#status = :pending AND attribute_exists(request_id)",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":decision": decision,
                ":pending": "PENDING_DOCTOR_REVIEW",
                ":review": review,
                ":updated": reviewed_at,
            },
            ReturnValues="ALL_NEW",
        )
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            raise ValueError("Request not found or already reviewed") from exc
        raise
    item = result["Attributes"]
    return {
        "request_id": request_id,
        "status": item["status"],
        "doctor_review": item["doctor_review"],
        "message": "Doctor review saved successfully.",
    }


def _patient_response(request_id):
    item = _get_request(request_id)
    status = item["status"]
    if status == "PENDING_DOCTOR_REVIEW":
        return {"request_id": request_id, "status": status, "message": "Your response is waiting for doctor approval."}
    if status == "REJECTED":
        return {
            "request_id": request_id,
            "status": status,
            "doctor_review": item.get("doctor_review", {}),
            "message": "Your request was not approved. Please contact your healthcare provider.",
        }
    if status == "APPROVED":
        return {
            "request_id": request_id,
            "status": status,
            "ai_answer": item["ai_answer"],
            "sources": item.get("sources", []),
            "doctor_review": item.get("doctor_review", {}),
        }
    raise ValueError("Unknown request status")


def lambda_handler(event, context):
    """Works with SAM AWS::Serverless::Api (REST API) event shape."""
    try:
        method = (event.get("httpMethod") or "").upper()
        path = event.get("path") or ""
        params = event.get("pathParameters") or {}

        if method == "OPTIONS":
            return _response(200, {"message": "OK"})

        raw_body = event.get("body")
        if isinstance(raw_body, str):
            body = json.loads(raw_body) if raw_body else {}
        elif raw_body is None:
            body = {}
        else:
            body = raw_body
        if not isinstance(body, dict):
            raise ValueError("Request body must be a JSON object")

        if method == "POST" and path == "/patient/query":
            return _response(201, _patient_query(body))
        if method == "GET" and path.startswith("/patient/status/"):
            return _response(200, _patient_status(params.get("request_id")))
        if method == "GET" and path == "/doctor/pending":
            return _response(200, _doctor_pending())
        if method == "POST" and path.startswith("/doctor/review/"):
            return _response(200, _doctor_review(params.get("request_id"), body))
        if method == "GET" and path.startswith("/patient/response/"):
            return _response(200, _patient_response(params.get("request_id")))
        return _response(404, {"message": "Route not found"})
    except (ValueError, json.JSONDecodeError) as exc:
        return _response(400, {"message": str(exc)})
    except Exception:
        logger.exception("Lambda execution failed")
        return _response(500, {"message": "Internal server error"})
