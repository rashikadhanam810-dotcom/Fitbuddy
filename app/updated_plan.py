import os
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


def update_workout_plan(original_plan, feedback):

    if client is None:
        return (
            "Updated plan unavailable because the Gemini API key is not configured. "
            "Please add a valid GOOGLE_API_KEY in the environment to enable AI adjustments."
        )

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Here is the user's original 7-day wellness plan:

{original_plan}

The user provided this feedback:

{feedback}

Create an updated 7-day general wellness and physical-activity plan
based on the feedback.

Requirements:
- Keep the plan safe and age-appropriate.
- Include Day 1 through Day 7.
- Modify activities according to the feedback.
- Include rest or recovery when appropriate.
- Include warm-up and cool-down suggestions.
- Do not recommend extreme exercise.
- Do not recommend restrictive eating.
- Do not recommend rapid weight changes.
- Keep the plan simple and easy to understand.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return getattr(response, "text", "Updated plan unavailable at the moment.")
    except Exception:
        return (
            "The AI plan update could not be generated right now. "
            "Please try again in a few moments."
        )