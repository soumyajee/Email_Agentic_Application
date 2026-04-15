from app.prompts import build_advanced_prompt, build_baseline_prompt
from app.schemas import GraphState


def build_prompt_node(state: GraphState) -> GraphState:
    scenario = state["scenario"]
    strategy_name = state["strategy_name"]

    if strategy_name == "baseline":
        prompt = build_baseline_prompt(scenario)
    else:
        prompt = build_advanced_prompt(scenario)

    return {"prompt": prompt}