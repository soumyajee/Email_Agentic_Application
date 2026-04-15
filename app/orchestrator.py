from langgraph.graph import StateGraph, START, END

from app.schemas import GraphState
from app.nodes.prepare_input import prepare_input_node
from app.nodes.build_prompt import build_prompt_node
from app.nodes.generate_emails import generate_email_node
from app.nodes.evaluate_facts import evaluate_facts_node
from app.nodes.evaluate_tone import evaluate_tone_node
from app.nodes.evaluate_conciseness import evaluate_conciseness_node
from app.nodes.aggregate_scores import aggregate_scores_node
from app.nodes.refine_prompts import refine_prompt_node
from app.nodes.format_output import format_output_node


def route_after_aggregation(state: GraphState) -> str:
    """
    Decide whether to retry generation or finish.
    """
    if state.get("should_retry", False):
        return "refine_prompt"
    return "format_output"


def build_email_graph():
    graph = StateGraph(GraphState)

    # Register nodes
    graph.add_node("prepare_input", prepare_input_node)
    graph.add_node("build_prompt", build_prompt_node)
    graph.add_node("generate_email", generate_email_node)
    graph.add_node("evaluate_facts", evaluate_facts_node)
    graph.add_node("evaluate_tone", evaluate_tone_node)
    graph.add_node("evaluate_conciseness", evaluate_conciseness_node)
    graph.add_node("aggregate_scores", aggregate_scores_node)
    graph.add_node("refine_prompt", refine_prompt_node)
    graph.add_node("format_output", format_output_node)

    # Main flow
    graph.add_edge(START, "prepare_input")
    graph.add_edge("prepare_input", "build_prompt")
    graph.add_edge("build_prompt", "generate_email")
    graph.add_edge("generate_email", "evaluate_facts")
    graph.add_edge("evaluate_facts", "evaluate_tone")
    graph.add_edge("evaluate_tone", "evaluate_conciseness")
    graph.add_edge("evaluate_conciseness", "aggregate_scores")

    # Conditional retry or finish
    graph.add_conditional_edges(
        "aggregate_scores",
        route_after_aggregation,
        {
            "refine_prompt": "refine_prompt",
            "format_output": "format_output",
        },
    )

    # Retry loop
    graph.add_edge("refine_prompt", "generate_email")

    # End
    graph.add_edge("format_output", END)

    return graph.compile()