from src.models.schemas import AgentResponse, MessageRole, ToolCallRecord

def test_tool_call_record_defaults():
    record = ToolCallRecord(tool_name="web_search", tool_input={"query": "test"})
    assert record.success is True
    assert record.tool_output is None

def test_agent_response_defaults():
    response = AgentResponse(content="merhaba")
    assert response.success is True
    assert response.tool_calls == []

def test_message_role_values():
    assert MessageRole.USER == "user"
    assert MessageRole.ASSISTANT == "assistant"
