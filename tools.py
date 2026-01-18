"""Function tools for the meal prep system."""

from typing import Annotated

from pydantic import BaseModel, Field

from agents import function_tool


class Recipe(BaseModel):
    """A recipe with ingredients and instructions."""

    name: str = Field(description="Name of the recipe")
    ingredients: list[str] = Field(description="List of ingredients with quantities")
    instructions: list[str] = Field(description="Step-by-step cooking instructions")
    prep_time_minutes: int = Field(description="Preparation time in minutes")
    cook_time_minutes: int = Field(description="Cooking time in minutes")
    servings: int = Field(description="Number of servings")
    cuisine_type: str | None = Field(default=None, description="Type of cuisine")
    dietary_tags: list[str] = Field(
        default_factory=list, description="Dietary tags (e.g., vegetarian, gluten-free)"
    )


class NutritionInfo(BaseModel):
    """Nutritional information for a recipe."""

    calories_per_serving: int = Field(description="Calories per serving")
    protein_grams: float = Field(description="Protein in grams per serving")
    carbs_grams: float = Field(description="Carbohydrates in grams per serving")
    fat_grams: float = Field(description="Fat in grams per serving")
    fiber_grams: float = Field(description="Fiber in grams per serving")
    sugar_grams: float = Field(description="Sugar in grams per serving")


# In-memory recipe database (in production, this would be a real database)
RECIPE_DATABASE: dict[str, Recipe] = {}


@function_tool
def search_recipes(
    query: Annotated[str, "Search query (e.g., 'pasta', 'chicken', 'vegetarian')"],
    max_results: Annotated[int, "Maximum number of recipes to return"] = 5,
) -> list[Recipe]:
    """Search for recipes matching the query."""
    query_lower = query.lower()
    matches = []

    for recipe in RECIPE_DATABASE.values():
        if (
            query_lower in recipe.name.lower()
            or any(query_lower in ing.lower() for ing in recipe.ingredients)
            or any(query_lower in tag.lower() for tag in recipe.dietary_tags)
            or (recipe.cuisine_type and query_lower in recipe.cuisine_type.lower())
        ):
            matches.append(recipe)
            if len(matches) >= max_results:
                break

    return matches


@function_tool
def get_recipe_by_name(
    name: Annotated[str, "Exact name of the recipe"]
) -> Recipe | None:
    """Get a recipe by its exact name."""
    return RECIPE_DATABASE.get(name)


@function_tool
def add_recipe(recipe: Annotated[Recipe, "The recipe to add"]) -> str:
    """Add a new recipe to the database."""
    RECIPE_DATABASE[recipe.name] = recipe
    return f"Added recipe: {recipe.name}"


@function_tool
def calculate_nutrition(
    ingredients: Annotated[list[str], "List of ingredients with quantities"],
    servings: Annotated[int, "Number of servings"] = 4,
) -> NutritionInfo:
    """
    Calculate approximate nutritional information for a recipe.
    This is a simplified calculation - in production, you'd use a real nutrition API.
    """
    # Simplified nutrition calculation based on common ingredients
    # In production, this would call a real nutrition API like Edamam, Spoonacular, etc.
    total_calories = 0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0
    total_fiber = 0.0
    total_sugar = 0.0

    for ingredient in ingredients:
        ing_lower = ingredient.lower()
        # Very simplified nutrition estimates
        if "chicken" in ing_lower or "beef" in ing_lower or "pork" in ing_lower:
            total_calories += 200
            total_protein += 25.0
            total_fat += 10.0
        elif "pasta" in ing_lower or "rice" in ing_lower or "bread" in ing_lower:
            total_calories += 150
            total_carbs += 30.0
            total_protein += 5.0
        elif "vegetable" in ing_lower or "broccoli" in ing_lower or "spinach" in ing_lower:
            total_calories += 30
            total_carbs += 5.0
            total_fiber += 3.0
        elif "cheese" in ing_lower or "milk" in ing_lower:
            total_calories += 100
            total_protein += 7.0
            total_fat += 8.0
        elif "oil" in ing_lower or "butter" in ing_lower:
            total_calories += 120
            total_fat += 14.0
        elif "sugar" in ing_lower or "honey" in ing_lower:
            total_calories += 50
            total_carbs += 12.0
            total_sugar += 12.0

    return NutritionInfo(
        calories_per_serving=int(total_calories / servings),
        protein_grams=round(total_protein / servings, 1),
        carbs_grams=round(total_carbs / servings, 1),
        fat_grams=round(total_fat / servings, 1),
        fiber_grams=round(total_fiber / servings, 1),
        sugar_grams=round(total_sugar / servings, 1),
    )


@function_tool
def generate_shopping_list(
    recipes: Annotated[list[str], "List of recipe names"],
    servings_multiplier: Annotated[float, "Multiply servings by this factor"] = 1.0,
) -> list[str]:
    """
    Generate a consolidated shopping list from multiple recipes.
    Combines ingredients and groups similar items together.
    """
    all_ingredients: list[str] = []

    for recipe_name in recipes:
        recipe = RECIPE_DATABASE.get(recipe_name)
        if recipe:
            # Adjust servings if needed
            if servings_multiplier != 1.0:
                adjusted_ingredients = []
                for ing in recipe.ingredients:
                    # Simple adjustment - in production, you'd parse quantities properly
                    adjusted_ingredients.append(ing)
                all_ingredients.extend(adjusted_ingredients)
            else:
                all_ingredients.extend(recipe.ingredients)

    # Group similar ingredients (simplified - in production, use NLP to group)
    consolidated: dict[str, list[str]] = {}
    for ingredient in all_ingredients:
        # Extract base ingredient name (simplified)
        base = ingredient.split(",")[0].strip().lower()
        if base not in consolidated:
            consolidated[base] = []
        consolidated[base].append(ingredient)

    # Return consolidated list
    shopping_list = []
    for base, items in consolidated.items():
        if len(items) == 1:
            shopping_list.append(items[0])
        else:
            # Combine multiple instances
            shopping_list.append(f"{items[0]} (x{len(items)})")

    return sorted(shopping_list)


@function_tool
def get_cooking_tips(
    recipe_name: Annotated[str, "Name of the recipe"],
    step_number: Annotated[int | None, "Specific step number, or None for general tips"] = None,
) -> str:
    """Get helpful cooking tips for a recipe or specific step."""
    recipe = RECIPE_DATABASE.get(recipe_name)
    if not recipe:
        return f"Recipe '{recipe_name}' not found."

    if step_number is not None and 1 <= step_number <= len(recipe.instructions):
        step = recipe.instructions[step_number - 1]
        return f"Tip for step {step_number} ({step[:50]}...): Make sure to follow the timing carefully and check doneness before proceeding."

    # General tips based on recipe type
    tips = []
    if "pasta" in recipe.name.lower():
        tips.append("Cook pasta 1 minute less than package directions for al dente texture.")
        tips.append("Reserve pasta water - it's great for making sauces creamier.")
    if "chicken" in recipe.name.lower() or "meat" in recipe.name.lower():
        tips.append("Let meat rest for 5-10 minutes after cooking for juicier results.")
        tips.append("Use a meat thermometer to ensure proper doneness.")
    if "vegetable" in recipe.name.lower() or any("vegetable" in tag.lower() for tag in recipe.dietary_tags):
        tips.append("Don't overcook vegetables - they're best when still slightly crisp.")
        tips.append("Season vegetables generously with salt and pepper.")

    if not tips:
        tips.append("Read through all instructions before starting.")
        tips.append("Prep all ingredients before you begin cooking (mise en place).")
        tips.append("Taste as you go and adjust seasoning accordingly.")

    return "\n".join(f"• {tip}" for tip in tips)
