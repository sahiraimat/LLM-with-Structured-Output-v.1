from app.llm import generate_structured_response
from app.schemas import (
    AskRequest, 
    AIAnswer, 
    EducationalAnswer, 
    EducationRequest,
    RAGRequest,
    RAGResponse,
    RAGSource
)


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import GEMINI_MODEL

import logging
import time
import uuid

from app.document_loader import load_knowledge_base
from app.retriever import search
from app.llm import generate_rag_response

from app.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


load_knowledge_base(
    "data/knowledge.txt"
)



app = FastAPI(
    title='Agentic AI API',
    version='0.1.0'
)




@app.middleware('http')
async def request_logging_middleware(
    request: Request,
    call_next
):

    request_id = str(uuid.uuid4())

    start_time = time.perf_counter()
    request.state.request_id = request_id

    logger.info(
        "request_started "
        "request_id=%s method=%s path=%s",
        request_id,
        request.method,
        request.url.path

    )

    try:

        response = await call_next(request)
        duration = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request_completed "
            "request_id=%s status=%s duration=%.3fs",
            request_id,
            response.status_code,
            duration
        ) 

        return response

    except Exception:

        duration= time.perf_counter() - start_time

        logger.info(
            "request_failed "
            "request_id=%s duration=%.3fs",
            request_id,
            duration

        )

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error.",
                "request_id": request_id
            }
        )

    


@app.get("/health")
def health():

    return {
        "status": "ok",
        "model": GEMINI_MODEL
    }


# @app.post(
#     "/ask",
#     response_model=EducationalAnswer
#     )
# def ask(request: AskRequest):

#     result = generate_structured_response(
#         request.prompt
#     )

#     return result

@app.post(
    "/educate",
    response_model=EducationalAnswer
)
def educate(request: EducationRequest):

    result = generate_structured_response(
        topic=request.topic,
        level=request.level
    )
    return result



@app.post(
    "/ask-rag",
    response_model=RAGResponse
)
def ask_rag(request: RAGRequest):

    results = search(
        request.question,
        top_k=3,
        min_score=0.60
    )

    if not results:
        return RAGResponse(
            answer = (
                "I could not find relavant information "
                "in the knowledge base."
            ),
            sources= []
        )

    context_parts = []

    for result in results:
        metadata = result["metadata"]
        context_parts.append(
            f"""
            SOURCE: {metadata["source"]}
            DOCUMENT_ID: {metadata["document_id"]}
            CHUNK: {metadata["chunk_id"]}
            SECTION: {metadata.get("section")}

            CONTENT: {result["text"]}

        """
        )



    context = "\n\n".join(
        context_parts
    )

    answer = generate_rag_response(
        question=request.question,
        context=context
    )


    return RAGResponse(
        answer=answer,
        sources=[
            RAGSource(
            
                document_id= result["metadata"]["document_id"],
                source= result['metadata']['source'],
                chunk_id= result["metadata"]["chunk_id"],
                score= result["score"],
                section= result["metadata"].get("section")

            )
            for result in results
        ]
    )