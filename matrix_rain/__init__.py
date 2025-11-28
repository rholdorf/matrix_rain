"""
Matrix Rain Terminal Effect

A modular Python implementation recreating the iconic Matrix digital rain effect
from the 1999 film "The Matrix", designed for terminal environments.

Research-based implementation featuring:
- Half-width katakana character set
- Bright white head with green trailing fade
- Character mutation every 3 frames
- Variable column speeds and lengths
- Highlighted runner glyphs (20% of columns)

Usage:
    from matrix_rain import main
    main.run()

Or run directly:
    python -m matrix_rain.main
"""

from . import main

__version__ = "1.0.0"
__all__ = ["main"]


def run() -> None:
    """
    Entry point for running the Matrix rain effect.

    Convenience function that delegates to main.run().
    """
    main.run()
