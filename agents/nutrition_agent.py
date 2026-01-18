"""Agent for analyzing nutrition information."""

from agents import Agent
from examples.meal_prep.tools import calculate_nutrition

PROMPT = (
    "You are a nutrition analysis assistant. Analyze the nutritional content of recipes "
    "and meal plans. Use the calculate_nutrition tool to get nutritional information. "
    "Provide insights about:\n"
    "- Calorie content\n"
    "- Macronutrient balance (protein, carbs, fats)\n"
    "- Micronutrient considerations\n"
    "- Dietary compliance (e.g., keto, low-carb, high-protein)\n"
    "- Suggestions for nutritional improvements\n\n"
    "Be specific and provide actionable advice."
)

nutrition_agent = Agent(
    name="NutritionAgent",
    instructions=PROMPT,
    tools=[calculate_nutrition],
)
