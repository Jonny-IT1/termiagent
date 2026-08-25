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

def test_new_cloud_and_local_providers():
    # Cohere
    p_cohere = UniversalLLMProvider(model_name="cohere/latest")
    assert p_cohere.provider_prefix == "cohere"
    assert "cohere.com" in p_cohere.base_url

    # Perplexity
    p_perp = UniversalLLMProvider(model_name="perplexity/sonar-pro")
    assert p_perp.provider_prefix == "perplexity"
    assert "perplexity.ai" in p_perp.base_url

    # Together AI
    p_together = UniversalLLMProvider(model_name="together/latest")
    assert p_together.provider_prefix == "together"
    assert "together.xyz" in p_together.base_url

    # vLLM local
    p_vllm = UniversalLLMProvider(model_name="vllm/latest")
    assert p_vllm.provider_prefix == "vllm"
    assert "localhost:8000" in p_vllm.base_url
