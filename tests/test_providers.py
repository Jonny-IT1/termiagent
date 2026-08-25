from termiagent.providers.universal import UniversalLLMProvider

def test_universal_provider_init():
    provider = UniversalLLMProvider(model_name="gemini/gemini-2.0-flash")
    assert provider.provider_prefix == "gemini"
    assert provider.clean_model_name == "gemini-2.0-flash"

def test_provider_parse_model_name():
    p = UniversalLLMProvider(model_name="ollama/qwen2.5-coder")
    assert p.provider_prefix == "ollama"
    assert p.clean_model_name == "qwen2.5-coder:latest"
    assert "localhost:11434" in p.base_url

def test_dynamic_wildcard_and_all_vendor_models():
    # Dynamic arbitrary custom model release
    p_custom = UniversalLLMProvider(model_name="openai/custom-gpt-5-future")
    assert p_custom.provider_prefix == "openai"
    assert p_custom.clean_model_name == "custom-gpt-5-future"

    # Meta Llama (routed via Together AI)
    p_llama = UniversalLLMProvider(model_name="meta/llama-3.1-405b")
    assert p_llama.provider_prefix == "together"
    assert p_llama.clean_model_name == "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"

    # Qwen (routed via Together AI)
    p_qwen = UniversalLLMProvider(model_name="qwen/qwen2.5-coder-32b")
    assert p_qwen.provider_prefix == "together"
    assert p_qwen.clean_model_name == "Qwen/Qwen2.5-Coder-32B-Instruct"

    # Microsoft Phi
    p_phi = UniversalLLMProvider(model_name="microsoft/phi-4")
    assert p_phi.provider_prefix == "together"
    assert p_phi.clean_model_name == "microsoft/phi-4"
