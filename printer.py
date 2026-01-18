"""Printer for displaying meal prep progress and results."""

from typing import Any

from rich.console import Console, Group
from rich.live import Live
from rich.spinner import Spinner


class Printer:
    """Printer for displaying meal prep workflow progress."""

    def __init__(self, console: Console) -> None:
        self.console = console
        self.live = Live(console=console)
        self.items: dict[str, tuple[str, bool]] = {}
        self.hide_done_ids: set[str] = set()
        self.live.start()

    def end(self) -> None:
        """Stop the live display."""
        self.live.stop()

    def hide_done_checkmark(self, item_id: str) -> None:
        """Hide the checkmark for a specific item."""
        self.hide_done_ids.add(item_id)

    def update_item(
        self, item_id: str, content: str, is_done: bool = False, hide_checkmark: bool = False
    ) -> None:
        """Update an item's content and status."""
        self.items[item_id] = (content, is_done)
        if hide_checkmark:
            self.hide_done_ids.add(item_id)
        self.flush()

    def mark_item_done(self, item_id: str) -> None:
        """Mark an item as done."""
        if item_id in self.items:
            self.items[item_id] = (self.items[item_id][0], True)
            self.flush()

    def flush(self) -> None:
        """Render all items."""
        renderables: list[Any] = []
        for item_id, (content, is_done) in self.items.items():
            if is_done:
                prefix = "✅ " if item_id not in self.hide_done_ids else ""
                renderables.append(prefix + content)
            else:
                renderables.append(Spinner("dots", text=content))
        self.live.update(Group(*renderables))
