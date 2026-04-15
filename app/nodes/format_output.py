from app.schemas import GraphState


def format_output_node(state: GraphState) -> GraphState:
    scenario = state["scenario"]

    output = {
        "scenario_id": scenario["scenario_id"],
        "strategy_name": state["strategy_name"],
        "model_name": state["model_name"],
        "input": {
            "intent": scenario["intent"],
            "key_facts": scenario["key_facts"],
            "tone": scenario["tone"],
        },
        "generated_email": state["generated_email"],
        "evaluation": {
            "factual_score": state["fact_result"]["score"],
            "tone_match_score": state["tone_result"]["score"],
            "conciseness_score": state["conciseness_result"]["score"],
            "overall_score": state["overall_score"],
            "details": {
                "fact_result": state["fact_result"],
                "tone_result": state["tone_result"],
                "conciseness_result": state["conciseness_result"],
            },
        },
        "human_reference_email": scenario["human_reference_email"],
        "retry_count": state.get("retry_count", 0),
    }

    return {"final_output": output}