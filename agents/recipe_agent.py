"""Agent for searching and finding recipes."""

from pydantic import BaseModel, Field

from agents import Agent
from examples.meal_prep.tools import get_recipe_by_name, search_recipes

PROMPT = (
    "You are a recipe search assistant. Your job is to find recipes that match the user's "
    "requirements. Use the search_recipes tool to find recipes, and get_recipe_by_name to "
    "retrieve full recipe details. Consider dietary restrictions, cuisine preferences, "
    "cooking time, and ingredient availability when searching."
)


class RecipeSearchResult(BaseModel):
    """Result of a recipe search."""

    recipes: list[str] = Field(description="List of recipe names that match the search criteria")
    reasoning: str = Field(description="Explanation of why these recipes were selected")


recipe_agent = Agent(
    name="RecipeSearchAgent",
    instructions=PROMPT,
    tools=[search_recipes, get_recipe_by_name],
    output_type=RecipeSearchResult,
)
