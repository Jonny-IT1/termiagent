from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLMProvider(ABC):
    @abstractmethod
    def chat_complete(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executes a chat completion request and returns normalized response dict:
        {
            "content": str,
            "tool_calls": Optional[List[Dict[str, Any]]],
            "model": str
        }
        """
        pass
