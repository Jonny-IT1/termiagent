from typing import Callable, Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True

class ToolSpec(BaseModel):
    name: str
    description: str
    parameters: List[ToolParameter]

    def to_openai_json(self) -> Dict[str, Any]:
        properties = {}
        required_list = []
        for p in self.parameters:
            properties[p.name] = {
                "type": p.type,
                "description": p.description
            }
            if p.required:
                required_list.append(p.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_list
                }
            }
        }


class Tool:
    def __init__(self, spec: ToolSpec, func: Callable[..., Any]):
        self.spec = spec
        self.func = func

    def execute(self, **kwargs) -> str:
        try:
            res = self.func(**kwargs)
            return str(res)
        except Exception as e:
            return f"Error executing tool {self.spec.name}: {str(e)}"


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.spec.name] = tool

    def get_openai_tools(self) -> List[Dict[str, Any]]:
        return [t.spec.to_openai_json() for t in self.tools.values()]

    def execute_tool(self, name: str, args: Dict[str, Any]) -> str:
        if name not in self.tools:
            return f"Unknown tool: {name}"
        return self.tools[name].execute(**args)
