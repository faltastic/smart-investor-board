from .base import BaseAgent
from .config import MODELS

SYSTEM_PROMPT = {
    "english": """You are the general partner and the ultimate investment decision-maker.

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
(Practical advice for the investor)""",
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


class SynthesizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_level="high", system_prompt=SYSTEM_PROMPT)

    async def synthesize(
        self,
        idea: str,
        market_analysis: dict,
        financial_analysis: dict,
        competitive_analysis: dict,
        api_key: str,
        provider: str,
        language: str,
    ) -> dict:
        market_text = market_analysis["text"]
        financial_text = financial_analysis["text"]
        competitive_text = competitive_analysis["text"]

        if language == "english":
            user_message = f"""Investment Idea:
{idea}

---

Market Logic Analysis:
{market_text}

---

Financial Sustainability Analysis:
{financial_text}

---

Competitive Resilience Analysis:
{competitive_text}

---

Based on the three analyses above, provide your final investment judgment and strategic advice."""
        else:
            user_message = f"""الفكرة الاستثمارية:
{idea}

---

تحليل منطق السوق:
{market_text}

---

تحليل الاستدامة المالية:
{financial_text}

---

تحليل المتانة التنافسية:
{competitive_text}

---

بناءً على التحليلات الثلاثة أعلاه، قدم حكمك الاستثماري النهائي والاستشارة الاستراتيجية."""

        return await self.analyze(
            idea=user_message,
            api_key=api_key,
            provider=provider,
            language=language,
            temperature=0.5,
            max_tokens=5000,
        )
