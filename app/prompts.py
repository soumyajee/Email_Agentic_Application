from app.schemas import Scenario


def build_baseline_prompt(scenario: Scenario) -> str:
    facts_block = "\n".join(f"- {fact}" for fact in scenario["key_facts"])
    return f"""
Write a professional email.

Intent:
{scenario["intent"]}

Key Facts:
{facts_block}

Tone:
{scenario["tone"]}

Requirements:
- Include all key facts naturally.
- Match the tone.
- Keep it professional.
- Return in this format only.

Subject: <subject line>

<body>
""".strip()


def build_advanced_prompt(scenario: Scenario) -> str:
    facts_block = "\n".join(f"- {fact}" for fact in scenario["key_facts"])
    return f"""
You are a senior executive communications assistant.

Your task is to write a polished business email.

Rules:
1. Use the intent accurately.
2. Include every required fact without inventing anything.
3. Match the requested tone exactly.
4. Keep the email concise, readable, and professional.
5. Add a strong subject line.
6. Use natural phrasing rather than copying the bullet points.

Few-shot example:

Intent:
Follow up after product demo

Key Facts:
- Thank them for attending the demo
- Mention pricing sheet was attached
- Ask whether they want a technical walkthrough next week

Tone:
formal

Output:
Subject: Follow-Up After Product Demo

Dear [Name],

Thank you for attending the product demo. I appreciate the opportunity to speak with you.

As discussed, I have attached the pricing sheet for your review. Please let me know if you would like to schedule a technical walkthrough next week so we can address any further questions.

Best regards,
[Your Name]

Now complete this task:

Intent:
{scenario["intent"]}

Key Facts:
{facts_block}

Tone:
{scenario["tone"]}

Return only:

Subject: <subject line>

<body>
""".strip()


def build_refinement_prompt(scenario: Scenario, previous_email: str, missing_facts: list[str]) -> str:
    missing_block = "\n".join(f"- {fact}" for fact in missing_facts) if missing_facts else "- None"
    return f"""
You are revising an email draft.

The previous draft did not fully satisfy the requirements.

Intent:
{scenario["intent"]}

Tone:
{scenario["tone"]}

Required facts that must be present:
{missing_block}

Previous draft:
{previous_email}

Instructions:
- Rewrite the email.
- Preserve professionalism.
- Make sure all missing facts are included naturally.
- Keep it concise.
- Return only:

Subject: <subject line>

<body>
""".strip()