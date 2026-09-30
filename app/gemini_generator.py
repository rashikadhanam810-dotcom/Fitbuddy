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


def _generate_with_fallback(prompt, models):
    if client is None:
        return None

    for model in models:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                text = getattr(response, "text", None)
                if text:
                    return text
            except Exception as exc:  # pragma: no cover - defensive runtime guard
                print(f"Gemini error with {model}, attempt {attempt + 1}: {exc}")
                time.sleep(1)

    return None


def _fallback_workout_plan(age, weight, goal, intensity):
    goal_text = goal.lower().strip()
    intensity_map = {
        "low": "light",
        "medium": "moderate",
        "high": "strong"
    }
    level = intensity_map.get(intensity.lower(), "moderate")

    if "weight" in goal_text:
        focus = "fat loss, strength, and consistent movement"
    elif "muscle" in goal_text:
        focus = "muscle activation, controlled strength work, and recovery"
    elif "flex" in goal_text:
        focus = "mobility, posture, and joint-friendly movement"
    else:
        focus = "overall wellbeing, stamina, and recovery"

    return f"""FitBuddy 7-Day Plan

Goal: {goal.title()} | Intensity: {intensity.title()} | Level: {level.title()}
Focus: {focus}

Day 1 - Mobility + Core
- Warm-up: 5 minutes brisk walk + shoulder rolls
- Main work: 10 bodyweight squats, 10 wall push-ups, 20-second plank, 20 lunges total
- Cool-down: 5 minutes of stretching for calves, hamstrings, and chest

Day 2 - Strength Basics
- Warm-up: 5 minutes marching in place + arm circles
- Main work: 12 sit-to-stands, 10 incline push-ups, 12 glute bridges, 20-second dead bug hold
- Cool-down: stretch hips, lower back, and shoulders

Day 3 - Recovery + Stretch
- Warm-up: 5 minutes easy walk
- Main work: gentle yoga flow, cat-cow, downward dog, hip openers, hamstring stretch
- Cool-down: breathing practice for 3 minutes and frequent hydration

Day 4 - Active Cardio
- Warm-up: 5 minutes mobility
- Main work: 20-25 minutes brisk walking, cycling, or low-impact cardio
- Cool-down: slow walk and calf/quad stretching

Day 5 - Strength + Balance
- Warm-up: 5 minutes body movement and marching
- Main work: 10 goblet-style squats (or bodyweight squats), 10 supported rows, 12 step-ups per leg, 20 seconds balance hold
- Cool-down: hamstring and ankle stretch

Day 6 - Flexibility + Posture
- Warm-up: 5 minutes easy movement
- Main work: dynamic stretching, seated twists, chest opener, quad stretch, glute stretch
- Cool-down: 5 minutes breathing and recovery

Day 7 - Light Recovery Day
- Warm-up: 5 minutes easy movement
- Main work: light walk, mobility drill, and easy stretching
- Cool-down: relax and hydrate; keep effort easy

General guidance:
- Keep effort at a level where you can still speak comfortably.
- Drink water before and after workouts.
- Aim for 7-9 hours of sleep, and keep meals balanced with protein, fruit, vegetables, and whole grains.
- If you feel pain, reduce intensity and stop.
"""


def generate_workout_gemini(age, weight, goal, intensity):

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a safe, beginner-friendly 7-day general wellness
and physical-activity plan.

User information:
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:
- Provide Day 1 through Day 7.
- Include simple exercises or physical activities.
- Include warm-up and cool-down suggestions.
- Include rest or recovery when appropriate.
- Keep activities age-appropriate and safe.
- Do not prescribe extreme exercise.
- Do not recommend restrictive eating.
- Do not recommend rapid weight changes.
- Keep the response easy to read.
"""

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
    ]

    response_text = _generate_with_fallback(prompt, models)
    if response_text:
        return response_text

    return _fallback_workout_plan(age, weight, goal, intensity)
