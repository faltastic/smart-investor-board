from openai import AsyncOpenAI
from google import genai
from google.genai import types
from .config import MODELS

class BaseAgent:
    def __init__(self, model_level: str, system_prompt: str):
        self.model_level = model_level
        self.system_prompt = system_prompt
    
    async def analyze(self, idea: str, api_key: str, provider: str = 'openai', language: str = 'arabic') -> str:
        model_name = MODELS.get(provider, MODELS['openai']).get(self.model_level)
        
        if provider == 'google':
            client = genai.Client(api_key=api_key)
            
            response = await client.aio.models.generate_content(
                model=model_name,
                contents=idea,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt.get(language, self.system_prompt['arabic']),
                )
            )
            
            return response.text
        else:
            client = AsyncOpenAI(api_key=api_key)
            
            response = await client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt.get(language, self.system_prompt['arabic'])},
                    {"role": "user", "content": idea}
                ]
            )
            
            return response.choices[0].message.content
