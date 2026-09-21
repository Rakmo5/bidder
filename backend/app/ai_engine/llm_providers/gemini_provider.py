import json
import logging
from typing import Dict, Any, Optional
from google import genai
from app.ai_engine.llm_providers.base_provider import BaseLLMProvider
from app.ai_engine.config import ai_config

logger = logging.getLogger(__name__)

class GeminiLLMProvider(BaseLLMProvider):
    """Google Gemini GenAI Provider (Gemini 2.0 / 1.5 Flash)."""

    def __init__(self):
        self._client = None
        if ai_config.gemini_api_key:
            try:
                self._client = genai.Client(api_key=ai_config.gemini_api_key)
            except Exception as e:
                logger.warning(f"GeminiLLMProvider init error: {e}")

    def is_available(self) -> bool:
        return self._client is not None

    def generate_json(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        if not self.is_available():
            return None

        models = [
            ai_config.gemini_primary_model,
            "gemini-2.0-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash",
            "gemini-pro"
        ]

        for model_name in models:
            try:
                response = self._client.models.generate_content(
                    model=model_name,
                    contents=f"{system_prompt}\n\n{user_prompt}"
                )
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                return json.loads(text.strip())
            except Exception as e:
                logger.debug(f"Gemini model '{model_name}' execution failed: {e}")

        return None
