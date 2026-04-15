from app.schemas import GraphState

FORMAL = {"dear", "regards", "sincerely", "please", "thank you"}
CASUAL = {"hi", "thanks", "quick", "great", "let me know"}
URGENT = {"urgent", "today", "as soon as possible", "priority"}
EMPATHETIC = {"sorry", "understand", "appreciate", "patience", "support"}


def _markers_for_tone(tone: str) -> list[str]:
    t = tone.lower()
    if "formal" in t:
        return list(FORMAL)
    if "casual" in t:
        return list(CASUAL)
    if "urgent" in t:
        return list(URGENT)
    if "empathetic" in t:
        return list(EMPATHETIC)
    return []


def evaluate_tone_node(state: GraphState) -> GraphState:
    tone = state["scenario"]["tone"]
    email = state["generated_email"]
    text = f'{email["subject"]}\n{email["body"]}'.lower()

    markers = _markers_for_tone(tone)
    matched = [m for m in markers if m in text]
    score = len(matched) / len(markers) if markers else 0.5

    return {
        "tone_result": {
            "score": round(score, 4),
            "details": {
                "definition": "Tone Match Score = matched tone markers / expected tone markers",
                "matched_markers": matched,
                "expected_markers": markers,
            },
        }
    }