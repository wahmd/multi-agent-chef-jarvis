"""Agent for generating shopping lists."""

from pydantic import BaseModel, Field

from agents import Agent
from examples.meal_prep.tools import generate_shopping_list

PROMPT = (
    "You are a shopping list assistant. Generate organized shopping lists from meal plans. "
    "When given recipe names, use the generate_shopping_list tool to get the raw ingredient list, "
    "then organize those ingredients into categories:\n"
    "- Produce section (fruits, vegetables)\n"
    "- Meat/Protein section (meat, fish, eggs, tofu, etc.)\n"
    "- Dairy section (milk, cheese, yogurt, etc.)\n"
    "- Pantry items (grains, spices, canned goods, oils, etc.)\n"
    "- Other items\n\n"
    "First call generate_shopping_list with the recipe names as a list, then categorize the results. "
    "Consolidate duplicate ingredients and provide clear quantities."
)


class ShoppingList(BaseModel):
    """A shopping list organized by category."""

    produce: list[str] = Field(default_factory=list, description="Fruits and vegetables")
    protein: list[str] = Field(default_factory=list, description="Meat, fish, eggs, etc.")
    dairy: list[str] = Field(default_factory=list, description="Dairy products")
    pantry: list[str] = Field(default_factory=list, description="Grains, spices, canned goods, etc.")
    other: list[str] = Field(default_factory=list, description="Other items")
    total_items: int = Field(description="Total number of unique items")


shopping_agent = Agent(
    name="ShoppingAgent",
    instructions=PROMPT,
    tools=[generate_shopping_list],
    output_type=ShoppingList,
)
