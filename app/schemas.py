from typing import Any, Dict, List, Optional, TypedDict


class Scenario(TypedDict):
    scenario_id: int
    intent: str
    key_facts: List[str]
    tone: str
    human_reference_email: str


class EmailDraft(TypedDict):
    subject: str
    body: str


class MetricResult(TypedDict):
    score: float
    details: Dict[str, Any]


class GraphState(TypedDict, total=False):
    scenario: Scenario
    strategy_name: str
    model_name: str

    prompt: str
    generated_email: EmailDraft

    fact_result: MetricResult
    tone_result: MetricResult
    conciseness_result: MetricResult

    overall_score: float
    retry_count: int
    should_retry: bool

    final_output: Dict[str, Any]