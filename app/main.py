from app.llm import generate_structured_response
from app.schemas import (
    AskRequest, 
    AIAnswer, 
    EducationalAnswer, 
    EducationRequest
)


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import GEMINI_MODEL

import logging
import time
import uuid

from app.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)



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