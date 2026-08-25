import os
import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.status import Status
from rich.prompt import Prompt

from .agent import TermiAgent
from .providers.universal import UniversalLLMProvider

console = Console()

WELCOME_BANNER = """[bold indigo]TermiAgent[/bold indigo] — Universal Terminal AI Coding Agent
[slate4]Connect any AI Model • Edit Codebase • Run Commands[/slate4]
Type [bold cyan]/help[/bold cyan] for slash commands or [bold cyan]/exit[/bold cyan] to quit."""


@click.command()
@click.option("-m", "--model", default="gemini/gemini-2.0-flash", help="LLM Provider and Model (e.g. gemini/gemini-2.0-flash, openai/gpt-4o, deepseek/deepseek-chat, ollama/qwen2.5-coder)")
@click.option("-k", "--api-key", help="API Key for the provider (or set env var).")
@click.option("-w", "--work-dir", default=".", type=click.Path(exists=True), help="Target codebase working directory.")
@click.option("-p", "--prompt", "one_shot_prompt", help="Execute a single prompt and exit.")
def main(model: str, api_key: str, work_dir: str, one_shot_prompt: str):
    """TermiAgent — Universal Terminal AI Coding Agent CLI."""
    target_path = Path(work_dir).resolve()
    provider = UniversalLLMProvider(model_name=model, api_key=api_key)
    agent = TermiAgent(provider=provider, work_dir=str(target_path))

    if one_shot_prompt:
        console.print(f"[bold cyan]TermiAgent ({model})[/bold cyan] executing task in [dim]{target_path}[/dim]...")
        _run_agent_turn(agent, one_shot_prompt)
        return

    # Interactive REPL mode
    console.print(Panel(WELCOME_BANNER, title="[bold]Welcome[/bold]", border_style="indigo"))
    console.print(f"Working Directory: [cyan]{target_path}[/cyan] | Active Model: [bold green]{model}[/bold green]\n")

    while True:
        try:
            user_input = console.input("[bold indigo]termiagent>[/bold indigo] ").strip()
            if not user_input:
                continue

            # Handle Slash Commands
            if user_input.startswith("/"):
                if _handle_slash_command(user_input, agent):
                    break
                continue

            _run_agent_turn(agent, user_input)

        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Exiting TermiAgent. Goodbye![/yellow]")
            break


def _handle_slash_command(cmd_str: str, agent: TermiAgent) -> bool:
    """Returns True if the CLI loop should exit."""
    parts = cmd_str.split(maxsplit=1)
    command = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if command in ["/exit", "/quit"]:
        console.print("[yellow]Goodbye![/yellow]")
        return True

    elif command == "/help":
        console.print(Panel("""[bold]Available Slash Commands:[/bold]
  [cyan]/model <name>[/cyan]  - Switch LLM model live (e.g. /model ollama/llama3.3)
  [cyan]/clear[/cyan]         - Reset conversation history
  [cyan]/history[/cyan]       - View conversation message count
  [cyan]/help[/cyan]          - Show this help menu
  [cyan]/exit[/cyan]          - Exit TermiAgent""", title="Commands", border_style="cyan"))

    elif command == "/model":
        if not arg:
            console.print(f"Current Model: [bold green]{agent.provider.model_name}[/bold green]")
        else:
            agent.provider = UniversalLLMProvider(model_name=arg)
            console.print(f"[green]Switched model to [bold]{arg}[/bold][/green]")

    elif command == "/clear":
        agent.clear_history()
        console.print("[green]Conversation history cleared.[/green]")

    elif command == "/history":
        console.print(f"Current History Length: [bold cyan]{len(agent.messages)}[/bold cyan] messages.")

    else:
        console.print(f"[red]Unknown command: {command}[/red]. Type [cyan]/help[/cyan] for options.")

    return False


def _run_agent_turn(agent: TermiAgent, user_input: str):
    """Helper callback renderer for tool calls and thoughts."""

    def on_thought(thought: str):
        if thought.strip():
            console.print("\n[bold slate4]Agent Thought:[/bold slate4]")
            console.print(Markdown(thought))

    def on_tool_call(name: str, args: dict):
        args_str = ", ".join(f"{k}={repr(v)}" for k, v in args.items())
        console.print(f"\n[bold yellow]⚡ Tool Call:[/bold yellow] [cyan]{name}[/cyan]({args_str})")

    def on_tool_result(name: str, result: str):
        preview = result[:300] + "..." if len(result) > 300 else result
        console.print(f"[dim]↳ Result ({name}): {preview}[/dim]")

    with console.status("[bold green]Agent thinking & executing...", spinner="dots"):
        final_answer = agent.run_turn(
            user_input=user_input,
            on_thought=on_thought,
            on_tool_call=on_tool_call,
            on_tool_result=on_tool_result
        )

    if final_answer and not final_answer.startswith("Reached maximum turn"):
        console.print("\n[bold green]TermiAgent Response:[/bold green]")
        console.print(Markdown(final_answer))
        console.print()


if __name__ == "__main__":
    main()
