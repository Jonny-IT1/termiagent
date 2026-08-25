import termiagent
from termiagent import TermiAgent, UniversalLLMProvider

def test_sdk_imports():
    assert hasattr(termiagent, "TermiAgent")
    assert hasattr(termiagent, "UniversalLLMProvider")

def test_sdk_instantiation(tmp_path):
    agent = TermiAgent(work_dir=str(tmp_path))
    assert agent.work_dir.resolve() == tmp_path.resolve()
    assert len(agent.registry.tools) >= 5
