# Matrix Rain Terminal Effect

A modular Python implementation recreating the iconic Matrix digital rain effect from the 1999 film "The Matrix", designed specifically for terminal environments.

## Overview

This implementation faithfully recreates the visual characteristics of the original Matrix digital rain effect within the constraints of a terminal running zsh or other modern shells. The effect features:

- **Authentic character set**: Half-width katakana characters (ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ) plus numerals 0-9
- **Distinctive color scheme**: Bright white heads fading through shades of green, inspired by old IBM CRT monitors
- **Dynamic character mutation**: Characters shimmer and change every 3 frames with synchronized global updates
- **Variable column behavior**: Random speeds (5-20 rows/second, time-based), lengths (7-20 characters), and spawn timing
- **Highlighted runner glyphs**: Approximately 20% of columns feature brighter mid-trail characters
- **Smooth rendering**: 20fps target with efficient dirty-region tracking to minimize flicker

## Requirements

- Python 3.10 or higher (for type hints)
- Terminal with ANSI color support
- Unicode-capable font with Japanese character support (for authentic appearance)
- Minimum terminal size: 40x20 characters

### Optional but Recommended

- 256-color terminal support for smoother color gradients
- Modern terminal emulator (iTerm2, Terminal.app, Alacritty, etc.)

## Installation

No installation required - this is a standalone Python application using only the standard library.

Simply clone or download the repository:

```bash
cd /Users/rui/matrix_rain
```

## Usage

### Run with Python

```bash
python run_matrix.py
```

Or run as a module:

```bash
python -m matrix_rain.main
```

### Make Executable (Unix/Linux/macOS)

```bash
chmod +x run_matrix.py
./run_matrix.py
```

### Exit the Effect

Press `q` or `Ctrl+C` to cleanly exit and restore your terminal.

## Architecture

The implementation follows a modular design with clear separation of concerns:

- **config.py** - All configuration constants and parameters derived from research findings
- **characters.py** - Character pool management and random selection logic
- **column.py** - Column state management, movement, and lifecycle
- **renderer.py** - Terminal rendering engine with ANSI control sequences
- **main.py** - Application entry point and main loop
- **__init__.py** - Package initialization and public API

### Key Design Decisions

1. **Approach B Implementation**: Uses moving column objects rather than a fixed grid with illumination waves. This is simpler to implement while still achieving visual authenticity.

2. **Dirty Region Tracking**: Only updates changed character positions each frame to minimize terminal flicker and improve performance.

3. **256-Color Fallback**: Automatically detects terminal capabilities and falls back to 16-color mode if needed.

4. **Unicode Fallback**: Attempts to use authentic katakana characters, falls back to ASCII if Unicode support is unavailable.

5. **Alternate Screen Buffer**: Uses ANSI alternate screen buffer to preserve user's terminal content during execution.

## Research Attribution

This implementation is based on extensive research documented in:
`.prompts/001-matrix-rain-research/matrix-rain-research.md`

Key research findings incorporated:

- **Character Set**: Half-width katakana from Unicode range FF65-FF9F, as designed by Simon Whiteley for the original film
- **Color Gradient**: White-to-dark-green fade inspired by IBM CRT monitors
- **Timing Parameters**: 20fps refresh rate, 3-frame character mutation interval
- **Spawn Behavior**: 2.5% spawn probability per column per frame
- **Column Properties**: Speed range 5-20 rows/second (time-based), length range 7-20 characters
- **Mutation Strategy**: 50% of character positions are mutating, synchronized globally
- **Highlighted Glyphs**: 20% of columns feature brighter mid-trail characters

## Film Credits

The Matrix digital rain effect was created for the 1999 film "The Matrix" by:

- **Designer**: Simon Whiteley - Created the custom typeface and visual design
- **Implementation**: Justen Marshall - Implemented the vertical cascading effect
- **Software**: Softimage 3D animation, Mental Ray renderer
- **Inspiration**: IBM CRT monitor aesthetics

This terminal implementation is an homage to their iconic work.

## Troubleshooting

### Characters Don't Display Correctly

Your terminal may not have proper Unicode support or Japanese fonts installed. The application should automatically fall back to ASCII characters (A-Z, 0-9, symbols).

To force ASCII mode, modify `matrix_rain/main.py` line 52 to:
```python
characters.initialize_pool(use_unicode=False)
```

### Colors Look Wrong

Ensure your terminal supports ANSI colors. For best results, use a terminal with 256-color support. Check your TERM environment variable:

```bash
echo $TERM
```

Should include "256color" (e.g., "xterm-256color").

### Screen Flickers

Some terminal emulators have slower rendering. Try:
- Using a modern terminal emulator
- Reducing terminal size
- Checking if your terminal supports alternate screen buffer

### Terminal Too Small Error

Resize your terminal to at least 40 columns by 20 rows.

## Performance Notes

The application targets 20fps (50ms frame delay) for a balance between visual smoothness and CPU efficiency. On typical modern hardware with a standard-sized terminal (80x24), CPU usage should be minimal.

For very large terminals (200x60+), consider that:
- More columns = more state to track
- Dirty region tracking minimizes rendering cost
- Overall performance remains acceptable on modern systems

## License

This is a research and educational implementation recreating the visual effect from "The Matrix" (1999). All rights to the original Matrix digital rain effect belong to Warner Bros. and the creators.

## Version

1.0.0 - Initial implementation based on research findings
