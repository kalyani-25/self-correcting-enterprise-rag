import os
from langchain_openai import ChatOpenAI
from app.config import get_settings


class LLMClient:
    def __init__(self):
        settings = get_settings()
        self.use_mock = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
        self.client = None if self.use_mock else ChatOpenAI(
            model=settings.llm_model,
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def invoke(self, prompt: str) -> str:
        if self.use_mock:
            return self._mock_response(prompt)

        response = self.client.invoke(prompt)
        return response.content

    def _mock_response(self, prompt: str) -> str:
        lower = prompt.lower()

        if "node_list" in lower:
            return '{"node_list": ["overview", "architecture"]}'

        if "grade" in lower and "improved_query" in lower:
            return '{"grade": "yes", "reason": "Mock answer is sufficient.", "improved_query": ""}'

        return "CloudShop Lite is a cloud-native microservices platform with AI-Ops automation and MCP-enabled system intelligence built on AWS."