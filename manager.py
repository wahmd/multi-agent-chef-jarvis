"""Manager for orchestrating the meal prep workflow."""

from __future__ import annotations

from rich.console import Console

from agents import Runner, custom_span, gen_trace_id, trace

from .agents import (
    MealPlan,
    RecipeSearchResult,
    ShoppingList,
    cooking_agent,
    nutrition_agent,
    planner_agent,
    recipe_agent,
    shopping_agent,
)
from .printer import Printer
from .tools import RECIPE_DATABASE, Recipe


class MealPrepManager:
    """Orchestrates the meal prep workflow with multiple agents."""

    def __init__(self) -> None:
        self.console = Console()
        self.printer = Printer(self.console)
        self._initialize_sample_recipes()

    def _initialize_sample_recipes(self) -> None:
        """Initialize the recipe database with some sample recipes."""
        sample_recipes = [
            Recipe(
                name="Chicken Stir Fry",
                ingredients=[
                    "2 chicken breasts, sliced",
                    "2 bell peppers, sliced",
                    "1 onion, sliced",
                    "2 cloves garlic, minced",
                    "2 tbsp soy sauce",
                    "1 tbsp vegetable oil",
                    "1 cup broccoli florets",
                ],
                instructions=[
                    "Heat oil in a large pan over high heat",
                    "Add chicken and cook until browned, about 5 minutes",
                    "Add vegetables and garlic, cook for 3-4 minutes",
                    "Add soy sauce and stir to combine",
                    "Cook for 2 more minutes until vegetables are tender-crisp",
                ],
                prep_time_minutes=15,
                cook_time_minutes=15,
                servings=4,
                cuisine_type="Asian",
                dietary_tags=["high-protein"],
            ),
            Recipe(
                name="Vegetarian Pasta Primavera",
                ingredients=[
                    "12 oz pasta",
                    "2 cups mixed vegetables (zucchini, bell peppers, cherry tomatoes)",
                    "3 cloves garlic, minced",
                    "1/4 cup olive oil",
                    "1/2 cup parmesan cheese",
                    "Fresh basil leaves",
                    "Salt and pepper to taste",
                ],
                instructions=[
                    "Cook pasta according to package directions",
                    "Heat olive oil in a pan, add garlic and cook for 1 minute",
                    "Add vegetables and cook until tender, about 5 minutes",
                    "Drain pasta and add to vegetables",
                    "Toss with parmesan cheese and basil",
                    "Season with salt and pepper",
                ],
                prep_time_minutes=10,
                cook_time_minutes=15,
                servings=4,
                cuisine_type="Italian",
                dietary_tags=["vegetarian"],
            ),
            Recipe(
                name="Grilled Salmon with Vegetables",
                ingredients=[
                    "4 salmon fillets",
                    "2 tbsp olive oil",
                    "1 lemon, juiced",
                    "1 lb asparagus",
                    "2 cups cherry tomatoes",
                    "Salt and pepper to taste",
                ],
                instructions=[
                    "Preheat grill to medium-high heat",
                    "Season salmon with salt, pepper, and lemon juice",
                    "Grill salmon for 4-5 minutes per side",
                    "Toss vegetables with olive oil and grill for 5-7 minutes",
                    "Serve salmon with grilled vegetables",
                ],
                prep_time_minutes=10,
                cook_time_minutes=15,
                servings=4,
                cuisine_type="Mediterranean",
                dietary_tags=["high-protein", "low-carb"],
            ),
            Recipe(
                name="Quinoa Bowl with Roasted Vegetables",
                ingredients=[
                    "1 cup quinoa",
                    "2 cups mixed vegetables (sweet potato, broccoli, bell peppers)",
                    "2 tbsp olive oil",
                    "1/4 cup feta cheese",
                    "1/4 cup chickpeas",
                    "Lemon vinaigrette",
                ],
                instructions=[
                    "Cook quinoa according to package directions",
                    "Toss vegetables with olive oil and roast at 400°F for 20 minutes",
                    "Combine quinoa with roasted vegetables",
                    "Top with feta cheese and chickpeas",
                    "Drizzle with lemon vinaigrette",
                ],
                prep_time_minutes=10,
                cook_time_minutes=25,
                servings=4,
                cuisine_type="Mediterranean",
                dietary_tags=["vegetarian", "gluten-free"],
            ),
            Recipe(
                name="Beef Tacos",
                ingredients=[
                    "1 lb ground beef",
                    "8 taco shells",
                    "1 onion, diced",
                    "2 cloves garlic, minced",
                    "1 packet taco seasoning",
                    "Shredded lettuce",
                    "Diced tomatoes",
                    "Shredded cheese",
                    "Sour cream",
                ],
                instructions=[
                    "Brown ground beef in a pan over medium heat",
                    "Add onion and garlic, cook until softened",
                    "Add taco seasoning and cook according to package directions",
                    "Warm taco shells according to package directions",
                    "Fill shells with beef mixture and top with desired toppings",
                ],
                prep_time_minutes=15,
                cook_time_minutes=15,
                servings=4,
                cuisine_type="Mexican",
                dietary_tags=[],
            ),
        ]

        for recipe in sample_recipes:
            RECIPE_DATABASE[recipe.name] = recipe

    async def run(self, query: str) -> None:
        """Run the complete meal prep workflow."""
        trace_id = gen_trace_id()
        with trace("Meal prep trace", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}",
                is_done=True,
                hide_checkmark=True,
            )

            self.printer.update_item("start", "Starting meal prep workflow...", is_done=True)

            # Step 1: Create meal plan
            meal_plan = await self._create_meal_plan(query)

            # Step 2: Search for recipes if needed
            recipes_found = await self._search_recipes(meal_plan)

            # Step 3: Analyze nutrition
            nutrition_analysis = await self._analyze_nutrition(meal_plan)

            # Step 4: Generate shopping list
            shopping_list = await self._generate_shopping_list(meal_plan)

            # Step 5: Provide cooking tips
            cooking_tips = await self._get_cooking_tips(meal_plan)

            self.printer.update_item("complete", "Meal prep workflow complete!", is_done=True)
            self.printer.end()

            # Print results
            self._print_results(meal_plan, recipes_found, nutrition_analysis, shopping_list, cooking_tips)

    async def _create_meal_plan(self, query: str) -> MealPlan:
        """Create a meal plan based on user query."""
        self.printer.update_item("planning", "Creating meal plan...")
        try:
            result = await Runner.run(planner_agent, query)
            meal_plan = result.final_output_as(MealPlan)
            self.printer.update_item(
                "planning",
                f"Created meal plan for {meal_plan.total_days} days",
                is_done=True,
            )
            return meal_plan
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                self.printer.update_item(
                    "planning",
                    "❌ Error: OpenAI API quota exceeded. Please check your billing at https://platform.openai.com/account/billing",
                    is_done=True,
                )
                raise RuntimeError(
                    "OpenAI API quota exceeded. Please:\n"
                    "1. Check your billing at https://platform.openai.com/account/billing\n"
                    "2. Add payment method or increase quota\n"
                    "3. Or use a different model/provider (see config.py)"
                ) from e
            raise

    async def _search_recipes(self, meal_plan: MealPlan) -> RecipeSearchResult | None:
        """Search for recipes needed in the meal plan."""
        with custom_span("Search recipes"):
            self.printer.update_item("searching", "Searching for recipes...")

            # Collect unique recipe names from meal plan
            recipe_names = set()
            for day in meal_plan.days:
                for meal in day.meals:
                    recipe_names.add(meal.recipe_name)

            # Search for each recipe
            search_query = ", ".join(recipe_names)
            result = await Runner.run(recipe_agent, f"Find recipes: {search_query}")
            recipe_result = result.final_output_as(RecipeSearchResult)

            found_count = len(recipe_result.recipes)
            self.printer.update_item(
                "searching",
                f"Found {found_count} recipes",
                is_done=True,
            )
            return recipe_result

    async def _analyze_nutrition(self, meal_plan: MealPlan) -> str:
        """Analyze nutrition for the meal plan."""
        self.printer.update_item("nutrition", "Analyzing nutrition...")

        # Collect all recipes from meal plan
        recipe_names = []
        for day in meal_plan.days:
            for meal in day.meals:
                recipe_names.append(meal.recipe_name)

        # Get nutrition info for each recipe
        nutrition_input = f"Analyze nutrition for these recipes: {', '.join(set(recipe_names))}"
        result = await Runner.run(nutrition_agent, nutrition_input)

        self.printer.mark_item_done("nutrition")
        return result.final_output

    async def _generate_shopping_list(self, meal_plan: MealPlan) -> ShoppingList:
        """Generate shopping list from meal plan."""
        self.printer.update_item("shopping", "Generating shopping list...")

        # Collect all recipe names
        recipe_names = []
        for day in meal_plan.days:
            for meal in day.meals:
                recipe_names.append(meal.recipe_name)

        shopping_input = f"Create shopping list for these recipes: {', '.join(set(recipe_names))}"
        result = await Runner.run(shopping_agent, shopping_input)
        shopping_list = result.final_output_as(ShoppingList)

        self.printer.update_item(
            "shopping",
            f"Generated shopping list with {shopping_list.total_items} items",
            is_done=True,
        )
        return shopping_list

    async def _get_cooking_tips(self, meal_plan: MealPlan) -> str:
        """Get cooking tips for recipes in meal plan."""
        self.printer.update_item("tips", "Gathering cooking tips...")

        # Get tips for first few recipes
        recipe_names = []
        for day in meal_plan.days[:2]:  # Just get tips for first 2 days
            for meal in day.meals:
                if meal.recipe_name not in recipe_names:
                    recipe_names.append(meal.recipe_name)

        tips_input = f"Provide cooking tips for: {', '.join(recipe_names)}"
        result = await Runner.run(cooking_agent, tips_input)

        self.printer.mark_item_done("tips")
        return result.final_output

    def _print_results(
        self,
        meal_plan: MealPlan,
        recipes_found: RecipeSearchResult | None,
        nutrition_analysis: str,
        shopping_list: ShoppingList,
        cooking_tips: str,
    ) -> None:
        """Print formatted results."""
        print("\n" + "=" * 80)
        print("MEAL PLAN")
        print("=" * 80 + "\n")

        for day in meal_plan.days:
            print(f"\n{day.day}:")
            for meal in day.meals:
                print(f"  {meal.meal_type.capitalize()}: {meal.recipe_name} ({meal.servings} servings)")

        if meal_plan.dietary_notes:
            print(f"\nDietary Notes: {meal_plan.dietary_notes}")

        print("\n" + "=" * 80)
        print("NUTRITION ANALYSIS")
        print("=" * 80 + "\n")
        print(nutrition_analysis)

        print("\n" + "=" * 80)
        print("SHOPPING LIST")
        print("=" * 80 + "\n")

        if shopping_list.produce:
            print("PRODUCE:")
            for item in shopping_list.produce:
                print(f"  • {item}")

        if shopping_list.protein:
            print("\nPROTEIN:")
            for item in shopping_list.protein:
                print(f"  • {item}")

        if shopping_list.dairy:
            print("\nDAIRY:")
            for item in shopping_list.dairy:
                print(f"  • {item}")

        if shopping_list.pantry:
            print("\nPANTRY:")
            for item in shopping_list.pantry:
                print(f"  • {item}")

        if shopping_list.other:
            print("\nOTHER:")
            for item in shopping_list.other:
                print(f"  • {item}")

        print("\n" + "=" * 80)
        print("COOKING TIPS")
        print("=" * 80 + "\n")
        print(cooking_tips)
        print()
