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

    market_result, financial_result, competitive_result = await asyncio.gather(
        market_task,
        financial_task,
        competitive_task,
    )

    final_verdict = await synthesizer.synthesize(
        idea=idea,
        market_analysis=market_result,
        financial_analysis=financial_result,
        competitive_analysis=competitive_result,
        api_key=api_key,
        provider=provider,
        language=language,
    )

    return {
        "market_analysis": market_result,
        "financial_analysis": financial_result,
        "competitive_analysis": competitive_result,
        "final_verdict": final_verdict,
    }
