from app.llm_clients import OpenRouterClient
from app.schemas import GraphState

client = OpenRouterClient()


def generate_email_node(state: GraphState) -> GraphState:
    text = client.generate_email_text(
        prompt=state["prompt"],
        model_name=state["model_name"],
        temperature=0.3,
    )
    parsed = client.parse_email(text)
    return {"generated_email": parsed}