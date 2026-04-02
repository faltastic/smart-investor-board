import asyncio
import webbrowser
from flask import Flask, render_template, request, jsonify
from agents import MarketLogicAgent, FinancialAgent, CompetitiveAgent, SynthesizerAgent

app = Flask(__name__)

market_agent = MarketLogicAgent()
financial_agent = FinancialAgent()
competitive_agent = CompetitiveAgent()
synthesizer = SynthesizerAgent()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    idea = data.get('idea', '')
    api_key = data.get('api_key', '')
    provider = data.get("provider", "google")
    language = data.get("language", "arabic")

    if not idea or not api_key:
        return jsonify({'error': 'الرجاء إدخال الفكرة ومفتاح API'}), 400

    try:
        result = asyncio.run(run_analysis(idea, api_key, provider, language))
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


async def run_analysis(idea: str, api_key: str, provider: str, language: str) -> dict:
    market_task = market_agent.analyze(idea, api_key, provider, language)
    financial_task = financial_agent.analyze(idea, api_key, provider, language)
    competitive_task = competitive_agent.analyze(idea, api_key, provider, language)

    market_result, financial_result, competitive_result = await asyncio.gather(
        market_task,
        financial_task,
        competitive_task
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
        'market_analysis': market_result,
        'financial_analysis': financial_result,
        'competitive_analysis': competitive_result,
        'final_verdict': final_verdict
    }


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    app.run(debug=True, use_reloader=False)
