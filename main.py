import asyncio
import webbrowser
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import your existing agents
from agents import MarketLogicAgent, FinancialAgent, CompetitiveAgent, SynthesizerAgent

app = FastAPI()

# -------------------------------------------------
# Static files & Jinja2 templates (same layout as Flask)
# -------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# -------------------------------------------------
# Agent instances – identical to the Flask version
# -------------------------------------------------
market_agent = MarketLogicAgent()
financial_agent = FinancialAgent()
competitive_agent = CompetitiveAgent()
synthesizer = SynthesizerAgent()


# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(request: Request):
    """
    Expected JSON payload (same shape as the Flask version):
    {
        "idea": "...",
        "api_key": "...",
        "provider": "google",   # optional, defaults to "google"
        "language": "arabic"    # optional, defaults to "arabic"
    }
    """
    data = await request.json()
    idea = data.get("idea", "")
    api_key = data.get("api_key", "")
    provider = data.get("provider", "google")
    language = data.get("language", "arabic")

    if not idea or not api_key:
        raise HTTPException(
            status_code=400, detail="Please provide both `idea` and `api_key`."
        )

    # Run the three analyses concurrently, just like the Flask version
    try:
        result = await run_analysis(idea, api_key, provider, language)
        return JSONResponse(content=result)
    except Exception as exc:
        # Propagate as a 500 error with the exception message
        raise HTTPException(status_code=500, detail=str(exc))


# -------------------------------------------------
# Core async helper (unchanged from Flask version)
# -------------------------------------------------
async def run_analysis(idea: str, api_key: str, provider: str, language: str) -> dict:
    market_task = market_agent.analyze(idea, api_key, provider, language)
    financial_task = financial_agent.analyze(idea, api_key, provider, language)
    competitive_task = competitive_agent.analyze(idea, api_key, provider, language)

    market_result_dict, financial_result_dict, competitive_result_dict = await asyncio.gather(
        market_task,
        financial_task,
        competitive_task,
    )

    market_result_text = market_result_dict["text"]
    financial_result_text = financial_result_dict["text"]
    competitive_result_text = competitive_result_dict["text"]

    final_verdict_dict = await synthesizer.synthesize(
        idea=idea,
        market_analysis=market_result_dict,
        financial_analysis=financial_result_dict,
        competitive_analysis=competitive_result_dict,
        api_key=api_key,
        provider=provider,
        language=language,
    )
    final_verdict_text = final_verdict_dict["text"]

    # Aggregate usage metadata
    total_prompt_tokens = (
        market_result_dict["usage_metadata"]["prompt_token_count"] +
        financial_result_dict["usage_metadata"]["prompt_token_count"] +
        competitive_result_dict["usage_metadata"]["prompt_token_count"] +
        final_verdict_dict["usage_metadata"]["prompt_token_count"]
    )
    total_completion_tokens = (
        market_result_dict["usage_metadata"]["candidates_token_count"] +
        financial_result_dict["usage_metadata"]["candidates_token_count"] +
        competitive_result_dict["usage_metadata"]["candidates_token_count"] +
        final_verdict_dict["usage_metadata"]["candidates_token_count"]
    )

    # Assuming all agents use the same provider and model_level for simplicity in reporting
    # You might want to refine this if different agents use different models
    aggregated_usage_metadata = {
        "provider": provider,
        "model_level": market_result_dict["usage_metadata"]["model_level"], # Or from any other agent
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
    }

    return {
        "market_analysis": market_result_text,
        "financial_analysis": financial_result_text,
        "competitive_analysis": competitive_result_text,
        "final_verdict": final_verdict_text,
        "usage_metadata": aggregated_usage_metadata,
    }
