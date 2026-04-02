# Oracle AI - Smart Investment Assistant

An AI-driven "Smart Investment Committee" that analyzes startup pitches and investment ideas. It uses multiple AI agents (Market, Financial, Competitive, and Synthesizer) running concurrently to evaluate an idea from multiple strategic angles and issue a final verdict (Invest, Caution, Reject).

## Setup & Run

**Prerequisites:** Python 3.10+

1. **Install dependencies:**
   ```bash
   uv sync
   # OR: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```

2. **Run the server (FastAPI):**
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the application:** Open `http://localhost:8000` in your browser.

## Features
* **Multi-LLM Support:** Compatible with Google Gemini and OpenAI.
* **Fast Analysis:** Asynchronous execution (`asyncio`) allows the Market, Financial, and Competitive agents to run concurrently.
* **Modern Stack:** Built with a FastAPI backend and a clean HTML/Tailwind CSS frontend.
* **Localization:** Primarily designed and configured for Arabic language interactions.