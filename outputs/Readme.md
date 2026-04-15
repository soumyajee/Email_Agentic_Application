# Email Generation Assistant

An agentic email generation and evaluation system built with **LangGraph** and **OpenRouter**.

This project generates professional emails from structured inputs and evaluates them using three custom metrics:

- **Factual Score**
- **Tone Match Score**
- **Conciseness Score**

It also compares two generation strategies:

- **Baseline**
- **Advanced**

Based on the current evaluation output, the **baseline strategy using `anthropic/claude-opus-4.6`** performed better overall than the advanced strategy using `openai/gpt-5.4`. The current output file shows an average overall score of **0.90** for the baseline and **0.7574** for the advanced strategy. :contentReference[oaicite:0]{index=0}

---

## 1. Project Objective

The goal of this project is to build an **Email Generation Assistant** that:

1. Accepts:
   - **Intent**
   - **Key Facts**
   - **Tone**

2. Generates:
   - A professional email with:
     - subject
     - body

3. Evaluates the generated email using custom metrics:
   - **Fact Recall Score**
   - **Tone Match Score**
   - **Conciseness Score**

4. Compares two models / prompting strategies and recommends the stronger one.

---

## 2. Tech Stack

- **Python**
- **LangGraph** for orchestration
- **OpenRouter** as model gateway
- **OpenAI-compatible SDK**
- **JSON** output for evaluation results

---

## 3. Project Structure

```text
email_generation_assistance/
│
├── app/
│   ├── data/
│   │   └── test_scenarios.py
│   │
│   ├── nodes/
│   │   ├── aggregate_scores.py
│   │   ├── build_prompt.py
│   │   ├── evaluate_conciseness.py
│   │   ├── evaluate_facts.py
│   │   ├── evaluate_tone.py
│   │   ├── format_output.py
│   │   ├── generate_emails.py
│   │   ├── prepare_input.py
│   │   └── refine_prompt.py
│   │
│   ├── .env
│   ├── config.py
│   ├── llm_clients.py
│   ├── main.py
│   ├── orchestrator.py
│   ├── prompts.py
│   ├── schemas.py
│   └── requirements.txt
│
├── outputs/
│   └── evaluation_results.json
│
└── Readme.md
4. Workflow Overview

This project uses LangGraph to orchestrate the workflow.
Graph flow
START
  -> prepare_input
  -> build_prompt
  -> generate_email
  -> evaluate_facts
  -> evaluate_tone
  -> evaluate_conciseness
  -> aggregate_scores
      -> if score is low -> refine_prompt -> generate_email
      -> else -> format_output
  -> END
What each node does
prepare_input.py

Initializes and normalizes the state passed into the graph.

build_prompt.py

Builds the model prompt from:

intent
key facts
tone
selected strategy (baseline or advanced)
generate_emails.py

Calls the OpenRouter model and parses the response into:

subject
body
evaluate_facts.py

Checks whether all required facts appear in the generated email.

evaluate_tone.py

Checks whether the generated email matches the requested tone using tone markers.

evaluate_conciseness.py

Measures readability and structure using:

word count
sentence length
paragraph count
aggregate_scores.py

Combines all metric scores into one overall score.

refine_prompt.py

If the score is below threshold, rebuilds the prompt and retries generation.

format_output.py

Formats the final result into structured JSON.
5. File-by-File Explanation
config.py

Stores environment and model configuration.

Typical values:

OpenRouter API key
base URL
primary model
secondary model
app name / referer
schemas.py

Defines the shared workflow state and data contracts used across graph nodes.

Contains structures like:

scenario
prompt
generated email
metric results
final output
prompts.py

Contains prompt templates for:

baseline generation
advanced generation
refinement prompt

This is where prompt engineering logic is defined.
llm_clients.py

Handles model calls through OpenRouter.

Responsibilities:

initialize OpenRouter-compatible client
generate email text
parse email output into:
subject
body

Important fix:
This file should explicitly set a small max_tokens value, such as 300 or 400, to avoid OpenRouter credit errors.
orchestrator.py

Builds the LangGraph workflow.

Responsibilities:

define graph nodes
define edges
define retry routing
compile the workflow

This is the orchestration layer of the system.
main.py

Project entry point.

Responsibilities:

load scenarios
run baseline strategy
run advanced strategy
save evaluation results into outputs/evaluation_results.json
data/test_scenarios.py

Contains all test scenarios.

Each scenario includes:

scenario_id
intent
key_facts
tone
human_reference_email
outputs/evaluation_results.json

Stores the final structured output of the evaluation.

Current file contents include:

metric definitions
raw results
summary metrics
recommended model

The uploaded result currently shows 3 scenarios, not 10, so more scenarios still need to be added if the assignment requires 10 full test cases.
6. Input Format

Each test scenario should look like this:
{
  "scenario_id": 1,
  "intent": "Follow up after client meeting",
  "key_facts": [
    "Thank the client for meeting on Monday",
    "Mention the pricing proposal was attached",
    "Request feedback by Friday"
  ],
  "tone": "formal",
  "human_reference_email": "Subject: Follow-Up After Monday's Meeting\n\nDear [Client Name],\n\nThank you for meeting with us on Monday..."
}
7. Output Format

The system produces JSON like:
{
  "scenario_id": 1,
  "strategy_name": "baseline",
  "model_name": "anthropic/claude-opus-4.6",
  "input": {
    "intent": "Follow up after client meeting",
    "key_facts": [
      "Thank the client for meeting on Monday",
      "Mention the pricing proposal was attached",
      "Request feedback by Friday"
    ],
    "tone": "formal"
  },
  "generated_email": {
    "subject": "Follow-Up on Monday's Meeting and Pricing Proposal",
    "body": "Dear [Client Name], ..."
  },
  "evaluation": {
    "factual_score": 1.0,
    "tone_match_score": 0.8,
    "conciseness_score": 1.0,
    "overall_score": 0.9333
  },
  "human_reference_email": "Subject: Follow-Up After Monday's Meeting...",
  "retry_count": 0
}
8. Custom Metrics
1. Fact Recall Score

Measures whether all required facts are present in the generated email.

Formula:
matched required facts / total required facts
Example from current results:

Baseline scenario 1 scored 1.0
Advanced scenario 2 scored 0.6667 because one required fact was missed.
2. Tone Match Score

Measures alignment with the requested tone using predefined marker words.

Examples:

formal markers: dear, regards, thank you, please
urgent markers: urgent, today, as soon as possible
empathetic markers: sorry, understand, patience

This is a heuristic metric
3. Conciseness Score

Measures whether the email is readable and appropriately brief using:

word count
average sentence length
paragraph structure

Important note:
This metric is effectively measuring brevity + completeness + structure, not just shortness.

That is why very short emails can lose points.
9. Current Evaluation Summary

From the current evaluation_results.json:

Baseline
Model: anthropic/claude-opus-4.6
Average Factual Score: 1.0
Average Tone Match Score: 0.7
Average Conciseness Score: 1.0
Average Overall Score: 0.9
Advanced
Model: openai/gpt-5.4
Average Factual Score: 0.8889
Average Tone Match Score: 0.6333
Average Conciseness Score: 0.75
Average Overall Score: 0.7574
Recommended Model
anthropic/claude-opus-4.6
10. Why Baseline Performed Better

Based on the current output:

Better fact retention
The baseline included all required facts in the shown scenarios.
Better score under the conciseness metric
The advanced strategy often generated shorter emails, which reduced its conciseness score under the current scoring rules.
Slightly better tone alignment
The baseline also scored slightly higher on tone marker coverage.
11. Setup Instructions
Step 1: Create environment
conda create -n email_gen python=3.10 -y
conda activate email_gen
or with venv:
python -m venv venv
venv\Scripts\activate
Step 2: Install dependencies
pip install -r app/requirements.txt
If your requirements.txt is in root, then use:
pip install -r requirements.txt
Step 3: Create .env

Example:
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL_PRIMARY=anthropic/claude-opus-4.6
OPENROUTER_MODEL_SECONDARY=openai/gpt-5.4
OPENROUTER_SITE_URL=http://localhost:8000
OPENROUTER_APP_NAME=Email Generation Assistant
12. How to Run

From the project root:
python -m app.main
This will:

load scenarios
run both strategies
evaluate outputs
save results to:
outputs/evaluation_results.json
13. Common Errors and Fixes
Error: OpenRouter 402 credits / max tokens

If you see:
This request requires more credits, or fewer max_tokens
Fix:

reduce max_tokens in llm_clients.py
use something like
max_tokens=400
Error: OpenRouterClient has no attribute parse_email

Fix:
Make sure parse_email() exists inside the OpenRouterClient class.

Error: imports not found

Fix:
Run from project root:
python -m app.main
Also make sure app/ is treated as a package.
Also make sure app/ is treated as a package.

14. Limitations

Current limitations:

Only 3 scenarios are currently present in the shown output, while the assignment asks for 10.
Tone evaluation is heuristic and based on marker matching.
Conciseness scoring may penalize very short but still acceptable emails.
Fact evaluation is keyword-overlap based and can be improved with semantic judging.
15. Recommended Improvements

Future improvements:

Add all 10 scenarios
Replace heuristic tone scoring with LLM-as-a-Judge
Add semantic fact checking
Export results to CSV in addition to JSON
Add FastAPI endpoint for production usage
Store evaluations in a database
Add human-in-the-loop review step
Add LangSmith or logging for tracing
16. Production Recommendation

Based on current evaluation data, the recommended production model is:

anthropic/claude-opus-4.6

Reason:
It achieved the highest overall score and showed stronger fact retention and structural quality in the current evaluation run.

17. Example Use Case

Input:

Intent: Follow up after client meeting
Key Facts:
Thank the client for meeting on Monday
Mention the pricing proposal was attached
Request feedback by Friday
Tone: formal

Output:
A polished professional email plus metric-based evaluation.

18. Author Notes

This project demonstrates:

prompt engineering
agentic orchestration using LangGraph
structured evaluation
model comparison
JSON-based reporting

It is designed as a prototype that can be extended into a production backend service.

If you want, I can also give you:
- a **short professional README version**
- a **GitHub polished README version with badges**
- or **separate README files for each folder** like `app/`, `nodes/`, and `data/`.

