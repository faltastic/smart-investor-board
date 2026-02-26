import google.generativeai as genai

# from google.generativeai.types import GenerationConfig
from openai import AsyncOpenAI

from .config import MODELS


class BaseAgent:

    def __init__(self, model_level: str, system_prompt: dict):
        self.model_level = model_level
        self.system_prompt = system_prompt
        self._openai_client: AsyncOpenAI | None = None
        self._gemini_model_cache: dict[str, genai.GenerativeModel] = {}

    async def _get_openai_client(self, api_key: str) -> AsyncOpenAI:
        if self._openai_client is None:
            self._openai_client = AsyncOpenAI(api_key=api_key)
        return self._openai_client

    async def _get_gemini_model(
        self, api_key: str, model_name: str
    ) -> genai.GenerativeModel:
        genai.configure(api_key=api_key)

        if model_name not in self._gemini_model_cache:
            self._gemini_model_cache[model_name] = genai.GenerativeModel(model_name)
        return self._gemini_model_cache[model_name]

    async def analyze(
        self,
        idea: str,
        api_key: str,
        provider: str = "google",
        language: str = "arabic",
    ) -> str:

        model_name = MODELS.get(provider, MODELS["openai"]).get(self.model_level)
        if not model_name:
            raise ValueError(
                f"Model level '{self.model_level}' not defined for provider '{provider}'."
            )

        if provider.lower() == "google":
            try:
                gemini_model = await self._get_gemini_model(api_key, model_name)

                response = await gemini_model.generate_content_async(
                    contents=[idea],
                    # generation_config=GenerateContentConfig(
                    #     system_instruction=self.system_prompt.get(
                    #         language, self.system_prompt["arabic"]
                    #     )
                    # ),
                )

                return response.text
            except Exception as exc:
                raise RuntimeError(f"Gemini request failed: {exc}") from exc

        else:
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
                )
                if not response.choices:
                    raise RuntimeError("OpenAI returned an empty choices list.")
                return response.choices[0].message.content
            except Exception as exc:
                raise RuntimeError(f"OpenAI request failed: {exc}") from exc
