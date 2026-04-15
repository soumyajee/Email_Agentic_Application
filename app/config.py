import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model_primary: str = os.getenv("OPENROUTER_MODEL_PRIMARY", "anthropic/claude-opus-4.6")
    openrouter_model_secondary: str = os.getenv("OPENROUTER_MODEL_SECONDARY", "openai/gpt-5.4")
    openrouter_site_url: str = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8000")
    openrouter_app_name: str = os.getenv("OPENROUTER_APP_NAME", "Email Generation Assistant")

    def validate(self) -> None:
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is missing. Add it to your .env file.")


settings = Settings()