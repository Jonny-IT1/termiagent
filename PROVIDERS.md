# 🔌 Complete LLM Provider Setup & Universal Model Catalog

This guide provides step-by-step instructions on how to get API keys, set environment variables, and launch **TermiAgent** with **EVERY model from EVERY manufacturer** (Google, OpenAI, Anthropic, DeepSeek, Mistral, Meta Llama, Qwen, Microsoft Phi, Cohere, Perplexity, MiniMax, Groq, Together, Fireworks, Ollama, vLLM, Jan, Kobold).

---

## ⚡ Dynamic Wildcard Resolution (100% Support for ALL Present & Future Models)

TermiAgent uses **Dynamic Provider-Model Wildcard Resolution**. This means you can specify **ANY model name** released by any manufacturer using the `provider/model-name` syntax, and TermiAgent will dynamically route it!

For example:
- `termiagent -m openai/gpt-4-0125-preview`
- `termiagent -m anthropic/claude-3-5-sonnet-20240620`
- `termiagent -m meta/llama-3.1-405b`
- `termiagent -m qwen/qwen2.5-coder-32b`
- `termiagent -m microsoft/phi-4`
- `termiagent -m ollama/custom-local-model`

---

## 📋 Table of Contents

1. [Google Gemini](#1-google-gemini)
2. [OpenAI](#2-openai)
3. [Anthropic Claude](#3-anthropic-claude)
4. [DeepSeek](#4-deepseek)
5. [Mistral AI (Le Chat & Codestral)](#5-mistral-ai-le-chat--codestral)
6. [Cohere](#6-cohere)
7. [Perplexity AI](#7-perplexity-ai)
8. [Together AI](#8-together-ai)
9. [Fireworks AI](#9-fireworks-ai)
10. [MiniMax](#10-minimax)
11. [Groq (Ultra-Fast Inference)](#11-groq-ultra-fast-inference)
12. [HuggingFace](#12-huggingface)
13. [Local Ollama (100% Offline)](#13-local-ollama-100-offline)
14. [Local LM Studio / vLLM / Jan / KoboldAI](#14-local-lm-studio--vllm--jan--koboldai)

---

## 1. Google Gemini

- **API Key Portal**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Environment Variable**: `GEMINI_API_KEY`

### Setup Commands:

```bash
# Linux / macOS
export GEMINI_API_KEY="your-gemini-key-here"

# Windows PowerShell
$env:GEMINI_API_KEY="your-gemini-key-here"
```

### Launch Commands:
```bash
termiagent -m gemini/latest            # Gemini 2.0 Flash (Default)
termiagent -m gemini/gemini-2.0-pro-exp # Gemini 2.0 Pro
termiagent -m gemini/gemini-1.5-pro     # Legacy Gemini 1.5 Pro
```

---

## 2. OpenAI

- **API Key Portal**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Environment Variable**: `OPENAI_API_KEY`

### Setup Commands:
```bash
export OPENAI_API_KEY="sk-..."
```

### Launch Commands:
```bash
termiagent -m openai/latest            # GPT-4o
termiagent -m openai/o3-mini           # Reasoning Model
termiagent -m openai/gpt-3.5-turbo     # Legacy GPT-3.5
```

---

## 3. Anthropic Claude

- **API Key Portal**: [Anthropic Console](https://console.anthropic.com/settings/keys)
- **Environment Variable**: `ANTHROPIC_API_KEY`

### Setup Commands:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Launch Commands:
```bash
termiagent -m anthropic/latest         # Claude 3.5 Sonnet
termiagent -m anthropic/claude-3-opus   # Claude 3 Opus
```

---

## 4. DeepSeek

- **API Key Portal**: [DeepSeek Platform](https://platform.deepseek.com/api_keys)
- **Environment Variable**: `DEEPSEEK_API_KEY`

### Setup Commands:
```bash
export DEEPSEEK_API_KEY="sk-..."
```

### Launch Commands:
```bash
termiagent -m deepseek/latest          # DeepSeek-V3 Chat
termiagent -m deepseek/deepseek-reasoner # DeepSeek-R1 Reasoning
```

---

## 5. Mistral AI (Le Chat & Codestral)

- **API Key Portal**: [Mistral AI Console](https://console.mistral.ai/api-keys/)
- **Environment Variable**: `MISTRAL_API_KEY`

### Setup Commands:
```bash
export MISTRAL_API_KEY="your-mistral-key"
```

### Launch Commands:
```bash
termiagent -m mistral/latest           # Codestral Latest
termiagent -m mistral/pixtral-large    # Pixtral Vision Model
```

---

## 6. Cohere

- **API Key Portal**: [Cohere Dashboard](https://dashboard.cohere.com/api-keys)
- **Environment Variable**: `COHERE_API_KEY`

### Setup Commands:
```bash
export COHERE_API_KEY="your-cohere-key"
```

### Launch Commands:
```bash
termiagent -m cohere/latest            # Command R+
```

---

## 7. Perplexity AI

- **API Key Portal**: [Perplexity API Settings](https://www.perplexity.ai/settings/api)
- **Environment Variable**: `PERPLEXITY_API_KEY`

### Setup Commands:
```bash
export PERPLEXITY_API_KEY="pplx-..."
```

### Launch Commands:
```bash
termiagent -m perplexity/latest        # Sonar Pro
termiagent -m perplexity/sonar-reasoning
```

---

## 8. Together AI

- **API Key Portal**: [Together AI Dashboard](https://api.together.ai/settings/api-keys)
- **Environment Variable**: `TOGETHER_API_KEY`

### Setup Commands:
```bash
export TOGETHER_API_KEY="your-together-key"
```

### Launch Commands:
```bash
termiagent -m together/latest         # Llama 3.3 70B
termiagent -m together/deepseek-r1
```

---

## 9. Fireworks AI

- **API Key Portal**: [Fireworks Account](https://fireworks.ai/account/api-keys)
- **Environment Variable**: `FIREWORKS_API_KEY`

### Setup Commands:
```bash
export FIREWORKS_API_KEY="fw-..."
```

### Launch Commands:
```bash
termiagent -m fireworks/latest        # DeepSeek R1
```

---

## 10. MiniMax

- **API Key Portal**: [MiniMax Platform](https://platform.minimaxi.com/user-center/basic-information/interface-key)
- **Environment Variable**: `MINIMAX_API_KEY`

### Setup Commands:
```bash
export MINIMAX_API_KEY="your-minimax-key"
```

### Launch Commands:
```bash
termiagent -m minimax/latest           # MiniMax Text-01
```

---

## 11. Groq (Ultra-Fast Inference)

- **API Key Portal**: [Groq Console](https://console.groq.com/keys)
- **Environment Variable**: `GROQ_API_KEY`

### Setup Commands:
```bash
export GROQ_API_KEY="gsk_..."
```

### Launch Commands:
```bash
termiagent -m groq/latest              # Llama 3.3 70B Versatile
termiagent -m groq/deepseek-r1-70b
```

---

## 12. HuggingFace

- **API Key Portal**: [Hugging Face Tokens](https://huggingface.co/settings/tokens)
- **Environment Variable**: `HF_TOKEN`

### Setup Commands:
```bash
export HF_TOKEN="hf_..."
```

### Launch Commands:
```bash
termiagent -m huggingface/latest
```

---

## 13. Local Ollama (100% Offline)

- **Website / Install**: [Ollama.com](https://ollama.com)
- **API Key Needed**: **NO** (Runs 100% locally on your computer)

### Setup Steps:
1. Install Ollama and pull your desired model:
   ```bash
   ollama pull qwen2.5-coder
   ```
2. Start TermiAgent:
   ```bash
   termiagent -m ollama/qwen2.5-coder
   ```

---

## 14. Local LM Studio / vLLM / Jan / KoboldAI

- **API Key Needed**: **NO**

### Setup Steps:
1. Start your local server (LM Studio, vLLM, or Jan) on port `1234` or `8000`.
2. Launch TermiAgent:
   ```bash
   termiagent -m lmstudio/latest
   # or for vLLM:
   termiagent -m vllm/latest
   ```

---

## 🔄 Switching Models Live in Chat

You don't need to restart TermiAgent to switch models! While in the interactive REPL chat, use the `/model` slash command:

```text
termiagent> /model mistral/codestral-latest
termiagent> /model ollama/llama3.3
termiagent> /model deepseek/deepseek-reasoner
```
