# Oracle AI - Smart Investment Assistant

## Project Overview

This project is an AI-driven "Smart Investment Committee" (Oracle AI) designed to analyze investment ideas and startup pitches from multiple strategic angles. It uses a "Diamond Structure" prompt engineering architecture to simulate specialized analysts.

The system features four main AI agents:
1.  **Market Logic Agent**: Analyzes market size, growth, supply/demand, and consumer behavior.
2.  **Financial Agent**: Evaluates unit economics, cost/revenue structures, and funding needs.
3.  **Competitive Agent**: Assesses barriers to entry, competitive moats, and replication risks.
4.  **Synthesizer Agent**: Compiles the three reports to issue a final verdict (Invest, Caution, Reject) with strategic advice.

The application backend is built in Python and provides two implementations: a FastAPI backend (`main.py`) and a Flask backend (`app_flask.py`). It supports both Google Gemini and OpenAI as LLM providers, leveraging asynchronous execution (`asyncio`) to run the initial three agent analyses concurrently.

## Building and Running

### Prerequisites
*   Python 3.10+

### Installation

You can install dependencies using standard `pip` or the modern `uv` package manager.

**Using `uv` (Recommended)**:
```bash
uv sync
```

**Using `pip`**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```



### Running the Application

There are two entry points for the application depending on the framework you choose to run.

**1. FastAPI (Recommended / Default)**
Run the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The application will be accessible at `http://localhost:8000`.


## Development Conventions

*   **Architecture**: 
    *   Backend routes are defined in `main.py` (FastAPI)
    *   Agent logic is encapsulated in the `agents/` directory. All agents inherit from a `BaseAgent` class located in `agents/base.py`.
    *   Configuration for LLM models (Google vs. OpenAI, model tiers) is handled in `agents/config.py`.
*   **Asynchronous Processing**: The application relies heavily on `asyncio` to execute the Market, Financial, and Competitive analyses concurrently, reducing overall wait times before the Synthesizer agent compiles the final report.
*   **Frontend**: The UI is built using HTML templates (`templates/index.html`) and styled with Tailwind CSS (`static/style.css`).
*   **Language & Localization**: The codebase is written in English, but the system is designed to handle user input and generate responses primarily in Arabic, as indicated by default parameters (`language="arabic"`) and the Arabic `README.md`.
