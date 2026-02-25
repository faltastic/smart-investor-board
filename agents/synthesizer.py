from openai import AsyncOpenAI
from google import genai
from google.genai import types
from .config import MODELS


SYSTEM_PROMPT = {
    "english": """"You are the general partner and the ultimate investment decision-maker.

Your role: To receive analyses from three expert analysts (market logic, financial sustainability, competitive resilience) and integrate them into a comprehensive final judgment.

When making the decision:

1. Weigh the conflicting arguments from the three analysts

2. Identify points of agreement and disagreement between the analyses

3. Assess the overall risk versus opportunity

4. Make a clear investment judgment

Your response should be structured as follows:
## Summary of Analyses
(A brief summary of what each analyst said)

## Points of Agreement
(Where the analysts agreed)

## Points of Disagreement
(Where the opinions differed and how to balance them)

## Final Investment Judgment
Choose one: [Invest aggressively | Invest cautiously | Watch and wait | Don't invest]

## Overall Rating
(From 1-10 with justification)

## Strategic Advice
(Practical advice for the investor) """,
    "arabic": """أنت الشريك العام وصانع القرار الاستثماري النهائي.

دورك: استلام تحليلات ثلاثة محللين متخصصين (منطق السوق، الاستدامة المالية، المتانة التنافسية) ودمجها في حكم نهائي شامل.

عند اتخاذ القرار:
1. وازن بين الحجج المتناقضة من المحللين الثلاثة
2. حدد أوجه التوافق والاختلاف بين التحليلات
3. قيّم المخاطر الإجمالية مقابل الفرص
4. أصدر حكماً استثمارياً واضحاً

هيكل ردك يجب أن يكون:
## ملخص التحليلات
(ملخص موجز لما قاله كل محلل)

## نقاط التوافق
(أين اتفق المحللون)

## نقاط الاختلاف
(أين اختلفت الآراء وكيف توازن بينها)

## الحكم الاستثماري النهائي
اختر واحداً: [استثمر بقوة | استثمر بحذر | راقب وانتظر | لا تستثمر]

## التقييم الإجمالي
(من 1-10 مع تبرير)

## الاستشارة الاستراتيجية
(نصائح عملية للمستثمر)""",
}


class SynthesizerAgent:
    def __init__(self):
        self.model_level = "high"
        self.system_prompt = SYSTEM_PROMPT

    async def synthesize(
        self,
        idea: str,
        market_analysis: str,
        financial_analysis: str,
        competitive_analysis: str,
        api_key: str,
        provider: str = "openai",
        language: str = "arabic",
    ) -> str:
        if language == "english":
            user_message = f"""Investment Idea:
{idea}

---

Market Logic Analysis:
{market_analysis}

---

Financial Sustainability Analysis:
{financial_analysis}

---

Competitive Resilience Analysis:
{competitive_analysis}

---

Based on the three analyses above, provide your final investment judgment and strategic advice."""
        else:
            user_message = f"""الفكرة الاستثمارية:
{idea}

---

تحليل منطق السوق:
{market_analysis}

---

تحليل الاستدامة المالية:
{financial_analysis}

---

تحليل المتانة التنافسية:
{competitive_analysis}

---

بناءً على التحليلات الثلاثة أعلاه، قدم حكمك الاستثماري النهائي والاستشارة الاستراتيجية."""

        model_name = MODELS.get(provider, MODELS["openai"]).get(self.model_level)
        system_instruction = self.system_prompt.get(language, self.system_prompt["arabic"])

        if provider == "google":
            client = genai.Client(api_key=api_key)

            response = await client.aio.models.generate_content(
                model=model_name,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.5,
                    max_output_tokens=2000,
                ),
            )
            return response.text
        else:
            client = AsyncOpenAI(api_key=api_key)

            response = await client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.5,
                max_tokens=2000,
            )

            return response.choices[0].message.content
