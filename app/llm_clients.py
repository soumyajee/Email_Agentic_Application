import re
from openai import OpenAI
from app.config import settings


class OpenRouterClient:
    def __init__(self) -> None:
        settings.validate()
        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
        )
        self.default_headers = {
            "HTTP-Referer": settings.openrouter_site_url,
            "X-OpenRouter-Title": settings.openrouter_app_name,
        }

    def generate_email_text(
        self,
        prompt: str,
        model_name: str,
        temperature: float = 0.3,
        max_tokens: int = 400,
    ) -> str:
        response = self.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You write high-quality professional emails."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            extra_headers=self.default_headers,
        )
        return response.choices[0].message.content or ""

    @staticmethod
    def parse_email(text: str) -> dict:
        subject_match = re.search(r"Subject:\s*(.+)", text)
        subject = subject_match.group(1).strip() if subject_match else "No Subject"

        body = text[subject_match.end():].strip() if subject_match else text.strip()

        return {
            "subject": subject,
            "body": body,
        }