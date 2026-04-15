import re
from app.schemas import GraphState


def _fact_present(fact: str, email_text: str) -> bool:
    cleaned_fact = re.sub(r"[^a-zA-Z0-9\s]", "", fact.lower())
    tokens = [t for t in cleaned_fact.split() if len(t) > 3]
    if not tokens:
        return False

    overlap = sum(1 for token in tokens if token in email_text)
    return (overlap / len(tokens)) >= 0.5


def evaluate_facts_node(state: GraphState) -> GraphState:
    scenario = state["scenario"]
    email = state["generated_email"]
    email_text = f'{email["subject"]}\n{email["body"]}'.lower()

    matched = []
    missed = []

    for fact in scenario["key_facts"]:
        if _fact_present(fact, email_text):
            matched.append(fact)
        else:
            missed.append(fact)

    score = len(matched) / len(scenario["key_facts"]) if scenario["key_facts"] else 1.0

    return {
        "fact_result": {
            "score": round(score, 4),
            "details": {
                "definition": "Fact Recall Score = matched required facts / total required facts",
                "matched_facts": matched,
                "missed_facts": missed,
            },
        }
    }