from app.schemas import Scenario


def build_test_scenarios() -> list[Scenario]:
    return [
        {
            "scenario_id": 1,
            "intent": "Follow up after client meeting",
            "key_facts": [
                "Thank the client for meeting on Monday",
                "Mention the pricing proposal was attached",
                "Request feedback by Friday",
            ],
            "tone": "formal",
            "human_reference_email": (
                "Subject: Follow-Up After Monday's Meeting\n\n"
                "Dear [Client Name],\n\n"
                "Thank you for meeting with us on Monday. As discussed, I have attached "
                "the pricing proposal for your review. We would appreciate your feedback "
                "by Friday so we can align on next steps.\n\n"
                "Best regards,\n[Your Name]"
            ),
        },
        {
            "scenario_id": 2,
            "intent": "Request project update from internal team",
            "key_facts": [
                "Ask for status of API integration",
                "Mention launch is scheduled for next Wednesday",
                "Request blockers if any",
            ],
            "tone": "urgent",
            "human_reference_email": (
                "Subject: Urgent Request for API Integration Update\n\n"
                "Hi Team,\n\n"
                "Could you please share the current status of the API integration? "
                "Our launch is scheduled for next Wednesday, so I need to understand "
                "whether there are any blockers that could impact the timeline.\n\n"
                "Thanks,\n[Your Name]"
            ),
        },
        {
            "scenario_id": 3,
            "intent": "Respond to delayed customer support case",
            "key_facts": [
                "Apologize for the delay",
                "Mention issue is under investigation",
                "Promise next update within 24 hours",
            ],
            "tone": "empathetic",
            "human_reference_email": (
                "Subject: Update on Your Support Request\n\n"
                "Dear [Customer Name],\n\n"
                "I sincerely apologize for the delay in resolving your issue. "
                "Our team is actively investigating the matter, and I will provide "
                "you with another update within the next 24 hours.\n\n"
                "Thank you for your patience.\n\n"
                "Best,\n[Your Name]"
            ),
        },
    ]