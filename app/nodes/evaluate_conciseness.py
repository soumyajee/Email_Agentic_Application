import re
from app.schemas import GraphState


def evaluate_conciseness_node(state: GraphState) -> GraphState:
    body = state["generated_email"]["body"].strip()
    words = body.split()
    word_count = len(words)

    sentences = [s.strip() for s in re.split(r"[.!?]+", body) if s.strip()]
    avg_sentence_length = (
        sum(len(sentence.split()) for sentence in sentences) / len(sentences)
        if sentences else 0.0
    )
    paragraph_count = len([p for p in body.split("\n\n") if p.strip()])

    score = 1.0

    if word_count < 60 or word_count > 220:
        score -= 0.25
    if avg_sentence_length > 28:
        score -= 0.25
    if paragraph_count < 2:
        score -= 0.15

    score = max(0.0, min(1.0, score))

    return {
        "conciseness_result": {
            "score": round(score, 4),
            "details": {
                "definition": "Conciseness Score measures readability, brevity, and structure.",
                "word_count": word_count,
                "avg_sentence_length": round(avg_sentence_length, 2),
                "paragraph_count": paragraph_count,
            },
        }
    }