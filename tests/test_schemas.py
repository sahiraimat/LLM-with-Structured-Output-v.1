import pytest

from app.schemas import EducationalAnswer


def test_valid_answer():

    result = EducationalAnswer(
        topic="Supervised Learning",
        explanation=(
            "Supervised learning learns from labelled "
            "training examples."
        ),
        key_concepts=[
            "Features",
            "Labels"
        ],
        examples=[
            "Spam detection"
        ],
        difficulty="beginner"
    )

    assert result.topic == "Supervised Learning"
    assert result.difficulty == "beginner"


def test_invalid_difficulty():

    with pytest.raises(ValueError):

        EducationalAnswer(
            topic="Python",
            explanation="Python is a programming language.",
            key_concepts=[
                "Variables",
                "Functions"
            ],
            examples=[
                "Web development"
            ],
            difficulty="expert"
        )