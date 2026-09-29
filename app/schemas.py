from pydantic import BaseModel, Field
from typing import Literal


class AskRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=4000
    )


class EducationRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=200
    )
    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ]


class AIAnswer(BaseModel):
    answer: str
    key_points: list[str]
    confidence: float = Field(
        ge=0.0,
        le=1.0 
    )


class EducationalAnswer(BaseModel):

    topic: str
    explanation: str = Field(
        min_length=20
    )
    key_concepts: list[str] = Field(
        min_length=2,
        max_length=10
    )

    examples: list[str] = Field(
        min_length=1,
        max_length=5
    )


    difficulty: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ]

