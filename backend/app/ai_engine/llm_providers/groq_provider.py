import json
import logging
from typing import Dict, Any, Optional
from groq import Groq
from app.ai_engine.llm_providers.base_provider import BaseLLMProvider
from app.ai_engine.config import ai_config

logger = logging.getLogger(__name__)

class GroqLLMProvider(BaseLLMProvider):
    """Groq Cloud LPU Inference Provider (Llama-3.3-70B & Llama-3.1-8B)."""

    def __init__(self):
        self._client = None
        if ai_config.groq_api_key:
            try:
                self._client = Groq(api_key=ai_config.groq_api_key)
            except Exception as e:
                logger.warning(f"GroqLLMProvider init error: {e}")

    def is_available(self) -> bool:
        return self._client is not None

    def generate_json(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        if not self.is_available():
            return None

        models = [
            ai_config.groq_primary_model,
            ai_config.groq_fast_model,
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "mixtral-8x7b-32768"
        ]

        for model_name in models:
            try:
                response = self._client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0
                )
                raw_json = response.choices[0].message.content
                return json.loads(raw_json)
            except Exception as e:
                logger.debug(f"Groq model '{model_name}' execution failed: {e}")
        
        return None
