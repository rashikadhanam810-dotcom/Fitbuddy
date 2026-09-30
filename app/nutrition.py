def get_basic_nutrition_tip(goal):

    tips = {
        "weight loss":
            "Include vegetables, fruits, whole grains and protein-rich foods in balanced meals.",

        "muscle gain":
            "Include protein-rich foods such as eggs, beans, fish, chicken or dairy in balanced meals.",

        "general wellness":
            "Stay hydrated and include a variety of fruits, vegetables, whole grains and protein sources.",

        "flexibility":
            "Stay hydrated and include balanced meals with enough protein and nutrient-rich foods."
    }

    return tips.get(
        goal.lower(),
        "Focus on balanced meals, hydration and adequate recovery."
    )