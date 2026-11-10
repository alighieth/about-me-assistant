import os

import requests
import json

from app.reponse_models import AIResponseModel
from openai import AsyncOpenAI, OpenAI

class LLM():
    def __init__(self, model_name: str = "nvidia/nemotron-3-ultra-550b-a55b:free"):
        self.model_name = model_name
        self.api_key = os.getenv("OPEN_ROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1"
        self.async_client = AsyncOpenAI(base_url=self.api_url, api_key=self.api_key)
        self.client = OpenAI(base_url=self.api_url, api_key=self.api_key)

    def send_request(self, prompt: str, with_reasoning: bool = False) -> dict:
        response =  self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                    ],
            extra_body={"reasoning": {"enabled": with_reasoning}}
            )
        
        return response

    async def send_stream(self, prompt: str, with_reasoning: bool = False):
        stream = await self.async_client.responses.create(
            model=self.model_name,
            input=[
                {
                    "role": "user",
                    "content": "Say 'double bubble bath' 3 times fast only in 1 sentence.",
                },
            ],
            stream=True,
            extra_body={"reasoning": {"enabled": with_reasoning}, "temperature": 0}
        )

        return stream  # Return the stream object for further processing
        
    def generate_response(self, prompt: str) -> AIResponseModel:
        response = self.send_request(prompt)

        # Extract message and usage using dot notation attributes
        message = response.choices[0].message
        usage = response.usage

        # Safely extract OpenRouter cost (if present on usage, or default to 0.0)
        cost = getattr(usage, "cost", 0.0)

        return AIResponseModel(
            inputTokenUsage=usage.prompt_tokens,
            outputTokenUsage=usage.completion_tokens,
            totalTokenUsage=usage.total_tokens,
            cost=cost,
            model=response.model,
            response=message.content or "",
        )
