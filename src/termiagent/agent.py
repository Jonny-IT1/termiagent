import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

from .providers.base import BaseLLMProvider
from .providers.universal import UniversalLLMProvider
from .tools.base import ToolRegistry
from .tools.filesystem import get_filesystem_tools
from .tools.shell import get_shell_tools

DEFAULT_SYSTEM_PROMPT = """You are TermiAgent, an autonomous open-source AI coding assistant running directly inside the user's terminal.
Your goal is to inspect codebases, write clean code, debug issues, and execute terminal commands to solve developer tasks.

### Guidelines:
1. Use the provided tools (view_file, write_file, edit_file, list_directory, search_codebase, run_shell_command) to inspect and modify code.
2. Inspect file contents before editing to avoid introducing syntax errors or breaking existing functionality.
3. Keep your text responses concise and informative.
4. When writing code, write production-ready code with clean docstrings and types.
"""

class TermiAgent:
    def __init__(
        self,
        provider: Optional[BaseLLMProvider] = None,
        model_name: str = "gemini/gemini-2.0-flash",
        work_dir: str = ".",
        system_prompt: Optional[str] = None
    ):
        self.work_dir = Path(work_dir).resolve()
        self.provider = provider or UniversalLLMProvider(model_name=model_name)
        self.registry = ToolRegistry()
        self._register_default_tools()

        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt or self._build_system_prompt()}
        ]

    def _register_default_tools(self):
        for tool in get_filesystem_tools():
            self.registry.register(tool)
        for tool in get_shell_tools():
            self.registry.register(tool)

    def _build_system_prompt(self) -> str:
        prompt = DEFAULT_SYSTEM_PROMPT
        prompt += f"\nCurrent Working Directory: {self.work_dir}\n"
        prompt += f"Operating System: {os.name}\n"
        return prompt

    def run_turn(
        self,
        user_input: str,
        on_thought: Optional[Callable[[str], None]] = None,
        on_tool_call: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        on_tool_result: Optional[Callable[[str, str], None]] = None,
        max_iterations: int = 10
    ) -> str:
        """
        Executes a single user interaction turn, running the ReAct tool calling loop until complete.
        """
        self.messages.append({"role": "user", "content": user_input})
        openai_tools = self.registry.get_openai_tools()

        for _ in range(max_iterations):
            response = self.provider.chat_complete(self.messages, tools=openai_tools)
            content = response.get("content", "")
            tool_calls = response.get("tool_calls")

            if content and on_thought:
                on_thought(content)

            if not tool_calls:
                self.messages.append({"role": "assistant", "content": content})
                return content

            # Append assistant turn with tool calls
            self.messages.append({
                "role": "assistant",
                "content": content,
                "tool_calls": [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {"name": tc["name"], "arguments": str(tc["arguments"])}
                    }
                    for tc in tool_calls
                ]
            })

            # Execute tool calls
            for tc in tool_calls:
                t_id = tc["id"]
                t_name = tc["name"]
                t_args = tc["arguments"]

                if on_tool_call:
                    on_tool_call(t_name, t_args)

                result = self.registry.execute_tool(t_name, t_args)

                if on_tool_result:
                    on_tool_result(t_name, result)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": t_id,
                    "name": t_name,
                    "content": result
                })

        return "Reached maximum turn iterations without completing tool calls."

    def clear_history(self):
        """Clears conversation history except system prompt."""
        sys_msg = self.messages[0] if self.messages else {"role": "system", "content": self._build_system_prompt()}
        self.messages = [sys_msg]
