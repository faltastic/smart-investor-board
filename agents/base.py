from google.genai import Client
from google.genai.types import GenerateContentConfig
from openai import AsyncOpenAI

from .config import MODELS


class BaseAgent:

    def __init__(self, model_level: str, system_prompt: dict):
        self.model_level = model_level
        self.system_prompt = system_prompt
        self._openai_client: AsyncOpenAI | None = None
        self._gemini_client: Client | None = None

    async def _get_openai_client(self, api_key: str) -> AsyncOpenAI:
        if self._openai_client is None:
            self._openai_client = AsyncOpenAI(api_key=api_key)
        return self._openai_client

    async def _get_gemini_client(self, api_key: str) -> Client:
        if self._gemini_client is None:
            self._gemini_client = Client(api_key=api_key)
        return self._gemini_client

    async def analyze(
        self,
        idea: str,
        api_key: str,
        provider: str,
        language: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> dict:  # Changed return type hint to dict

        model_name = MODELS.get(provider, MODELS["openai"]).get(self.model_level)
        if not model_name:
            raise ValueError(
                f"Model level '{self.model_level}' not defined for provider '{provider}'."
            )

        if provider.lower() == "google":
            try:
                system_prompt_content = self.system_prompt.get(
                    language, self.system_prompt["arabic"]
                )
                gemini_client = await self._get_gemini_client(api_key)

                generate_content_config = GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    system_instruction=system_prompt_content,
                )

                response = await gemini_client.aio.models.generate_content(
                    model=model_name,
                    contents=[idea],
                    config=generate_content_config,
                )
                return {
                    "text": response.text,
                    "usage_metadata": {
                        "prompt_token_count": (
                            response.usage_metadata.prompt_token_count
                            if response.usage_metadata
                            else 0
                        ),
                        "candidates_token_count": (
                            response.usage_metadata.candidates_token_count
                            if response.usage_metadata
                            else 0
                        ),
                        "model_level": self.model_level,
                        "provider": provider,
                    },
                }
            except Exception as exc:
                raise RuntimeError(f"Gemini request failed: {exc}") from exc

        elif provider.lower() == "openai":
            try:
                client = await self._get_openai_client(api_key)

                response = await client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": self.system_prompt.get(
                                language, self.system_prompt["arabic"]
                            ),
                        },
                        {"role": "user", "content": idea},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                # print(f"DEBUG: OpenAI Full Response: {response.model_dump()}")
                if not response.choices:
                    raise RuntimeError("OpenAI returned an empty choices list.")

                # OpenAI API response structure for token usage
                prompt_tokens = response.usage.prompt_tokens if response.usage else 0
                completion_tokens = (
                    response.usage.completion_tokens if response.usage else 0
                )

                return {
                    "text": response.choices[0].message.content,
                    "usage_metadata": {
                        "prompt_token_count": prompt_tokens,
                        "candidates_token_count": completion_tokens,
                        "model_level": self.model_level,
                        "provider": provider,
                    },
                }
            except Exception as exc:
                raise RuntimeError(f"OpenAI request failed: {exc}") from exc
