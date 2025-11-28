"""
Main application entry point and main loop for Matrix rain effect.

Handles initialization, main rendering loop, input handling, and graceful shutdown.
"""

import select
import signal
import sys
import termios
import time
import tty
from typing import NoReturn

from . import characters
from . import config
from . import column
from . import renderer


class MatrixRain:
    """
    Main application class for Matrix rain effect.

    Manages the main loop, column updates, rendering, and user input.

    Using __slots__ to reduce memory overhead.
    """

    __slots__ = ('running', 'renderer', 'column_manager', 'use_256_color',
                 'old_terminal_settings')

    def __init__(self):
        """Initialize the Matrix rain application."""
        self.running = False
        self.renderer: renderer.TerminalRenderer | None = None
        self.column_manager: column.ColumnManager | None = None
        self.use_256_color = False
        self.old_terminal_settings = None

    def setup(self) -> bool:
        """
        Set up terminal and initialize components.

        Returns:
            True if setup successful, False otherwise
        """
        # Get terminal size
        width, height = renderer.get_terminal_size()

        # Validate terminal size
        is_valid, error_msg = renderer.validate_terminal_size(width, height)
        if not is_valid:
            print(f"Error: {error_msg}", file=sys.stderr)
            print(f"Please resize your terminal to at least {config.MIN_TERMINAL_WIDTH}x{config.MIN_TERMINAL_HEIGHT}", file=sys.stderr)
            return False

        # Detect 256-color support
        self.use_256_color = renderer.detect_256_color_support()

        # Initialize character pool
        # Try Unicode first, fallback to ASCII if needed
        try:
            characters.initialize_pool(use_unicode=True)
            # Test that Unicode works
            test_char = characters.get_random_char()
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Fallback to ASCII
            characters.initialize_pool(use_unicode=False)

        # Initialize renderer
        self.renderer = renderer.TerminalRenderer(width, height, self.use_256_color)
        self.renderer.initialize_terminal()

        # Initialize column manager
        self.column_manager = column.ColumnManager(width, height)

        # Set up keyboard input for 'q' to quit
        self.setup_input()

        return True

    def setup_input(self) -> None:
        """Set up non-blocking keyboard input."""
        # Save current terminal settings
        self.old_terminal_settings = termios.tcgetattr(sys.stdin)
        # Set terminal to raw mode for immediate key detection
        tty.setcbreak(sys.stdin.fileno())

    def check_for_quit(self) -> bool:
        """
        Check if user pressed 'q' to quit.

        Returns:
            True if 'q' was pressed, False otherwise
        """
        # Use select to check if input is available (non-blocking)
        if select.select([sys.stdin], [], [], 0)[0]:
            char = sys.stdin.read(1)
            if char.lower() == 'q':
                return True
        return False

    def cleanup(self) -> None:
        """Clean up and restore terminal state."""
        # Restore terminal settings
        if self.old_terminal_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_terminal_settings)

        # Restore renderer terminal state
        if self.renderer:
            self.renderer.restore_terminal()

    def handle_interrupt(self, signum: int, frame) -> None:
        """
        Handle keyboard interrupt (Ctrl+C).

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        self.running = False

    def run(self) -> None:
        """
        Main loop for Matrix rain effect.

        Research: "Target 20fps refresh rate with 50ms delay between frames"
        Press 'q' or Ctrl+C to exit gracefully.
        """
        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, self.handle_interrupt)

        # Setup
        if not self.setup():
            return

        try:
            self.running = True
            last_time = time.time()

            while self.running:
                # Check for 'q' key to quit
                if self.check_for_quit():
                    self.running = False
                    break

                # Calculate delta time
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time

                # Update column states
                if self.column_manager:
                    self.column_manager.update(delta_time)

                # Clear buffer
                if self.renderer:
                    self.renderer.clear_buffer()

                # Get all render data from columns
                if self.column_manager:
                    render_data = self.column_manager.get_all_render_data()

                    # Update renderer buffer
                    if self.renderer:
                        for row, col, char, trail_pos, is_highlighted in render_data:
                            self.renderer.set_character(
                                row, col, char, trail_pos, is_highlighted
                            )

                # Render to screen
                if self.renderer:
                    self.renderer.render()

                # Frame rate limiting
                # Research: "50ms delay between frames (1000ms/20fps)"
                time.sleep(config.FRAME_DELAY)

        except Exception as e:
            # Ensure cleanup happens even on unexpected errors
            self.cleanup()
            print(f"\nError: {e}", file=sys.stderr)
            raise
        finally:
            # Always restore terminal
            self.cleanup()


def run() -> None:
    """
    Entry point for running the Matrix rain effect.

    Called from launcher script or package import.
    """
    app = MatrixRain()
    app.run()


if __name__ == "__main__":
    run()
