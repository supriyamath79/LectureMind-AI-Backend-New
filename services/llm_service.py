"""Question answering service."""

from core.config import settings
from core.logging import get_logger
from managers.lecture_manager import get_lecture_for_user
from services.ai_service import generate_completion
from services.retrieve_service import retrieve_chunks
from utils.responses import error_response, success_response

logger = get_logger(__name__)


def answer_question(lecture_id: int, question: str, user_id: int) -> dict:
    """Answer a question for one lecture using retrieved context."""

    lecture = get_lecture_for_user(lecture_id, user_id)

    if lecture is None:
        return error_response(
            "Lecture not found.",
            legacy={"message": "Lecture not found."},
        )

    retrieved = retrieve_chunks(
        question,
        lecture["embedding_path"],
        lecture["faiss_path"],
    )

    chunks = retrieved["chunks"]
    best_score = retrieved["best_score"]
    logger.info("Best similarity score: %.4f", best_score)

    if best_score < settings.answer_similarity_threshold:
        answer = "I could not find the answer in the lecture."
        return success_response(
            "Answer generated successfully.",
            data={"answer": answer},
            legacy={"answer": answer},
        )

    answer = generate_answer(question, chunks)
    return success_response(
        "Answer generated successfully.",
        data={"answer": answer},
        legacy={"answer": answer},
    )


def generate_answer(question, retrieved_chunks):
    """Generate an answer from the top retrieved chunks."""

    context = "\n\n".join(retrieved_chunks[:2])

    prompt = f"""
    You are LectureMind AI.

    You are a Retrieval-Augmented Generation (RAG) assistant.

    STRICT RULES:

    - Answer ONLY from the Lecture Context.
    - Never use your own knowledge.
    - Never guess.
    - Never add examples that are not present in the lecture.
    - Never explain concepts beyond the lecture.
    - If the answer is missing, reply exactly:
    "I could not find the answer in the lecture."
    - Give a complete answer if it exists.
    - Finish every sentence.
    - Use simple paragraphs.

    Lecture Context:
    {context}

    Question:
    {question}

    Answer:
    """

    return generate_completion(
        prompt,
        options={
            "temperature": 0,
            "num_predict": 512,
            "top_p": 0.9,
            "top_k": 40,
        },
    )
