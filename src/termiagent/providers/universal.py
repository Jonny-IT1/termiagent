import os
import json
import base64
import httpx
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from .base import BaseLLMProvider

PROVIDER_ENDPOINT_MAP = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
    "deepseek": "https://api.deepseek.com/chat/completions",
    "mistral": "https://api.mistral.ai/v1/chat/completions",
    "minimax": "https://api.minimaxi.chat/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "ollama": "http://localhost:11434/v1/chat/completions",
    "lmstudio": "http://localhost:1234/v1/chat/completions"
}

PROVIDER_ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "minimax": "MINIMAX_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "groq": "GROQ_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY"
}

# Complete Catalog of Modern, Vision, and Legacy Models
MODEL_CATALOG = {
    # OpenAI (Modern, Vision & Legacy)
    "openai/latest": "gpt-4o",
    "openai/gpt-4o": "gpt-4o",
    "openai/gpt-4o-mini": "gpt-4o-mini",
    "openai/o1": "o1",
    "openai/o3-mini": "o3-mini",
    "openai/gpt-4-turbo": "gpt-4-turbo",
    "openai/gpt-4": "gpt-4",
    "openai/gpt-3.5-turbo": "gpt-3.5-turbo",

    # Google Gemini (Modern, Vision & Legacy)
    "gemini/latest": "gemini-2.0-flash",
    "gemini/gemini-2.0-flash": "gemini-2.0-flash",
    "gemini/gemini-2.0-pro-exp": "gemini-2.0-pro-exp",
    "gemini/gemini-1.5-pro": "gemini-1.5-pro",
    "gemini/gemini-1.5-flash": "gemini-1.5-flash",
    "gemini/gemini-1.0-pro": "gemini-1.0-pro",

    # Anthropic Claude (Modern & Legacy)
    "anthropic/latest": "claude-3-5-sonnet-20241022",
    "anthropic/claude-3-5-sonnet": "claude-3-5-sonnet-20241022",
    "anthropic/claude-3-5-haiku": "claude-3-5-haiku-20241022",
    "anthropic/claude-3-opus": "claude-3-opus-20240229",
    "anthropic/claude-3-sonnet": "claude-3-sonnet-20240229",
    "anthropic/claude-3-haiku": "claude-3-haiku-20240307",
    "anthropic/claude-2.1": "claude-2.1",

    # DeepSeek
    "deepseek/latest": "deepseek-chat",
    "deepseek/deepseek-chat": "deepseek-chat",
    "deepseek/deepseek-reasoner": "deepseek-reasoner",
    "deepseek/deepseek-coder": "deepseek-coder",
    "deepseek/deepseek-vl": "deepseek-vl",

    # Mistral AI (Modern, Vision & Legacy)
    "mistral/latest": "codestral-latest",
    "mistral/codestral": "codestral-latest",
    "mistral/mistral-large": "mistral-large-latest",
    "mistral/pixtral-large": "pixtral-large-latest", # Vision Model
    "mistral/mistral-small": "mistral-small-latest",
    "mistral/mistral-medium": "mistral-medium",      # Legacy

    # MiniMax (Modern & Legacy)
    "minimax/latest": "minimax-text-01",
    "minimax/minimax-text-01": "minimax-text-01",
    "minimax/abab6.5t": "abab6.5t-chat",
    "minimax/abab6.5g": "abab6.5g-chat",
    "minimax/abab6.5": "abab6.5-chat",
    "minimax/abab5.5": "abab5.5-chat",               # Legacy

    # Groq (Super-Fast)
    "groq/latest": "llama-3.3-70b-versatile",
    "groq/llama-3.3-70b": "llama-3.3-70b-versatile",
    "groq/deepseek-r1-70b": "deepseek-r1-distill-llama-70b",
    "groq/mixtral-8x7b": "mixtral-8x7b-32768",

    # Local Ollama
    "ollama/latest": "qwen2.5-coder:latest",
    "ollama/qwen2.5-coder": "qwen2.5-coder:latest",
    "ollama/llama3.3": "llama3.3:latest",
    "ollama/llava": "llava:latest",                    # Vision Model
    "ollama/qwen2-vl": "qwen2-vl:latest"              # Vision Model
}


class UniversalLLMProvider(BaseLLMProvider):
    def __init__(
        self,
        model_name: str = "gemini/gemini-2.0-flash",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        raw_key = model_name.lower()
        clean = MODEL_CATALOG.get(raw_key, model_name)
        if "/" not in clean and "/" in model_name:
            provider_part = model_name.split("/", 1)[0].lower()
            clean = f"{provider_part}/{clean}"

        self.model_name = clean
        self.provider_prefix, self.clean_model_name = self._parse_model_name(self.model_name)
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

    @staticmethod
    def encode_image_to_base64(image_path: Union[str, Path]) -> str:
        """Helper to encode a local image into base64 data URI for vision model inputs."""
        path = Path(image_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Image file '{image_path}' not found.")

        ext = path.suffix.lower().lstrip(".")
        mime_type = f"image/{ext}" if ext in ["png", "jpeg", "jpg", "webp", "gif"] else "image/png"

        with open(path, "rb") as image_file:
            encoded_bytes = base64.b64encode(image_file.read()).decode("utf-8")

        return f"data:{mime_type};base64,{encoded_bytes}"

    def chat_complete(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Sends chat request using OpenAI-compatible HTTP REST protocol with Vision payload support."""
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
                        "content": f"API Error ({self.provider_prefix} HTTP {response.status_code}): {response.text}",
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
