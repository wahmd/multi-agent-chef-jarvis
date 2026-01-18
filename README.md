# Multi-Agent Chef Jarvis 👨‍🍳

A multi-agent meal prep app using openai-agents-python. This project demonstrates how multiple AI agents can work together to handle complex meal planning workflows - from creating meal plans to generating shopping lists and providing cooking tips.

## What It Does

Ever wish you had a personal chef that could plan your meals, check nutrition, create shopping lists, and give you cooking tips? That's what this app does. It uses five specialized AI agents that each handle a different part of meal prep:

- **Meal Planner** - Creates balanced meal plans based on your preferences
- **Recipe Finder** - Searches through recipes to match your meal plan
- **Nutrition Analyst** - Breaks down the nutritional content of your meals
- **Shopping List Generator** - Consolidates ingredients into an organized shopping list
- **Cooking Assistant** - Provides tips and guidance for preparing your meals

## Architecture

Here's how the agents work together:

```
┌─────────────────┐
│   User Query    │
│ "Plan meals for │
│  3 days, veg"   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              MealPrepManager (Orchestrator)              │
└────────┬─────────────────────────────────────────────────┘
         │
         ├──────────────────────────────────────────────┐
         │                                              │
         ▼                                              ▼
┌──────────────────┐                          ┌──────────────────┐
│ MealPlannerAgent │                          │ RecipeSearchAgent│
│                  │                          │                  │
│ Creates structured│                          │ Finds matching  │
│ meal plan with   │                          │ recipes from DB │
│ breakfast/lunch/ │                          │                  │
│ dinner for each  │                          │                  │
│ day               │                          │                  │
└────────┬──────────┘                          └────────┬─────────┘
         │                                              │
         │                                              │
         ├──────────────────────────────────────────────┤
         │                                              │
         ▼                                              ▼
┌──────────────────┐                          ┌──────────────────┐
│ NutritionAgent  │                          │ ShoppingAgent    │
│                  │                          │                  │
│ Analyzes macros, │                          │ Consolidates     │
│ calories, dietary│                          │ ingredients by   │
│ compliance       │                          │ category         │
└────────┬──────────┘                          └────────┬─────────┘
         │                                              │
         │                                              │
         └──────────────┬───────────────────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ CookingAgent      │
              │                   │
              │ Provides tips &   │
              │ step-by-step help │
              └─────────┬──────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Final Output    │
              │  (Meal Plan +    │
              │   Shopping List +│
              │   Tips)          │
              └──────────────────┘
```

The workflow is orchestrated by the `MealPrepManager`, which coordinates all the agents and handles the flow of data between them. Each agent is specialized for its task, making the system modular and easy to extend.

## Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation

1. Clone the repo:
```bash
git clone https://github.com/yourusername/multi-agent-chef-jarvis.git
cd multi-agent-chef-jarvis
```

2. Install dependencies:
```bash
pip install openai-agents rich pydantic
```

3. Set up your API key. Copy the example config:
```bash
cp config.py.example config.py
```

Then edit `config.py` and either:
- Set `API_KEY = "sk-your-key-here"` directly (for local dev)
- Or use environment variable: `export OPENAI_API_KEY="sk-your-key-here"`

**Important:** `config.py` is in `.gitignore` - never commit your API key!

### Running It

```bash
python main.py
```

Then enter a query like:
- "Plan meals for 3 days, vegetarian, quick recipes"
- "Create a meal plan for 5 days with high protein"
- "I need Pakistani-style meals for a week, calorie deficit"

The app will walk through each step and give you a complete meal plan, nutrition breakdown, shopping list, and cooking tips.

## How It Works Under the Hood

The app uses the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) which provides a clean way to build multi-agent systems. Each agent is defined with:

- **Instructions**: What the agent should do
- **Tools**: Functions the agent can call (like searching recipes or calculating nutrition)
- **Output Types**: Structured data formats (using Pydantic models)

The manager orchestrates everything - it calls each agent in sequence, passes data between them, and handles errors gracefully. The agents use function tools to interact with the recipe database and perform calculations.

## Project Structure

```
multi-agent-chef-jarvis/
├── agents/              # Individual agent definitions
│   ├── planner_agent.py
│   ├── recipe_agent.py
│   ├── nutrition_agent.py
│   ├── shopping_agent.py
│   └── cooking_agent.py
├── tools.py            # Function tools (recipe DB, nutrition calc, etc.)
├── manager.py          # Orchestrates the workflow
├── printer.py          # Handles terminal output
├── main.py             # Entry point
├── config.py.example   # Config template (copy to config.py)
└── README.md           # This file
```

## Customization

Want to add more recipes? The system comes with 5 sample recipes, but you can easily add more by modifying the `_initialize_sample_recipes()` method in `manager.py`.

To integrate with real APIs (like Spoonacular for recipes or Edamam for nutrition), you'd replace the mock functions in `tools.py` with actual API calls.

## Example Output

When you run it, you'll get something like:
prompt: "Plan calorie deficit meals for one week, Pakistani style, with quick recipes."

```
================================================================================
MEAL PLAN
================================================================================


Day 1:
  Breakfast: Vegetable Egg White Omelette with Whole Wheat Toast (1 servings)
  Lunch: Grilled Chicken Salad with Yogurt Mint Dressing (1 servings)
  Dinner: Lauki (Bottle Gourd) Curry with 1 Roti (1 servings)

Day 2:
  Breakfast: Dahi Poha (Flattened Rice with Yogurt and Vegetables) (1 servings)
  Lunch: Bhuna Keema (Lean Minced Beef/Chicken) with Salad (1 servings)
  Dinner: Moong Masoor Dal with Brown Rice (Small Portion) (1 servings)

Day 3:
  Breakfast: Chana Chaat (Chickpea Salad) with Lemon (1 servings)
  Lunch: Grilled Fish Tikka with Mixed Vegetables (1 servings)
  Dinner: Palak Paneer (Light, No Cream) with 1 Roti (1 servings)

Day 4:
  Breakfast: Oats Upma with Mixed Vegetables (1 servings)
  Lunch: Chicken Shorba (Clear Soup) with Grilled Veggies (1 servings)
  Dinner: Tinda Curry with 1 Roti (1 servings)

Day 5:
  Breakfast: Boiled Egg and Tomato Sandwich on Whole Wheat Bread (1 servings)
  Lunch: Mixed Lentil Daal with Cucumber Salad (1 servings)
  Dinner: Grilled Chicken Seekh Kebab with Mixed Salad (1 servings)

Day 6:
  Breakfast: Fruit Yogurt Parfait (Low-fat Yogurt, Fresh Fruits) (1 servings)
  Lunch: Bhindi (Okra) Sabzi with 1 Roti (1 servings)
  Dinner: Lean Beef Curry (Light Oil) with Cauliflower Rice (1 servings)

Day 7:
  Breakfast: Moong Dal Chilla (Savory Pancake) with Mint Chutney (1 servings)
  Lunch: Grilled Fish Fillet with Sauteed Spinach (1 servings)
  Dinner: Chicken Karahi (Minimal Oil) with 1 Roti (1 servings)

Dietary Notes: Portion sizes are controlled for calorie deficit. All meals are Pakistani inspired and use minimal oil. Recipes are designed to be quick (under 30 minutes) and use fresh ingredients. Focus on lean meats, vegetables, whole grains, and legumes. Roti is whole wheat and rice is brown or minimal quantity. Snacks can be fresh fruit or unsalted nuts if needed.

================================================================================
NUTRITION ANALYSIS
================================================================================

Here’s a breakdown and analysis for the recipes you listed (nutritional values are per serving; approximate, key macronutrients shown):

---

### 1. Dahi Poha
- **Calories:** 75 
- **Protein:** 2.5g
- **Carbs:** 15g
- **Fat:** 0g
- *Insight:* Low in fat and calories. Good source of carbs. Add more protein (nuts/seeds) for better balance.

### 2. Moong Dal Chilla + Mint Chutney
- **Calories:** 30
- **Protein:** 0g
- **Carbs:** 0g
- **Fat:** 3.5g
- *Insight:* Very low cal. If using whole dal, expect more protein. Chutney adds little calories, but overall not a protein-rich meal unless more dal is included.

### 3. Chana Chaat
- **Calories:** 60
- **Protein:** 0g
- **Carbs:** 0g
- **Fat:** 7g
- *Insight:* Higher in fat (likely from dressing). Actual chana chaat is higher protein/carb; consider adding veggies to boost fiber and micronutrients.

### 4. Oats Upma
- **Calories:** 75
- **Protein:** 0g
- **Carbs:** 2.5g
- **Fat:** 7g
- *Insight:* Low calorie, decent healthy fat if oil is moderate. Add protein (peas, nuts, egg whites).

### 5. Moong Masoor Dal with Brown Rice
- **Calories:** 75
- **Protein:** 2.5g
- **Carbs:** 15g
- **Fat:** 0g
- *Insight:* Good complex carbs and some protein. Portion size can be increased for higher protein.

### 6. Bhuna Keema (Lean Beef/Chicken) with Salad
- **Calories:** 175
- **Protein:** 12.5g
- **Carbs:** 2.5g
- **Fat:** 12g
- *Insight:* Good low-carb, moderate protein meal if using lean meat. Fiber via salad. Suitable for low-carb diets.

### 7. Lean Beef Curry with Cauliflower Rice
- **Calories:** 235
- **Protein:** 15g
- **Carbs:** 15g
- **Fat:** 12g
- *Insight:* Balanced, protein-rich, moderate fat. Cauliflower rice keeps carbs lower than regular rice.

### 8. Grilled Chicken Seekh Kebab with Salad
- **Calories:** 175
- **Protein:** 12.5g
- **Carbs:** 2.5g
- **Fat:** 12g
- *Insight:* Good protein, low carb—excellent for weight loss or low-carb diets.

### 9. Fruit Yogurt Parfait (Low-fat Yogurt, Fresh Fruits)
- **Calories:** 0 
- *Note:* This seems off; low-fat yogurt + fruit should yield ~100-150 cal, 6g protein, 20g carbs.
- *Insight:* Light, good for breakfast/snack. Add seeds/nuts for healthy fats.

### 10. Grilled Chicken Salad with Yogurt Mint Dressing
- **Calories:** 100
- **Protein:** 12.5g
- **Carbs:** 0g
- **Fat:** 5g
- *Insight:* High protein, low carb—great for weight loss or muscle retention.

### 11. Palak Paneer with 1 Roti (Light, No Cream)
- **Calories:** 15
- **Protein:** 0g
- **Carbs:** 2.5g
- **Fat:** 0g
- *Note:* Likely higher, especially with roti and paneer (~200 kcal, 8g protein, 18g carbs, 7g fat)
- *Insight:* Good vegetarian protein. Use low-fat paneer.

### 12. Chicken Karahi (Minimal Oil) with 1 Roti
- **Calories:** 160
- **Protein:** 12.5g
- **Carbs:** 0g
- **Fat:** 12g
- *Insight:* Good protein, moderate fat. Whole wheat roti adds fiber. Low carb overall.

### 13. Bhindi (Okra) Sabzi with 1 Roti
- **Calories:** 60
- **Protein:** 0g
- **Carbs:** 0g
- **Fat:** 7g
- *Insight:* Bhindi is high in fiber, roti adds complex carbs. Protein is low—add lentils or yogurt for balance.

### 14. Boiled Egg & Tomato Sandwich (Whole Wheat)
- **Calories:** 270
- **Protein:** 5g
- **Carbs:** 30g
- **Fat:** 14g
- *Insight:* Balanced with emphasis on carbs. Eggs provide protein. Could use 1 egg + 2 whites for higher protein.

### 15. Mixed Lentil Daal with Cucumber Salad
- **Calories:** 0 
- *Note:* Should have carbs, protein (~120 kcal, 5g protein/serving)
- *Insight:* Good fiber, plant protein. Add brown rice for a fuller meal.

### 16. Chicken Shorba (Clear Soup) with Grilled Veggies
- **Calories:** 200
- **Protein:** 25g
- **Carbs:** 0g
- **Fat:** 10g
- *Insight:* Very high protein for low cals. Good meal for muscle preservation during weight loss.

### 17. Vegetable Egg White Omelette + Whole Wheat Toast
- **Calories:** 150
- **Protein:** 0g
- **Carbs:** 5g
- **Fat:** 14g
- *Insight:* Very low protein (should be 8-10g); probably an underestimate. Add more egg whites for protein. Good combination.

### 18. Tinda Curry with 1 Roti
- **Calories:** 60
- **Protein:** 0g
- **Carbs:** 0g
- **Fat:** 7g
- *Insight:* Low cal, light meal. Low protein; combine with dal for balance.

### 19. Grilled Fish Fillet with Sauteed Spinach
- **Calories:** 150
- **Protein:** 0g
- **Carbs:** 5g
- **Fat:** 14g
- *Insight:* Fish is a lean protein source. Should yield about 20g protein per serving. Add lemon for vitamin C.

### 20. Lauki Curry with 1 Roti
- **Calories:** 60
- **Protein:** 0g
- **Carbs:** 0g
- **Fat:** 7g
- *Insight:* Light on protein. Lauki is great for volume/low-cal diets. Pair with daal or yogurt.

### 21. Grilled Fish Tikka with Mixed Vegetables
- **Calories:** 30
- **Protein:** 0g
- **Carbs:** 5g
- **Fat:** 0g
- *Insight:* Should be higher in protein (~15g+ per serving), very low carbs. Great for keto/low-carb.

---

## General Insights and Suggestions

**Calorie Content:**
- Most meals are under 250 kcal per serving; suitable for weight management.

**Macronutrient Balance:**
- Several recipes are low in protein (vegetarian options especially).
- Fats are moderate; keep oils measured.
- Carbs are mostly complex and fiber-rich.

**Micronutrient Considerations:**
- Wide variety of vegetables = good vitamin and mineral coverage.
- Include citrus bell peppers, spinach, and yogurt to boost Vitamin C, iron, and calcium.

**Dietary Compliance:**
- Many dishes suit low-carb, high-protein, and diabetes-friendly diets.
- Some vegetarian options can easily be made high-protein with the addition of legumes, paneer, or yogurt.

**Suggestions for Improvement:**
1. **Increase Protein:** Add lentils/beans, tofu/paneer, eggs, or lean meat to vegetarian options.
2. **Balance Fats:** Use healthy fats like olive oil; avoid ghee or heavy frying.
3. **Boost Fiber:** Use whole grains (brown rice, whole wheat), add more veggies.
4. **Micronutrients:** Add greens, seeds/nuts for omega-3 and minerals.
5. **Variety:** Rotate protein sources (fish, chicken, beans, lentils) and veggies.

Let me know if you want more details for any specific recipe or need tailored dietary advice!

================================================================================
SHOPPING LIST
================================================================================

PRODUCE:
  • Onion
  • Tomato
  • Cucumber
  • Mint leaves
  • Spinach
  • Carrot
  • Green chili
  • Coriander leaves
  • Lemon
  • Potato
  • Mixed salad greens
  • Cauliflower
  • Bhindi (Okra)
  • Tinda
  • Bottle gourd (Lauki)
  • Mixed vegetables (peas, carrots, beans, corn)
  • Ginger
  • Garlic
  • Capsicum (Bell pepper)
  • Fresh fruits (seasonal, as per parfait)

PROTEIN:
  • Moong dal
  • Masoor dal
  • Chickpeas (chana)
  • Eggs
  • Paneer (low-fat)
  • Lean minced beef or chicken
  • Chicken breast/thigh (for kebab & curry)
  • Fish fillet (firm white fish)

DAIRY:
  • Low-fat yogurt
  • Low-fat milk

PANTRY:
  • Poha (flattened rice)
  • Rolled oats
  • Brown rice
  • Whole wheat flour (for roti)
  • Whole wheat bread
  • Olive oil or light cooking oil
  • Turmeric powder
  • Red chili powder
  • Cumin seeds
  • Black pepper
  • Chaat masala
  • Salt
  • Garam masala
  • Coriander powder

OTHER:
  • Toothpicks/skewers for kebabs (if required)

================================================================================
COOKING TIPS
================================================================================

Here are some helpful general cooking tips for each of these dishes:

1. Vegetable Egg White Omelette with Whole Wheat Toast
   - Whisk egg whites thoroughly for a fluffier omelette.
   - Use non-stick pans and a little olive oil or cooking spray to prevent sticking.
   - Finely chop vegetables (like spinach, tomatoes, onions, peppers) for even and quick cooking.
   - Toast the whole wheat bread lightly for crunch and to avoid sogginess from steam.

2. Grilled Chicken Salad with Yogurt Mint Dressing
   - Marinate chicken in advance with a little lemon, salt, pepper, and herbs for juicier, tastier meat.
   - Grill chicken until juicy but cooked through—rest before slicing to retain juices.
   - For the dressing, use fresh mint and whisk with yogurt, a bit of lemon, salt, and pepper for freshness.
   - Toss salad just before serving to keep greens crisp.

3. Lauki (Bottle Gourd) Curry with 1 Roti
   - Cut lauki evenly to ensure uniform cooking.
   - Add a pinch of turmeric, ginger, and green chili for flavor lift.
   - Let the curry simmer gently; overcooking can turn lauki mushy.
   - Keep your roti dough covered while rolling to keep it from drying out.

4. Dahi Poha (Flattened Rice with Yogurt and Vegetables)
   - Rinse poha gently and drain well; don’t over-soak or it will get mushy.
   - Use chilled yogurt for freshness and crunch.
   - Add grated carrots, cucumber, and pomegranate seeds for added texture and flavor.
   - Season with roasted cumin, black salt, and a squeeze of lemon for zing.

5. Bhuna Keema (Lean Minced Beef/Chicken) with Salad
   - Cook the mince on medium-high to get a good 'bhuna' (roasted) flavor.
   - Use onions, ginger, garlic, and tomatoes as a base for a rich, flavorful masala.
   - Cook off excess moisture so the keema is dry but moist.
   - Pair with a fresh salad—onion, cucumber, mint, and lemon is classic.

6. Moong Masoor Dal with Brown Rice (Small Portion)
   - Wash and soak lentils for 10-20 minutes for faster cooking and better texture.
   - Add a tadka (tempering) of cumin, garlic, and hing (asafoetida) at the end for added aroma.
   - Simmer gently so the dal is soft but not mushy.
   - Serve with brown rice for extra fiber and nutty flavor.

If you’d like specific cooking steps or have questions about one dish, let me know!
...
```

## Why Multi-Agent?

Instead of one big agent trying to do everything, this uses specialized agents. Each one is really good at its specific task. The meal planner focuses on creating balanced plans, the nutrition agent knows how to analyze macros, etc. This makes the system:

- More reliable (each agent is focused)
- Easier to debug (you know which agent failed)
- Easier to extend (just add a new agent)
- More maintainable (smaller, focused code)

## Limitations & Future Work

Right now it uses a simple in-memory recipe database with 5 sample recipes. In production, you'd want to:

- Connect to a real recipe API (Spoonacular, Edamam)
- Use a proper nutrition API for accurate calculations
- Add a database for storing recipes and meal plans
- Integrate with grocery delivery services
- Add more specialized agents (budget analysis, leftover suggestions, etc.)

## Contributing

Feel free to fork and extend! Some ideas:
- Add more recipe sources
- Create new specialized agents
- Improve the nutrition calculations
- Add support for dietary restrictions
- Build a web interface

## License

MIT

## Credits

Built with [openai-agents-python](https://github.com/openai/openai-agents-python) - a great framework for building multi-agent systems.
