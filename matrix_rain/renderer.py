"""
Terminal rendering and ANSI handling for Matrix rain effect.

Manages screen buffer, cursor control, and efficient terminal updates.
"""

import os
import sys
from typing import Final

from . import config


class TerminalRenderer:
    """
    Handles efficient terminal rendering with ANSI codes.

    Research findings:
    - Use ANSI cursor positioning to avoid flicker
    - Update only changed positions (dirty tracking)
    - 256-color mode for smooth gradients

    Using __slots__ to reduce memory overhead.
    """

    __slots__ = ('width', 'height', 'use_256_color', 'buffer', 'prev_buffer')

    def __init__(self, width: int, height: int, use_256_color: bool = True):
        """
        Initialize terminal renderer.

        Args:
            width: Terminal width in characters
            height: Terminal height in characters
            use_256_color: Whether to use 256-color mode
        """
        self.width = width
        self.height = height
        self.use_256_color = use_256_color

        # Screen buffer: stores (char, color_code) for each position
        # Initialize with empty spaces
        self.buffer: list[list[tuple[str, str]]] = [
            [(" ", "")] * width for _ in range(height)
        ]

        # Previous buffer for dirty tracking
        self.prev_buffer: list[list[tuple[str, str]]] = [
            [(" ", "")] * width for _ in range(height)
        ]

    def initialize_terminal(self) -> None:
        """
        Initialize terminal for rendering.

        Research: "Hide cursor", "Clear screen", "Enter alternate buffer"
        """
        # Enter alternate screen buffer (preserves user's terminal content)
        sys.stdout.write(config.ANSI_ALTERNATE_BUFFER)
        # Clear screen
        sys.stdout.write(config.ANSI_CLEAR_SCREEN)
        # Hide cursor
        sys.stdout.write(config.ANSI_HIDE_CURSOR)
        # Move to home
        sys.stdout.write(config.ANSI_HOME)
        sys.stdout.flush()

    def restore_terminal(self) -> None:
        """
        Restore terminal to normal state.

        Called on exit to clean up.
        """
        # Show cursor
        sys.stdout.write(config.ANSI_SHOW_CURSOR)
        # Reset colors
        sys.stdout.write(config.ANSI_RESET)
        # Exit alternate screen buffer
        sys.stdout.write(config.ANSI_NORMAL_BUFFER)
        sys.stdout.flush()

    def clear_buffer(self) -> None:
        """Clear the screen buffer (fill with spaces)."""
        # Optimized: Use list comprehension instead of nested loops
        empty_cell = (" ", "")
        self.buffer = [[empty_cell] * self.width for _ in range(self.height)]

    def set_character(
        self, row: int, col: int, char: str, trail_position: int, is_highlighted: bool
    ) -> None:
        """
        Set a character in the buffer with appropriate color.

        Args:
            row: Row position (0-based)
            col: Column position (0-based)
            char: Character to display
            trail_position: Distance from column head (0 = head)
            is_highlighted: Whether this is a highlighted runner glyph
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            if is_highlighted:
                color = config.get_highlighted_color(trail_position, self.use_256_color)
            else:
                color = config.get_color_for_position(trail_position, self.use_256_color)

            self.buffer[row][col] = (char, color)

    def render(self) -> None:
        """
        Render the buffer to the terminal.

        Research: "Update only changed positions" for efficiency.
        """
        output = []
        current_color = ""  # Track current color to avoid redundant resets

        for row in range(self.height):
            for col in range(self.width):
                current = self.buffer[row][col]
                previous = self.prev_buffer[row][col]

                # Only update if changed (dirty tracking)
                if config.USE_DIRTY_TRACKING and current == previous:
                    continue

                char, color = current

                # Move cursor to position (1-based indexing for ANSI)
                output.append(f"\033[{row + 1};{col + 1}H")

                # Only change color if different from current
                if color != current_color:
                    if color:
                        output.append(color)
                        current_color = color
                    else:
                        # Need to reset to default
                        output.append(config.ANSI_RESET)
                        current_color = ""

                # Write character
                output.append(char)

        # Reset color at end if needed
        if current_color:
            output.append(config.ANSI_RESET)

        # Write all updates in single operation
        if output:
            sys.stdout.write("".join(output))
            sys.stdout.flush()

        # Update previous buffer (optimized: list comprehension)
        self.prev_buffer = [row[:] for row in self.buffer]

    def resize(self, new_width: int, new_height: int) -> None:
        """
        Handle terminal resize.

        Args:
            new_width: New terminal width
            new_height: New terminal height
        """
        self.width = new_width
        self.height = new_height

        # Recreate buffers with new dimensions
        self.buffer = [
            [(" ", "")] * new_width for _ in range(new_height)
        ]
        self.prev_buffer = [
            [(" ", "")] * new_width for _ in range(new_height)
        ]

        # Clear and redraw
        sys.stdout.write(config.ANSI_CLEAR_SCREEN)
        sys.stdout.write(config.ANSI_HOME)
        sys.stdout.flush()


def get_terminal_size() -> tuple[int, int]:
    """
    Get current terminal size.

    Returns:
        Tuple of (width, height) in characters

    Raises:
        RuntimeError: If terminal size cannot be determined
    """
    try:
        # Try using os.get_terminal_size (Python 3.3+)
        size = os.get_terminal_size()
        return size.columns, size.lines
    except (AttributeError, OSError):
        # Fallback: try using tput command
        try:
            import subprocess

            cols = subprocess.check_output(["tput", "cols"]).decode().strip()
            lines = subprocess.check_output(["tput", "lines"]).decode().strip()
            return int(cols), int(lines)
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            # Last resort: return standard size
            return 80, 24


def validate_terminal_size(width: int, height: int) -> tuple[bool, str]:
    """
    Validate that terminal size meets minimum requirements.

    Args:
        width: Terminal width
        height: Terminal height

    Returns:
        Tuple of (is_valid, error_message)
    """
    if width < config.MIN_TERMINAL_WIDTH:
        return False, f"Terminal width ({width}) is less than minimum ({config.MIN_TERMINAL_WIDTH})"

    if height < config.MIN_TERMINAL_HEIGHT:
        return False, f"Terminal height ({height}) is less than minimum ({config.MIN_TERMINAL_HEIGHT})"

    return True, ""


def detect_256_color_support() -> bool:
    """
    Detect if terminal supports 256-color mode.

    Returns:
        True if 256-color mode is likely supported
    """
    # Check TERM environment variable
    term = os.environ.get("TERM", "")

    # Common 256-color terminal types
    color256_terms = [
        "256color",
        "xterm-256color",
        "screen-256color",
        "tmux-256color",
    ]

    return any(t in term for t in color256_terms)
