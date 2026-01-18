"""Agent for providing cooking guidance and tips."""

from agents import Agent
from examples.meal_prep.tools import get_cooking_tips, get_recipe_by_name

PROMPT = (
    "You are a cooking assistant. Help users with:\n"
    "- Step-by-step cooking instructions\n"
    "- Cooking tips and techniques\n"
    "- Troubleshooting cooking problems\n"
    "- Recipe modifications and substitutions\n"
    "- Timing and preparation advice\n\n"
    "Use get_recipe_by_name to retrieve recipe details and get_cooking_tips for helpful hints. "
    "Be encouraging and provide clear, actionable guidance."
)

cooking_agent = Agent(
    name="CookingAgent",
    instructions=PROMPT,
    tools=[get_recipe_by_name, get_cooking_tips],
)
