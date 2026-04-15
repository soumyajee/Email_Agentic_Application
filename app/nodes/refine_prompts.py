from app.prompts import build_refinement_prompt
from app.schemas import GraphState


def refine_prompt_node(state: GraphState) -> GraphState:
    scenario = state["scenario"]
    missed = state["fact_result"]["details"]["missed_facts"]
    email = state["generated_email"]

    previous_email = f'Subject: {email["subject"]}\n\n{email["body"]}'
    prompt = build_refinement_prompt(
        scenario=scenario,
        previous_email=previous_email,
        missing_facts=missed,
    )

    return {
        "prompt": prompt,
        "retry_count": state.get("retry_count", 0) + 1,
    }