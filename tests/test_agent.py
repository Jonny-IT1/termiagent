from termiagent.agent import TermiAgent
from termiagent.providers.base import BaseLLMProvider

class MockLLMProvider(BaseLLMProvider):
    def __init__(self, responses):
        self.responses = responses
        self.idx = 0

    def chat_complete(self, messages, tools=None):
        if self.idx < len(self.responses):
            res = self.responses[self.idx]
            self.idx += 1
            return res
        return {"content": "Done", "tool_calls": None, "model": "mock"}


def test_agent_tool_loop(tmp_path):
    f_path = tmp_path / "test.txt"
    f_path.write_text("hello mock", encoding="utf-8")

    mock_responses = [
        {
            "content": "Reading file now.",
            "tool_calls": [
                {
                    "id": "call_1",
                    "name": "view_file",
                    "arguments": {"file_path": str(f_path)}
                }
            ],
            "model": "mock"
        },
        {
            "content": "I have read the file successfully.",
            "tool_calls": None,
            "model": "mock"
        }
    ]

    mock_provider = MockLLMProvider(mock_responses)
    agent = TermiAgent(provider=mock_provider, work_dir=str(tmp_path))

    final_resp = agent.run_turn("Please view test.txt")
    assert "read the file successfully" in final_resp
    assert len(agent.messages) > 3
