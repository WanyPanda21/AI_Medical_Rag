
import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from anthropic import Anthropic
from qdrant_client import QdrantClient, models
from boto3.dynamodb.conditions import Attr

# --------------------------------
# Configuration
# --------------------------------

TABLE_NAME = os.environ["MEDICAL_CASES_TABLE"]

QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]

COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION",
    "medical_knowledge"
)

CLAUDE_MODEL = os.getenv(
    "CLAUDE_MODEL",
    "claude-haiku-5-5"
)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

MAX_CONTEXT_DOCUMENTS = 5

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

anthropic = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    timeout=20.0
)

# --------------------------------
# API Response
# --------------------------------

def response(status_code, body):

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(body, default=str)
    }

# --------------------------------
# Request Body
# --------------------------------

def get_request_body(event):

    body = event.get("body")

    if not body:
        return {}

    if event.get("isBase64Encoded"):
        import base64
        body = base64.b64decode(body).decode("utf-8")

    return json.loads(body)

# --------------------------------
# Qdrant Retrieval
# --------------------------------

def retrieve_documents(question):

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        cloud_inference=True,
        timeout=15
    )

    try:

        result = client.query_points(
            collection_name=COLLECTION_NAME,

            query=models.Document(
                text=question,
                model=EMBEDDING_MODEL
            ),

            limit=MAX_CONTEXT_DOCUMENTS,
            with_payload=True
        )

        documents = []

        for point in result.points:

            payload = point.payload or {}

            documents.append({
                "content": payload.get("page_content", ""),
                "metadata": payload.get("metadata", {})
            })

        return documents

    finally:
        client.close()

# --------------------------------
# Claude Generation
# --------------------------------

def generate_answer(question, documents):

    if not documents:
        return (
            "I could not find relevant information in the "
            "available medical knowledge base."
        )

    context = ""

    for index, document in enumerate(documents, start=1):

        metadata = document.get("metadata", {})

        context += f"""
        SOURCE {index}
        Document: {metadata.get('source', 'Unknown')}
        Page: {metadata.get('page', 'Unknown')}

        Content:
        {document.get('content', '')}

        -----------------------
        """

    system_prompt = """
    You are a medical knowledge assistant.

    Rules:
    1. Answer using the provided medical context.
    2. Do not invent medical facts.
    3. Do not diagnose patients.
    4. Do not prescribe medicines or dosages.
    5. If the context is insufficient, clearly say so.
    6. Recommend consulting a qualified doctor.
    7. This answer must be reviewed by a doctor.
    """

    result = anthropic.messages.create(

        model=CLAUDE_MODEL,

        max_tokens=1500,

        system=system_prompt,

        messages=[
            {
                "role": "user",
                "content": f"""
                Patient question:
                {question}

                Retrieved medical context:
                {context}

                Generate an educational response.
                """
            }
        ]
    )

    return result.content[0].text

# --------------------------------
# Create Patient Case
# --------------------------------

def create_case(event):

    body = get_request_body(event)

    patient_id = body.get("patient_id")
    question = body.get("question") or body.get("query")

    if not patient_id or not question:
        return response(
            400,
            {"error": "patient_id and question are required"}
        )

    documents = retrieve_documents(question)

    answer = generate_answer(
        question,
        documents
    )

    case_id = str(uuid.uuid4())

    sources = []

    for document in documents:

        metadata = document.get("metadata", {})

        sources.append({
            "source": metadata.get("source", "Unknown"),
            "page": str(metadata.get("page", "Unknown"))
        })

    item = {
        "case_id": case_id,
        "patient_id": str(patient_id),
        "question": question,
        "answer": answer,
        "sources": sources,
        "status": "PENDING_DOCTOR_REVIEW",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    # Optional patient details
    if body.get("age") is not None:
        item["age"] = int(body["age"])

    if body.get("gender"):
        item["gender"] = str(body["gender"])

    table.put_item(Item=item)

    return response(
        201,
        {
            "message": "Case created successfully",
            "case_id": case_id,
            "status": item["status"],
            "answer": answer,
            "sources": sources
        }
    )

# --------------------------------
# Get Patient Case
# --------------------------------

def get_case(case_id):

    result = table.get_item(
        Key={"case_id": case_id}
    )

    item = result.get("Item")

    if not item:
        return response(
            404,
            {"error": "Case not found"}
        )

    return response(200, item)

# --------------------------------
# Doctor Pending Cases
# --------------------------------

def get_doctor_cases():

    result = table.scan(
        FilterExpression=Attr("status").eq(
            "PENDING_DOCTOR_REVIEW"
        ),
        Limit=100
    )

    return response(
        200,
        {
            "cases": result.get("Items", [])
        }
    )

# --------------------------------
# Doctor Review
# --------------------------------

def review_case(event, case_id):

    body = get_request_body(event)

    decision = str(
        body.get("decision", "")
    ).upper()

    doctor_id = body.get("doctor_id")
    comments = body.get("comments", "")

    if decision not in ["APPROVED", "REJECTED"]:
        return response(
            400,
            {
                "error": "decision must be APPROVED or REJECTED"
            }
        )

    if not doctor_id:
        return response(
            400,
            {"error": "doctor_id is required"}
        )

    existing = table.get_item(
        Key={"case_id": case_id}
    ).get("Item")

    if not existing:
        return response(
            404,
            {"error": "Case not found"}
        )

    if existing.get("status") != "PENDING_DOCTOR_REVIEW":
        return response(
            409,
            {"error": "This case has already been reviewed"}
        )

    table.update_item(

        Key={"case_id": case_id},

        UpdateExpression="""
            SET #status = :status,
                doctor_id = :doctor_id,
                doctor_comments = :comments,
                reviewed_at = :reviewed_at
        """,

        ExpressionAttributeNames={
            "#status": "status"
        },

        ExpressionAttributeValues={
            ":status": decision,
            ":doctor_id": str(doctor_id),
            ":comments": str(comments),
            ":reviewed_at": datetime.now(
                timezone.utc
            ).isoformat()
        },

        ConditionExpression=Attr("status").eq(
            "PENDING_DOCTOR_REVIEW"
        )
    )

    return response(
        200,
        {
            "message": "Doctor review completed",
            "case_id": case_id,
            "status": decision
        }
    )

# --------------------------------
# Lambda Entry Point
# --------------------------------

def handler(event, context):

    try:

        method = event.get(
            "httpMethod",
            ""
        )

        path = event.get(
            "path",
            ""
        )

        path_parameters = event.get(
            "pathParameters"
        ) or {}

        if method == "OPTIONS":
            return response(200, {"message": "OK"})

        # POST /cases

        if method == "POST" and path == "/cases":
            return create_case(event)

        # GET /cases/{case_id}

        if method == "GET" and path_parameters.get("case_id"):
            return get_case(
                path_parameters["case_id"]
            )

        # GET /doctor/cases

        if method == "GET" and path == "/doctor/cases":
            return get_doctor_cases()

        # POST /doctor/cases/{case_id}

        if (
            method == "POST"
            and path.startswith("/doctor/cases/")
            and path_parameters.get("case_id")
        ):
            return review_case(
                event,
                path_parameters["case_id"]
            )

        return response(
            404,
            {"error": "Route not found"}
        )

    except Exception as error:

        print("Lambda error:", str(error))

        return response(
            500,
            {"error": "Internal server error"}
        )