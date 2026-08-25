import os
import json
import httpx
from typing import List, Dict, Any, Optional

from .base import BaseLLMProvider

PROVIDER_ENDPOINT_MAP = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
    "deepseek": "https://api.deepseek.com/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "ollama": "http://localhost:11434/v1/chat/completions",
    "lmstudio": "http://localhost:1234/v1/chat/completions"
}

PROVIDER_ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "groq": "GROQ_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY"
}


class UniversalLLMProvider(BaseLLMProvider):
    def __init__(
        self,
        model_name: str = "gemini/gemini-2.0-flash",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.model_name = model_name
        self.provider_prefix, self.clean_model_name = self._parse_model_name(model_name)
        self.api_key = api_key or self._resolve_api_key(self.provider_prefix)
        self.base_url = base_url or PROVIDER_ENDPOINT_MAP.get(self.provider_prefix, PROVIDER_ENDPOINT_MAP["openai"])

    def _parse_model_name(self, name: str) -> tuple[str, str]:
        if "/" in name:
            parts = name.split("/", 1)
            return parts[0].lower(), parts[1]
        return "openai", name

    def _resolve_api_key(self, provider: str) -> str:
        env_var = PROVIDER_ENV_KEYS.get(provider, "OPENAI_API_KEY")
        return os.getenv(env_var, os.getenv("LLM_API_KEY", "dummy-key-for-local"))

    def chat_complete(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Sends chat request using OpenAI-compatible HTTP REST protocol."""
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key and self.api_key != "dummy-key-for-local":
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload: Dict[str, Any] = {
            "model": self.clean_model_name,
            "messages": messages,
            "temperature": 0.2
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(self.base_url, headers=headers, json=payload)
                if response.status_code != 200:
                    return {
                        "content": f"API Error (HTTP {response.status_code}): {response.text}",
                        "tool_calls": None,
                        "model": self.model_name
                    }

                data = response.json()
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})

                content = message.get("content") or ""
                raw_tool_calls = message.get("tool_calls")
                parsed_tool_calls = None

                if raw_tool_calls:
                    parsed_tool_calls = []
                    for tc in raw_tool_calls:
                        fn = tc.get("function", {})
                        args = fn.get("arguments", "{}")
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except Exception:
                                args = {}
                        parsed_tool_calls.append({
                            "id": tc.get("id", f"call_{len(parsed_tool_calls)}"),
                            "name": fn.get("name"),
                            "arguments": args
                        })

                return {
                    "content": content,
                    "tool_calls": parsed_tool_calls,
                    "model": self.model_name
                }

        except Exception as e:
            return {
                "content": f"Network Error contacting provider '{self.provider_prefix}': {str(e)}",
                "tool_calls": None,
                "model": self.model_name
            }
