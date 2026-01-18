"""Main entry point for the meal prep system example."""

import asyncio

from examples.auto_mode import input_with_fallback

# Import config to set up API key
from . import config  # noqa: F401

from .manager import MealPrepManager


async def main() -> None:
    """Run the meal prep system."""
    query = input_with_fallback(
        "What would you like help with for meal prep? "
        "(e.g., 'Plan meals for 3 days, vegetarian, quick recipes'): ",
        "Plan meals for 3 days with a mix of vegetarian and protein options, quick to prepare",
    )
    manager = MealPrepManager()
    await manager.run(query)


if __name__ == "__main__":
    asyncio.run(main())
