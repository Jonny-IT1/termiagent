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

def test_legacy_and_vision_models():
    # Legacy GPT-3.5
    p_legacy = UniversalLLMProvider(model_name="openai/gpt-3.5-turbo")
    assert p_legacy.clean_model_name == "gpt-3.5-turbo"

    # Vision Pixtral Large
    p_vision = UniversalLLMProvider(model_name="mistral/pixtral-large")
    assert p_vision.clean_model_name == "pixtral-large-latest"

    # MiniMax Legacy
    p_minimax_legacy = UniversalLLMProvider(model_name="minimax/abab5.5")
    assert p_minimax_legacy.clean_model_name == "abab5.5-chat"

def test_image_base64_encoder(tmp_path):
    img_file = tmp_path / "test.png"
    img_file.write_bytes(b"fake_image_bytes")
    encoded = UniversalLLMProvider.encode_image_to_base64(img_file)
    assert encoded.startswith("data:image/png;base64,")
