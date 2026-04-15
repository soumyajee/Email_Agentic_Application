from app.schemas import GraphState


def aggregate_scores_node(state: GraphState) -> GraphState:
    fact_score = state["fact_result"]["score"]
    tone_score = state["tone_result"]["score"]
    conciseness_score = state["conciseness_result"]["score"]

    overall = round((fact_score + tone_score + conciseness_score) / 3, 4)

    should_retry = overall < 0.75 and state.get("retry_count", 0) < 1

    return {
        "overall_score": overall,
        "should_retry": should_retry,
    }