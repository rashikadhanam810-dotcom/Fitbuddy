from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .database import (
    save_user,
    save_plan,
    update_plan,
    get_user,
    get_all_users,
    delete_user
)

from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan


router = APIRouter()

# Correct template path
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# ---------------------------------------
# HOME PAGE
# ---------------------------------------

@router.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ---------------------------------------
# GENERATE WORKOUT
# ---------------------------------------

@router.post("/generate-workout")
def generate_workout(
    request: Request,

    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    workout_plan = generate_workout_gemini(
        age,
        weight,
        goal,
        intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    save_user(
        username,
        user_id,
        age,
        weight,
        goal,
        intensity
    )

    save_plan(
        user_id,
        workout_plan,
        nutrition_tip
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "updated_plan": None
        }
    )


# ---------------------------------------
# SUBMIT FEEDBACK
# ---------------------------------------

@router.post("/submit-feedback")
def submit_feedback(
    request: Request,

    user_id: str = Form(...),
    feedback: str = Form(...)
):

    user = get_user(user_id)

    if not user:

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "error": "User ID not found."
            }
        )

    original_plan = user.original_plan

    updated_plan = update_workout_plan(
        original_plan,
        feedback
    )

    update_plan(
        user_id,
        updated_plan
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": user.original_plan,
            "nutrition_tip": user.nutrition_tip,
            "updated_plan": updated_plan,
            "message": "Workout plan updated successfully!"
        }
    )


# ---------------------------------------
# VIEW ALL USERS
# ---------------------------------------

@router.get("/view-all-users")
def view_all_users(request: Request):

    users = get_all_users()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        }
    )


# ---------------------------------------
# DELETE USER
# ---------------------------------------

@router.post("/delete-user")
def remove_user(
    user_id: str = Form(...)
):

    delete_user(user_id)

    return RedirectResponse(
        url="/view-all-users",
        status_code=303
    )