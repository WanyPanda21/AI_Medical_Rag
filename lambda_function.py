
import json
import logging
import os
import uuid

from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from src.generator import generate_answer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    os.environ["MEDICAL_REQUESTS_TABLE"]
)

def current_time():
    return datetime.now(timezone.utc).isoformat()

def api_response(status_code, data):

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "http://localhost:8501",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(data, default=str)
    }

def get_request(request_id):

    if not request_id:
        raise ValueError("request_id is required")

    result = table.get_item(
        Key={"request_id": request_id}
    )

    item = result.get("Item")

    if not item:
        raise ValueError("Request not found")

    return item

# --------------------------------------------------
# PATIENT QUERY
# POST /patient/query
# --------------------------------------------------

def patient_query(body):

    patient_id = body.get("patient_id")
    patient_info = body.get("patient_info", {})
    query = body.get("query")

    if not isinstance(patient_id, str) or not patient_id.strip():
        raise ValueError("patient_id is required")

    if not isinstance(patient_info, dict):
        raise ValueError("patient_info must be an object")

    if not isinstance(query, str) or not query.strip():
        raise ValueError("query is required")

    query = query.strip()

    request_id = str(uuid.uuid4())

    # RAG retrieval + Claude generation
    rag_result = generate_answer(
        query=query,
        top_k=5
    )

    ai_answer = rag_result.get("answer")

    sources = rag_result.get("sources", [])

    if not isinstance(ai_answer, str) or not ai_answer.strip():
        raise RuntimeError("AI response was empty")

    created_at = current_time()

    item = {
        "request_id": request_id,
        "patient_id": patient_id.strip(),
        "patient_info": patient_info,
        "patient_query": query,
        "ai_answer": ai_answer,
        "sources": sources,
        "doctor_review": {},
        "status": "PENDING_DOCTOR_REVIEW",
        "created_at": created_at,
        "updated_at": created_at
    }

    table.put_item(
        Item=item,
        ConditionExpression="attribute_not_exists(request_id)"
    )

    return {
        "request_id": request_id,
        "status": "PENDING_DOCTOR_REVIEW",
        "message": "Your request has been submitted for doctor review."
    }

# --------------------------------------------------
# PATIENT STATUS
# GET /patient/status/{request_id}
# --------------------------------------------------

def patient_status(request_id):

    item = get_request(request_id)

    return {
        "request_id": request_id,
        "status": item["status"],
        "created_at": item["created_at"]
    }

# --------------------------------------------------
# DOCTOR PENDING REQUESTS
# GET /doctor/pending
# --------------------------------------------------

def doctor_pending():

    requests = []

    scan_kwargs = {
        "FilterExpression": Attr("status").eq(
            "PENDING_DOCTOR_REVIEW"
        )
    }

    while True:

        result = table.scan(**scan_kwargs)

        for item in result.get("Items", []):

            requests.append({
                "request_id": item["request_id"],
                "patient_id": item["patient_id"],
                "patient_info": item["patient_info"],
                "patient_query": item["patient_query"],
                "ai_answer": item["ai_answer"],
                "sources": item["sources"],
                "status": item["status"],
                "created_at": item["created_at"]
            })

        last_key = result.get("LastEvaluatedKey")

        if not last_key:
            break

        scan_kwargs["ExclusiveStartKey"] = last_key

    return {
        "total_requests": len(requests),
        "requests": requests
    }

# --------------------------------------------------
# DOCTOR REVIEW
# POST /doctor/review/{request_id}
# --------------------------------------------------

def doctor_review(request_id, body):

    decision = body.get("decision")
    doctor_id = body.get("doctor_id")
    comments = body.get("review_comments")

    if decision not in ["APPROVED", "REJECTED"]:
        raise ValueError(
            "decision must be APPROVED or REJECTED"
        )

    if not isinstance(doctor_id, str) or not doctor_id.strip():
        raise ValueError("doctor_id is required")

    if not isinstance(comments, str) or not comments.strip():
        raise ValueError("Doctor review comments are required")

    reviewed_at = current_time()

    review_details = {
        "doctor_id": doctor_id.strip(),
        "decision": decision,
        "review_comments": comments.strip(),
        "reviewed_at": reviewed_at
    }

    try:

        result = table.update_item(
            Key={
                "request_id": request_id
            },

            UpdateExpression=(
                "SET #status = :decision, "
                "doctor_review = :review, "
                "updated_at = :updated"
            ),

            ConditionExpression=(
                "#status = :pending "
                "AND attribute_exists(request_id)"
            ),

            ExpressionAttributeNames={
                "#status": "status"
            },

            ExpressionAttributeValues={
                ":decision": decision,
                ":pending": "PENDING_DOCTOR_REVIEW",
                ":review": review_details,
                ":updated": reviewed_at
            },

            ReturnValues="ALL_NEW"
        )

        item = result["Attributes"]

        return {
            "request_id": request_id,
            "status": item["status"],
            "doctor_review": item["doctor_review"],
            "message": "Doctor review saved successfully."
        }

    except ClientError as error:

        error_code = error.response.get(
            "Error", {}
        ).get("Code")

        if error_code == "ConditionalCheckFailedException":

            raise ValueError(
                "Request not found or already reviewed"
            )

        raise

# --------------------------------------------------
# PATIENT APPROVED RESPONSE
# GET /patient/response/{request_id}
# --------------------------------------------------

def patient_response(request_id):

    item = get_request(request_id)

    status = item["status"]

    if status == "PENDING_DOCTOR_REVIEW":

        return {
            "request_id": request_id,
            "status": status,
            "message": "Your response is waiting for doctor approval."
        }

    if status == "REJECTED":

        return {
            "request_id": request_id,
            "status": status,
            "doctor_review": item["doctor_review"],
            "message": (
                "Your request was not approved. "
                "Please contact your healthcare provider."
            )
        }

    if status == "APPROVED":

        return {
            "request_id": request_id,
            "status": status,
            "ai_answer": item["ai_answer"],
            "sources": item["sources"],
            "doctor_review": item["doctor_review"]
        }

    raise ValueError("Unknown request status")

# --------------------------------------------------
# MAIN LAMBDA HANDLER
# --------------------------------------------------

def lambda_handler(event, context):

    try:

        route = event.get("routeKey", "")

        if route.startswith("OPTIONS "):

            return api_response(
                200,
                {"message": "OK"}
            )

        body = event.get("body")

        if isinstance(body, str):

            body = json.loads(body) if body else {}

        elif body is None:

            body = {}

        if not isinstance(body, dict):

            raise ValueError(
                "Request body must be a JSON object"
            )

        path_params = event.get("pathParameters") or {}

        if route == "POST /patient/query":

            result = patient_query(body)

            return api_response(201, result)

        elif route == "GET /patient/status/{request_id}":

            result = patient_status(
                path_params.get("request_id")
            )

            return api_response(200, result)

        elif route == "GET /doctor/pending":

            result = doctor_pending()

            return api_response(200, result)

        elif route == "POST /doctor/review/{request_id}":

            result = doctor_review(
                path_params.get("request_id"),
                body
            )

            return api_response(200, result)

        elif route == "GET /patient/response/{request_id}":

            result = patient_response(
                path_params.get("request_id")
            )

            return api_response(200, result)

        return api_response(
            404,
            {"message": "Route not found"}
        )

    except ValueError as error:

        return api_response(
            400,
            {"message": str(error)}
        )

    except Exception:

        logger.exception(
            "Lambda execution failed"
        )

        return api_response(
            500,
            {"message": "Internal server error"}
        )