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

```
MEAL PLAN
================================================================================

Day 1:
  Breakfast: Quinoa Bowl with Roasted Vegetables (2 servings)
  Lunch: Chicken Stir Fry (2 servings)
  Dinner: Grilled Salmon with Vegetables (2 servings)

NUTRITION ANALYSIS
================================================================================
[Detailed breakdown of calories, macros, and dietary compliance...]

SHOPPING LIST
================================================================================
PRODUCE:
  • 2 bell peppers, sliced
  • 1 onion, sliced
  • 2 cups mixed vegetables

PROTEIN:
  • 2 chicken breasts, sliced
  • 4 salmon fillets

COOKING TIPS
================================================================================
• Cook pasta 1 minute less than package directions for al dente texture
• Let meat rest for 5-10 minutes after cooking for juicier results
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
