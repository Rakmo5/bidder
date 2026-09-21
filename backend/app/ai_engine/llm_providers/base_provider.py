from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseLLMProvider(ABC):
    """Abstract Base Class defining the LLM client contract."""
    
    @abstractmethod
    def generate_json(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """Executes a structured JSON completion against the LLM."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if the provider is configured and available."""
        pass
