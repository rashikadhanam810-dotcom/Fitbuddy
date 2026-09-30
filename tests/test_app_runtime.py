import app.gemini_generator as gemini_generator
import app.gemini_flash_generator as gemini_flash_generator


def test_workout_generation_handles_missing_client(monkeypatch):
    monkeypatch.setattr(gemini_generator, "client", None)
    result = gemini_generator.generate_workout_gemini(30, 70, "weight loss", "medium")
    assert "FitBuddy 7-Day Plan" in result
    assert "Day 1" in result


def test_nutrition_generation_handles_missing_client(monkeypatch):
    monkeypatch.setattr(gemini_flash_generator, "client", None)
    result = gemini_flash_generator.generate_nutrition_tip_with_flash("general wellness")
    assert "balanced meals" in result.lower()
