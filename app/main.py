import json
import os

from app.config import settings
from app.data.test_scenario import build_test_scenarios
from app.orchestrator import build_email_graph


def summarize_results(results: list[dict], strategy_name: str, model_name: str) -> dict:
    factual_scores = [r["evaluation"]["factual_score"] for r in results]
    tone_scores = [r["evaluation"]["tone_match_score"] for r in results]
    conciseness_scores = [r["evaluation"]["conciseness_score"] for r in results]
    overall_scores = [r["evaluation"]["overall_score"] for r in results]

    return {
        "strategy_name": strategy_name,
        "model_name": model_name,
        "average_factual_score": round(sum(factual_scores) / len(factual_scores), 4),
        "average_tone_match_score": round(sum(tone_scores) / len(tone_scores), 4),
        "average_conciseness_score": round(sum(conciseness_scores) / len(conciseness_scores), 4),
        "average_overall_score": round(sum(overall_scores) / len(overall_scores), 4),
    }


def run_strategy(strategy_name: str, model_name: str) -> dict:
    app = build_email_graph()
    scenarios = build_test_scenarios()
    results = []

    for scenario in scenarios:
        final_state = app.invoke(
            {
                "scenario": scenario,
                "strategy_name": strategy_name,
                "model_name": model_name,
                "retry_count": 0,
            }
        )
        results.append(final_state["final_output"])

    return {
        "raw_results": results,
        "summary": summarize_results(results, strategy_name, model_name),
    }


def main() -> None:
    settings.validate()
    os.makedirs("outputs", exist_ok=True)

    baseline_results = run_strategy(
        strategy_name="baseline",
        model_name=settings.openrouter_model_primary,
    )

    advanced_results = run_strategy(
        strategy_name="advanced",
        model_name=settings.openrouter_model_secondary,
    )

    baseline_avg = baseline_results["summary"]["average_overall_score"]
    advanced_avg = advanced_results["summary"]["average_overall_score"]

    final_output = {
        "metric_definitions": {
            "factual_score": "Fact Recall Score = proportion of required facts included correctly.",
            "tone_match_score": "Tone Match Score = alignment of language with requested tone.",
            "conciseness_score": "Conciseness Score = clarity, brevity, and readability of the email.",
        },
        "model_results": {
            "baseline": baseline_results,
            "advanced": advanced_results,
        },
        "recommended_model": (
            settings.openrouter_model_secondary
            if advanced_avg >= baseline_avg
            else settings.openrouter_model_primary
        ),
    }

    with open("outputs/evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print("Saved results to outputs/evaluation_results.json")


if __name__ == "__main__":
    main()