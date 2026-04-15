from app.schemas import GraphState


def prepare_input_node(state: GraphState) -> GraphState:
    scenario = state["scenario"]
    return {
        "scenario": scenario,
        "strategy_name": state["strategy_name"],
        "model_name": state["model_name"],
        "retry_count": state.get("retry_count", 0),
        "should_retry": False,
    }