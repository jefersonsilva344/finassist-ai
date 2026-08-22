from unittest.mock import Mock, patch

from src.llm.client import LLMClient


def test_llm_client_initializes_openai_client():
    with patch("src.llm.client.OpenAI") as openai_mock:
        client = LLMClient(api_key="test-key")

    openai_mock.assert_called_once_with(api_key="test-key")
    assert client.client is openai_mock.return_value


def test_llm_client_generate_calls_openai_responses_api():
    with patch("src.llm.client.OpenAI") as openai_mock:
        response = Mock()
        response.output_text = "Resposta gerada pela IA"

        openai_mock.return_value.responses.create.return_value = response

        client = LLMClient(api_key="test-key")

        result = client.generate(
            system_prompt="Você é um assistente financeiro.",
            user_message="Quanto devo economizar por mês?",
        )

    openai_mock.return_value.responses.create.assert_called_once_with(
        model="gpt-5.6",
        instructions="Você é um assistente financeiro.",
        input="Quanto devo economizar por mês?",
    )

    assert result == "Resposta gerada pela IA"