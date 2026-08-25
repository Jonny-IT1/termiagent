from termiagent.providers.universal import UniversalLLMProvider

def test_universal_provider_init():
    provider = UniversalLLMProvider(model_name="gemini/gemini-2.0-flash")
    assert provider.provider_prefix == "gemini"
    assert provider.clean_model_name == "gemini-2.0-flash"

def test_provider_parse_model_name():
    p = UniversalLLMProvider(model_name="ollama/qwen2.5-coder")
    assert p.provider_prefix == "ollama"
    assert p.clean_model_name == "qwen2.5-coder"
    assert "localhost:11434" in p.base_url

def test_mistral_and_minimax_provider():
    p_mistral = UniversalLLMProvider(model_name="mistral/codestral-latest")
    assert p_mistral.provider_prefix == "mistral"
    assert "api.mistral.ai" in p_mistral.base_url

    p_minimax = UniversalLLMProvider(model_name="minimax/minimax-text-01")
    assert p_minimax.provider_prefix == "minimax"
    assert "api.minimaxi.chat" in p_minimax.base_url
