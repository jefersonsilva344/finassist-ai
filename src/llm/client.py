from openai import OpenAI


class LLMClient:

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:

        response = self.client.responses.create(
            model="gpt-5.6",
            instructions=system_prompt,
            input=user_message,
        )

        return response.output_text