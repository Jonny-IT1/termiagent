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
