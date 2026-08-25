import subprocess
import os
from pathlib import Path
from typing import List, Optional

from .base import Tool, ToolSpec, ToolParameter


def run_shell_command(command: str, cwd: Optional[str] = None, timeout_seconds: int = 60) -> str:
    """Executes a shell command safely and returns stdout and stderr."""
    target_cwd = Path(cwd).resolve() if cwd else Path.cwd()

    try:
        res = subprocess.run(
            command,
            shell=True,
            cwd=str(target_cwd),
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )

        stdout = res.stdout.strip()
        stderr = res.stderr.strip()
        exit_code = res.returncode

        output_parts = [f"Exit Code: {exit_code}"]
        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")

        return "\n".join(output_parts)
    except subprocess.TimeoutExpired:
        return f"Error: Command '{command}' timed out after {timeout_seconds} seconds."
    except Exception as e:
        return f"Error executing shell command '{command}': {str(e)}"


def get_shell_tools() -> List[Tool]:
    """Returns shell execution tool spec."""
    return [
        Tool(
            spec=ToolSpec(
                name="run_shell_command",
                description="Executes a bash/terminal command in the project directory.",
                parameters=[
                    ToolParameter(name="command", type="string", description="Exact shell command to execute."),
                    ToolParameter(name="cwd", type="string", description="Working directory path.", required=False),
                    ToolParameter(name="timeout_seconds", type="integer", description="Execution timeout in seconds.", required=False)
                ]
            ),
            func=run_shell_command
        )
    ]
