"""Agent for creating meal plans."""

import os

from pydantic import BaseModel, Field

from agents import Agent

# Allow model override from config
DEFAULT_MODEL = os.getenv("MEAL_PREP_MODEL") or None

PROMPT = (
    "You are a meal planning assistant. Create a balanced meal plan based on the user's "
    "requirements. Consider:\n"
    "- Number of days to plan for\n"
    "- Dietary restrictions and preferences\n"
    "- Variety in meals (don't repeat the same dish)\n"
    "- Nutritional balance\n"
    "- Cooking time constraints\n"
    "- Leftover utilization\n\n"
    "Output a structured meal plan with breakfast, lunch, and dinner for each day."
)


class MealItem(BaseModel):
    """A single meal item in the plan."""

    meal_type: str = Field(description="Type of meal: breakfast, lunch, dinner, or snack")
    recipe_name: str = Field(description="Name of the recipe for this meal")
    servings: int = Field(description="Number of servings", default=2)


class DayPlan(BaseModel):
    """Meal plan for a single day."""

    day: str = Field(description="Day name (e.g., Monday, Day 1)")
    meals: list[MealItem] = Field(description="List of meals for this day")


class MealPlan(BaseModel):
    """Complete meal plan."""

    days: list[DayPlan] = Field(description="Meal plan for each day")
    total_days: int = Field(description="Total number of days planned")
    dietary_notes: str = Field(
        default="", description="Notes about dietary considerations in this plan"
    )


planner_agent = Agent(
    name="MealPlannerAgent",
    instructions=PROMPT,
    output_type=MealPlan,
    model=DEFAULT_MODEL if DEFAULT_MODEL else None,  # Use default if not set
)
