import os
import time

from dotenv import load_dotenv

try:
    from google import genai
except ImportError:  # pragma: no cover - handled at runtime
    genai = None

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
client = None

if genai is not None and API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:  # pragma: no cover - defensive runtime guard
        client = None


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
You are FitBuddy, a general wellness assistant.

Give one short, age-appropriate nutrition and recovery tip
related to this fitness goal:

Goal: {goal}

Requirements:
- Focus on balanced meals, hydration, sleep, and recovery.
- Do not recommend restrictive diets.
- Do not recommend calorie counting.
- Do not recommend rapid weight changes.
- Keep the answer simple and practical.
- Give only one useful tip.
"""

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
    ]

    if client is None:
        if "flex" in goal.lower():
            return (
                "For flexibility, prioritize balanced meals with protein, fruit, vegetables, and whole grains; stay well-hydrated; and recover with gentle stretching, sleep, and regular mobility work."
            )
        if "weight" in goal.lower():
            return (
                "For weight goals, build meals around lean protein, colorful vegetables, fruit, and whole grains; keep water intake high; and focus on consistent routines instead of restriction."
            )
        if "muscle" in goal.lower():
            return (
                "For muscle growth, include protein-rich foods, enough carbohydrates for energy, and plenty of hydration; pair your meals with quality sleep and recovery time."
            )
        return (
            "For general wellness, focus on regular balanced meals, "
            "drink enough water, get adequate sleep, and allow time "
            "for recovery."
        )

    for model in models:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                if getattr(response, "text", None):
                    return response.text
            except Exception as exc:  # pragma: no cover - defensive runtime guard
                print(f"Nutrition error with {model}, attempt {attempt + 1}: {exc}")
                time.sleep(1)

    return (
        "For general wellness, focus on regular balanced meals, "
        "drink enough water, get adequate sleep, and allow time "
        "for recovery."
    )