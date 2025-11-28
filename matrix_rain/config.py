"""
Configuration constants and parameters for Matrix rain effect.

All values derived from research findings documented in:
.prompts/001-matrix-rain-research/matrix-rain-research.md
"""

from typing import Final

# Character Set (from research: half-width katakana + numerals)
# Research: "Half-width katakana characters (mirrored/reversed)"
# Using Unicode FF65-FF9F range for terminal compatibility
KATAKANA_CHARS: Final[str] = "ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ"
NUMERAL_CHARS: Final[str] = "0123456789"
LATIN_CHARS: Final[str] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
SYMBOL_CHARS: Final[str] = ".,;:!?+-=*/"

# Complete character pool
# Research: "katakana set plus numerals 0-9 for authentic appearance"
CHARACTER_POOL: Final[str] = KATAKANA_CHARS + NUMERAL_CHARS

# Alternative ASCII-only pool for terminals without Unicode support
ASCII_POOL: Final[str] = NUMERAL_CHARS + LATIN_CHARS + SYMBOL_CHARS

# Frame Rate and Timing
# Research: "Target 20fps refresh rate" "50ms delay between frames"
TARGET_FPS: Final[int] = 20
FRAME_DELAY: Final[float] = 1.0 / TARGET_FPS  # 0.05 seconds = 50ms

# Character Mutation Timing
# Research: "Glyphs remain static for exactly 3 frames, then change"
MUTATION_INTERVAL_FRAMES: Final[int] = 3

# Static vs Dynamic Character Distribution
# Research: "Randomly designate 40-60% of character positions as mutating"
MUTATING_CHAR_PROBABILITY: Final[float] = 0.5  # 50% chance

# Column Spawn Parameters
# Research: "Per-column spawn check: ~2.5% chance per frame"
SPAWN_PROBABILITY: Final[float] = 0.025  # 2.5% per frame per column

# Column Speed Parameters
# Research: "Randomize between 1 row/frame (slow) and 2-3 rows/frame (fast)"
# Original research: 20-60 rows/sec, reduced to ~half for better visibility
# Speed is now in rows per second (time-based, FPS-independent)
MIN_SPEED: Final[float] = 5.0   # rows per second (slow columns)
MAX_SPEED: Final[float] = 20.0  # rows per second (fast columns)

# Column Length Parameters
# Research: "Randomize between 7-20 characters at spawn"
MIN_TRAIL_LENGTH: Final[int] = 7
MAX_TRAIL_LENGTH: Final[int] = 20

# Highlighted Runner Glyphs
# Research: "Approximately 1 in 5 strings (20%) feature a highlighted glyph"
HIGHLIGHTED_COLUMN_PROBABILITY: Final[float] = 0.2  # 20% chance

# Screen Coverage
# Research: "Typical coverage is 20-40% of available columns at any moment"
MIN_ACTIVE_COLUMNS_RATIO: Final[float] = 0.20
MAX_ACTIVE_COLUMNS_RATIO: Final[float] = 0.40

# ANSI Color Codes (256-color mode)
# Research: "Use green palette (colors 46→40→34→28→22) for smoother gradient"
# Fallback to 16-color mode if 256-color not available

# 256-color mode green shades (from bright to dark)
COLOR_256_HEAD: Final[int] = 231  # Bright white
COLOR_256_BRIGHT_GREEN: Final[int] = 46  # Bright green
COLOR_256_GREEN: Final[int] = 40  # Medium green
COLOR_256_MID_GREEN: Final[int] = 34  # Mid green
COLOR_256_DARK_GREEN: Final[int] = 28  # Dark green
COLOR_256_DIM_GREEN: Final[int] = 22  # Dim green

# 16-color mode ANSI codes (fallback)
# Research: "bright white for head, then bright green to normal green to dim green"
ANSI_RESET: Final[str] = "\033[0m"
ANSI_BRIGHT_WHITE: Final[str] = "\033[97m"
ANSI_BRIGHT_GREEN: Final[str] = "\033[92m"
ANSI_GREEN: Final[str] = "\033[32m"
ANSI_DIM_GREEN: Final[str] = "\033[2;32m"

# ANSI Terminal Control Codes
ANSI_HIDE_CURSOR: Final[str] = "\033[?25l"
ANSI_SHOW_CURSOR: Final[str] = "\033[?25h"
ANSI_CLEAR_SCREEN: Final[str] = "\033[2J"
ANSI_HOME: Final[str] = "\033[H"
ANSI_ALTERNATE_BUFFER: Final[str] = "\033[?1049h"  # Enter alternate screen
ANSI_NORMAL_BUFFER: Final[str] = "\033[?1049l"  # Exit alternate screen

# Color gradient steps for trail
# Maps trail position to color (0 = head, higher = further down trail)
# Research: "3-4 discrete brightness levels"
COLOR_GRADIENT_256 = [
    COLOR_256_HEAD,         # Position 0: Bright white head
    COLOR_256_BRIGHT_GREEN, # Position 1: Bright green
    COLOR_256_GREEN,        # Positions 2-3: Green
    COLOR_256_MID_GREEN,    # Positions 4-6: Mid green
    COLOR_256_DARK_GREEN,   # Positions 7-10: Dark green
    COLOR_256_DIM_GREEN,    # Positions 11+: Dim green
]

COLOR_GRADIENT_16 = [
    ANSI_BRIGHT_WHITE,  # Position 0: Bright white head
    ANSI_BRIGHT_GREEN,  # Position 1-2: Bright green
    ANSI_GREEN,         # Positions 3-6: Normal green
    ANSI_DIM_GREEN,     # Positions 7+: Dim green
]

# Performance settings
# Research: "Optimize by tracking dirty regions (only redraw changed characters)"
USE_DIRTY_TRACKING: Final[bool] = True

# Terminal size constraints
# Research: "Set minimum size requirements (e.g., 40x20) for usable effect"
MIN_TERMINAL_WIDTH: Final[int] = 40
MIN_TERMINAL_HEIGHT: Final[int] = 20


def get_color_for_position(position: int, use_256_color: bool = True) -> str:
    """
    Get ANSI color code for a given trail position.

    Args:
        position: Distance from column head (0 = head, higher = further back)
        use_256_color: Whether to use 256-color mode (vs 16-color)

    Returns:
        ANSI color code string
    """
    if use_256_color:
        # Map position to gradient index
        if position == 0:
            idx = 0
        elif position == 1:
            idx = 1
        elif position <= 3:
            idx = 2
        elif position <= 6:
            idx = 3
        elif position <= 10:
            idx = 4
        else:
            idx = 5

        color_code = COLOR_GRADIENT_256[idx]
        return f"\033[38;5;{color_code}m"
    else:
        # 16-color mode
        if position == 0:
            return COLOR_GRADIENT_16[0]
        elif position <= 2:
            return COLOR_GRADIENT_16[1]
        elif position <= 6:
            return COLOR_GRADIENT_16[2]
        else:
            return COLOR_GRADIENT_16[3]


def get_highlighted_color(position: int, use_256_color: bool = True) -> str:
    """
    Get brighter color for highlighted runner glyphs.

    Args:
        position: Distance from column head
        use_256_color: Whether to use 256-color mode

    Returns:
        ANSI color code string (one level brighter than normal)
    """
    # Make highlighted glyphs one level brighter than normal trail
    highlight_position = max(0, position - 3)
    return get_color_for_position(highlight_position, use_256_color)
