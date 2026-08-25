<div align="center">

# 🤖 TermiAgent

### *Universal Terminal AI Coding Agent CLI*

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Package Manager: uv](https://img.shields.io/badge/managed_with-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

**TermiAgent** is an autonomous open-source AI coding agent that runs directly in your terminal. Inspect codebases, edit files, search code, and run shell commands — powered by **ANY** AI provider or local LLM (*Gemini, Claude 3.5, GPT-4o, DeepSeek, Mistral Le Chat, MiniMax, Ollama, OpenRouter, Groq*).

[Features](#-key-features) • [1-Command Install](#-fast-1-command-installation-with-uv) • [Supported Models](#-supported-ai-model-providers) • [Python SDK](#-python-sdk-integration) • [License](#-license)

</div>

---

## ⚡ Key Features

- 🔌 **Universal Model Compatibility**: Connect seamlessly to Google Gemini, Anthropic Claude, OpenAI, DeepSeek, Mistral AI (Le Chat / Codestral), MiniMax, OpenRouter, Groq, or 100% offline local LLMs via Ollama & LM Studio.
- 🔀 **Live Model Switching**: Switch models on-the-fly mid-conversation using `/model <name>`.
- 🛠️ **Autonomous Agent Tools**:
  - 📖 `view_file`: Read file contents with precise line numbers.
  - ✏️ `write_file` & `edit_file`: Create files or apply targeted diff replacements.
  - 🔍 `search_codebase`: Fast regex and keyword code search.
  - ⚡ `run_shell_command`: Safely execute terminal commands (`pytest`, `git`, `python`, `npm`).
- ⚡ **Ultra-Fast & Modern**: Built with 100% Pure Python 3, `httpx`, `rich`, `prompt-toolkit`, and managed via `uv`.
- 🐍 **Python SDK Library**: Import `from termiagent import TermiAgent` to use the agent programmatically inside other Python projects.

---

## 🏗️ Architecture & How It Works

```
                                  ┌───────────────────────────┐
                                  │      TermiAgent CLI       │
                                  │ (Rich REPL + Slash Cmds)  │
                                  └─────────────┬─────────────┘
                                                │
                                  ┌─────────────▼─────────────┐
                                  │   Autonomous ReAct Engine │
                                  └─────────────┬─────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 │                                                             │
   ┌─────────────▼─────────────┐                                 ┌─────────────▼─────────────┐
   │ Universal LLM Provider    │                                 │   Agent Tools Registry    │
   │ (OpenAI/Gemini/DeepSeek/  │                                 │ (FileSystem & Shell Exec) │
   │ Mistral/MiniMax/Ollama)   │                                 └───────────────────────────┘
   └───────────────────────────┘
```

---

## 🚀 Fast 1-Command Installation (with `uv`)

### Linux / macOS

```bash
curl -LsSf https://raw.githubusercontent.com/Jonny-IT1/termiagent/main/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/Jonny-IT1/termiagent/main/install.ps1 | iex"
```

### Standard PyPI / Local Installation

```bash
uv pip install -e .
# or standard pip:
pip install termiagent
```

---

## 🤖 Supported AI Model Providers

TermiAgent supports any OpenAI-compatible API endpoint or native provider. Specify the model using `--model provider/model-name`:

| Provider | Example Command / Model String | Environment Variable |
| :--- | :--- | :--- |
| **Google Gemini** | `termiagent -m gemini/gemini-2.0-flash` | `GEMINI_API_KEY` |
| **Mistral AI (Le Chat)** | `termiagent -m mistral/codestral-latest` | `MISTRAL_API_KEY` |
| **MiniMax** | `termiagent -m minimax/minimax-text-01` | `MINIMAX_API_KEY` |
| **OpenAI** | `termiagent -m openai/gpt-4o` | `OPENAI_API_KEY` |
| **Anthropic** | `termiagent -m anthropic/claude-3-5-sonnet` | `ANTHROPIC_API_KEY` |
| **DeepSeek** | `termiagent -m deepseek/deepseek-chat` | `DEEPSEEK_API_KEY` |
| **Local Ollama** | `termiagent -m ollama/qwen2.5-coder` | *None (Runs locally)* |
| **OpenRouter** | `termiagent -m openrouter/anthropic/claude-3.5-sonnet` | `OPENROUTER_API_KEY` |
| **Groq** | `termiagent -m groq/llama-3.3-70b-versatile` | `GROQ_API_KEY` |

---

## 💻 CLI & REPL Usage

### Interactive Chat Mode

Start TermiAgent in your project directory:

```bash
termiagent
```

### One-Shot Command Mode

Run a single instruction directly from the command line:

```bash
termiagent -p "Check why tests in tests/ are failing and fix them."
```

### Interactive Slash Commands

Inside the terminal REPL chat, use slash commands:
- `/model <name>`: Switch active LLM model live (e.g. `/model ollama/llama3.3`).
- `/clear`: Reset conversation context history.
- `/history`: Show current conversation message count.
- `/help`: Display slash command options.
- `/exit`: Exit TermiAgent.

---

## 🐍 Python SDK Integration (Use in Other Projects)

You can import `TermiAgent` into your own Python applications, AI frameworks, or agent workflows:

```python
from termiagent import TermiAgent, UniversalLLMProvider

# 1. Initialize custom provider
provider = UniversalLLMProvider(model_name="gemini/gemini-2.0-flash")

# 2. Instantiate agent in target directory
agent = TermiAgent(provider=provider, work_dir="./my_project")

# 3. Execute turn programmatically
response = agent.run_turn("Refactor main.py to use async functions")

print("Agent Response:", response)
```

---

## 🧪 Testing & Verification

Run the full automated test suite using `pytest`:

```bash
uv run pytest
```

---

## 📄 License & Legal Disclaimer

This project is licensed under the **MIT License**.

> **Disclaimer:** TermiAgent is provided "as is", without warranty of any kind, express or implied. The authors and contributors shall not be held liable for any damages, code changes, or shell commands executed during use. Always review generated code and command executions.
