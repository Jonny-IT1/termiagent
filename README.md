<div align="center">

# 🤖 TermiAgent

### *Universal Terminal AI Coding Agent CLI*

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Package Manager: uv](https://img.shields.io/badge/managed_with-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

**TermiAgent** is an autonomous open-source AI coding agent that runs directly in your terminal. Inspect codebases, edit files, search code, process images, generate assets, and run shell commands — powered by **ANY** AI provider or local LLM (*Gemini, Claude, GPT, DeepSeek, Mistral, MiniMax, Cohere, Perplexity, Together AI, Fireworks, Groq, HuggingFace, Ollama, vLLM, LM Studio, Jan*).

[Features](#-key-features) • [1-Command Install](#-fast-1-command-installation-with-uv) • [Supported Models](#-supported-ai-model-providers) • [Python SDK](#-python-sdk-integration) • [License](#-license)

</div>

---

## ⚡ Key Features

- 🔌 **Universal Model & Provider Compatibility**: Connect seamlessly to Google Gemini, Anthropic Claude, OpenAI, DeepSeek, Mistral AI (Le Chat / Codestral), MiniMax, Cohere, Perplexity AI, Together AI, Fireworks AI, Groq, HuggingFace, or 100% offline local LLMs via Ollama, LM Studio, vLLM, Jan, and KoboldAI.
- 👁️ **Multimodal Vision Understanding**: Input screenshots, diagrams, or UI mockups for vision models (Claude 3.5 Vision, Gemini 2.0 Vision, GPT-4o Vision, Pixtral, LLaVA, Qwen2-VL).
- 🎨 **Image & Diagram Generation**: Native `generate_image` tool to produce diagrams, UI mockups, and visual assets directly from text prompts.
- 📜 **Full Modern & Legacy Model Catalog**: Support for both the newest flagship models (`gemini/latest`, `openai/latest`, `mistral/latest`) AND legacy versions (`gpt-3.5-turbo`, `claude-2.1`, `gemini-1.0-pro`, `abab5.5`).
- 🔀 **Live Model Switching**: Switch models on-the-fly mid-conversation using `/model <name>`.
- 🛠️ **Autonomous Agent Tools**:
  - 📖 `view_file`: Read file contents with precise line numbers.
  - ✏️ `write_file` & `edit_file`: Create files or apply targeted diff replacements.
  - 🔍 `search_codebase`: Fast regex and keyword code search.
  - 🖼️ `generate_image`: Produce visual diagrams and image assets.
  - ⚡ `run_shell_command`: Safely execute terminal commands (`pytest`, `git`, `python`, `npm`).
- ⚡ **Ultra-Fast & Modern**: Built with 100% Pure Python 3, `httpx`, `rich`, `prompt-toolkit`, and managed via `uv`.
- 🐍 **Python SDK Library**: Import `from termiagent import TermiAgent` to use the agent programmatically inside other Python projects.

---

## 🤖 Supported AI Model Catalog (Modern, Vision, Legacy & Local)

| Provider | Modern Models | Legacy Models | Vision Models |
| :--- | :--- | :--- | :--- |
| **Google Gemini** | `gemini/latest`, `gemini/gemini-2.0-flash`, `gemini/gemini-2.0-pro-exp` | `gemini/gemini-1.5-pro`, `gemini/gemini-1.0-pro` | `gemini/gemini-2.0-flash` |
| **OpenAI** | `openai/latest`, `openai/gpt-4o`, `openai/o1`, `openai/o3-mini` | `openai/gpt-4-turbo`, `openai/gpt-3.5-turbo` | `openai/gpt-4o` |
| **Anthropic** | `anthropic/latest`, `anthropic/claude-3-5-sonnet` | `anthropic/claude-3-opus`, `anthropic/claude-2.1` | `anthropic/claude-3-5-sonnet` |
| **Mistral AI** | `mistral/latest`, `mistral/codestral-latest`, `mistral/mistral-large` | `mistral/mistral-medium`, `mistral/mistral-small` | `mistral/pixtral-large` |
| **DeepSeek** | `deepseek/latest`, `deepseek/deepseek-chat` (V3), `deepseek/deepseek-reasoner` (R1) | `deepseek/deepseek-coder` | `deepseek/deepseek-vl` |
| **Cohere** | `cohere/latest`, `cohere/command-r-plus`, `cohere/command-r` | `cohere/command-light` | `cohere/command-r-plus` |
| **Perplexity AI** | `perplexity/latest`, `perplexity/sonar-pro`, `perplexity/sonar-reasoning` | `perplexity/sonar` | `perplexity/sonar-pro` |
| **Together / Fireworks** | `together/latest`, `together/llama3.3`, `fireworks/latest` | `together/mixtral` | `together/llama-vision` |
| **MiniMax** | `minimax/latest`, `minimax/minimax-text-01`, `minimax/abab6.5t` | `minimax/abab6.5`, `minimax/abab5.5` | `minimax/minimax-text-01` |
| **Groq (Fast)** | `groq/latest`, `groq/llama-3.3-70b`, `groq/deepseek-r1-70b` | `groq/mixtral-8x7b` | `groq/llama-3.3-70b` |
| **HuggingFace** | `huggingface/latest` | Custom HF endpoints | `huggingface/vision` |
| **Ollama / vLLM / Jan** | `ollama/latest`, `ollama/qwen2.5-coder`, `ollama/llama3.3`, `vllm/latest` | `ollama/mistral-small` | `ollama/llava`, `ollama/qwen2-vl` |

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
