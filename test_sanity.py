# test_sanity.py
import asyncio
import os

# Import the concrete agent you want to sanity‑check.
# Adjust the import if you want to test a different agent.
from agents.market_logic import MarketLogicAgent

SYSTEM_PROMPT = {
    "english": "You are a market logic analyst.",
    "arabic": "أنت محلل منطق السوق."
}


async def demo():

    agent = MarketLogicAgent()

    # Minimal test payload – you can replace the strings with anything.
    idea = "Invest in solar panel manufacturing in North Africa."
    dummy_api_key = "fake-key-for-testing"  # No real request will succeed.

    try:
        # The `analyze` coroutine is awaited directly.
        result = await agent.analyze(
            idea=idea,
            api_key=dummy_api_key,
            provider="google",  # or "google" if you have a Gemini key
            language="english",
        )
        print("\n✅  Agent returned a response:")
        print(result)
    except Exception as exc:
        # Expected when using a fake key – we just surface the error.
        print("\n⚠️  Expected error (invalid API key or network issue):")
        print(exc)


if __name__ == "__main__":
    # Run the async demo using asyncio.run (Python 3.7+)
    asyncio.run(demo())
