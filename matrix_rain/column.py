"""
Column class representing a single falling rain column.

Each column maintains its state including position, speed, trail characters,
and mutation behavior.
"""

import itertools
import random
from dataclasses import dataclass
from typing import Final

from . import characters
from . import config


@dataclass(slots=True)
class CharacterCell:
    """
    A single character cell in a column trail.

    Research: "Some strings consist entirely of changing glyphs while
    others have static characters"

    Using __slots__ to reduce memory overhead (important for many instances).
    """

    char: str
    is_mutating: bool  # Whether this character changes every 3 frames

    def mutate(self) -> None:
        """Change this character to a new random one."""
        if self.is_mutating:
            self.char = characters.get_random_char()


class Column:
    """
    Represents a single falling rain column.

    Research findings:
    - Columns fall at variable speeds (5-20 rows/second, time-based)
    - Trail lengths vary (7-20 characters)
    - 20% of columns have highlighted runner glyphs
    - Characters mutate every 3 frames (synchronized globally)

    Using __slots__ to reduce memory overhead.
    """

    __slots__ = ('x', 'terminal_height', 'speed', 'length', 'y', 'trail',
                 'is_highlighted', 'highlight_position')

    def __init__(self, x: int, terminal_height: int):
        """
        Initialize a new column.

        Args:
            x: Horizontal position (column number)
            terminal_height: Height of terminal (for lifecycle management)
        """
        self.x = x
        self.terminal_height = terminal_height

        # Random speed from research parameters
        self.speed = random.uniform(config.MIN_SPEED, config.MAX_SPEED)

        # Random trail length from research parameters
        self.length = random.randint(config.MIN_TRAIL_LENGTH, config.MAX_TRAIL_LENGTH)

        # Position tracking (can start above screen)
        # Research: "Invisible characters precede visible glyphs"
        self.y = random.uniform(-self.length, 0)  # Start position (can be negative)

        # Initialize trail characters
        # Research: "40-60% of character positions as mutating"
        self.trail: list[CharacterCell] = []
        for _ in range(self.length):
            char = characters.get_random_char()
            is_mutating = random.random() < config.MUTATING_CHAR_PROBABILITY
            self.trail.append(CharacterCell(char, is_mutating))

        # Highlighted runner glyph support
        # Research: "1 in 5 strings (20%) feature a highlighted glyph"
        self.is_highlighted = random.random() < config.HIGHLIGHTED_COLUMN_PROBABILITY
        if self.is_highlighted:
            # Highlight position in middle third of trail (not head)
            self.highlight_position = random.randint(self.length // 3, 2 * self.length // 3)
        else:
            self.highlight_position = -1

    def update(self, delta_time: float) -> None:
        """
        Update column position based on elapsed time.

        Args:
            delta_time: Time elapsed since last update (in seconds)
        """
        # Move down by speed (rows per second) × time elapsed
        # This ensures consistent speed regardless of actual FPS
        self.y += self.speed * delta_time

    def mutate_characters(self) -> None:
        """
        Mutate all mutating characters in the trail.

        Research: "All changing glyphs change on the same frame"
        Called globally every 3 frames.
        """
        for cell in self.trail:
            cell.mutate()

    def is_alive(self) -> bool:
        """
        Check if column should still be rendered.

        Research: "Columns disappear when their length exceeds
        approximately 2x screen height"

        Returns:
            True if column is still visible or will be visible
        """
        # Column is dead when its tail has passed off screen
        tail_y = self.y - self.length
        return tail_y < self.terminal_height

    def get_visible_characters(self) -> list[tuple[int, str, bool]]:
        """
        Get list of visible characters with their screen positions.

        Returns:
            List of (row, character, is_highlighted) tuples for visible chars
        """
        visible = []
        head_y = int(self.y)

        for i, cell in enumerate(self.trail):
            char_y = head_y - i

            # Only include if on screen
            if 0 <= char_y < self.terminal_height:
                is_highlighted = (self.is_highlighted and i == self.highlight_position)
                visible.append((char_y, cell.char, is_highlighted))

        return visible

    def get_render_data(self) -> list[tuple[int, int, str, int, bool]]:
        """
        Get complete rendering data for this column.

        Returns:
            List of (row, col, char, trail_position, is_highlighted) tuples
            where trail_position is distance from head (0 = head)
        """
        render_data = []
        head_y = int(self.y)

        for i, cell in enumerate(self.trail):
            char_y = head_y - i

            # Only include if on screen
            if 0 <= char_y < self.terminal_height:
                is_highlighted = (self.is_highlighted and i == self.highlight_position)
                render_data.append((char_y, self.x, cell.char, i, is_highlighted))

        return render_data


class ColumnManager:
    """
    Manages all active columns on screen.

    Handles spawning, updating, and cleanup of columns.

    Using __slots__ to reduce memory overhead.
    """

    __slots__ = ('terminal_width', 'terminal_height', 'columns', 'frame_count')

    def __init__(self, terminal_width: int, terminal_height: int):
        """
        Initialize column manager.

        Args:
            terminal_width: Width of terminal
            terminal_height: Height of terminal
        """
        self.terminal_width = terminal_width
        self.terminal_height = terminal_height
        self.columns: dict[int, list[Column]] = {x: [] for x in range(terminal_width)}
        self.frame_count = 0

    def update(self, delta_time: float) -> None:
        """
        Update all columns.

        Args:
            delta_time: Time since last frame
        """
        self.frame_count += 1

        # Update existing columns
        for x in range(self.terminal_width):
            # Update each column in this x position
            for column in self.columns[x]:
                column.update(delta_time)

            # Remove dead columns
            self.columns[x] = [col for col in self.columns[x] if col.is_alive()]

            # Spawn new columns based on probability
            # Research: "~2.5% chance per frame"
            if random.random() < config.SPAWN_PROBABILITY:
                self.spawn_column(x)

        # Global character mutation every 3 frames
        # Research: "Glyphs remain static for exactly 3 frames, then change"
        if self.frame_count % config.MUTATION_INTERVAL_FRAMES == 0:
            self.mutate_all_characters()

    def spawn_column(self, x: int) -> None:
        """
        Spawn a new column at the given x position.

        Args:
            x: Horizontal position
        """
        # Research allows multiple raindrops per column
        # Limit to 2-3 to avoid excessive density
        if len(self.columns[x]) < 3:
            column = Column(x, self.terminal_height)
            self.columns[x].append(column)

    def mutate_all_characters(self) -> None:
        """
        Trigger character mutation for all columns.

        Research: "All changing glyphs change on the same frame"
        """
        for x in range(self.terminal_width):
            for column in self.columns[x]:
                column.mutate_characters()

    def get_all_render_data(self) -> list[tuple[int, int, str, int, bool]]:
        """
        Get rendering data for all columns.

        Returns:
            List of (row, col, char, trail_position, is_highlighted) tuples
        """
        # Optimized: Use itertools.chain to flatten without intermediate lists
        return list(itertools.chain.from_iterable(
            column.get_render_data()
            for x in range(self.terminal_width)
            for column in self.columns[x]
        ))

    def resize(self, new_width: int, new_height: int) -> None:
        """
        Handle terminal resize.

        Args:
            new_width: New terminal width
            new_height: New terminal height
        """
        old_width = self.terminal_width
        self.terminal_width = new_width
        self.terminal_height = new_height

        # Adjust columns dict
        if new_width > old_width:
            # Add new columns
            for x in range(old_width, new_width):
                self.columns[x] = []
        elif new_width < old_width:
            # Remove excess columns
            for x in range(new_width, old_width):
                if x in self.columns:
                    del self.columns[x]

        # Update terminal height for existing columns
        for x in range(min(new_width, old_width)):
            for column in self.columns[x]:
                column.terminal_height = new_height
