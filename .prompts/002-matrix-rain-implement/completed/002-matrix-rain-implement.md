# Implementation: Matrix Rain Terminal Effect

<objective>
Build a modular Python implementation that recreates the Matrix digital rain effect in a terminal environment.

Purpose: Produce a visually authentic recreation of the iconic 1999 Matrix effect within the constraints of a terminal running zsh
Output: Multi-module Python application with clean architecture
</objective>

<context>
Research findings: @.prompts/001-matrix-rain-research/matrix-rain-research.md

The research document contains:
- Character set composition and differentiation
- Visual characteristics (brightness, fade patterns, colors)
- Motion parameters (spawn frequency, velocity, column lengths)
- Dynamic behavior (character mutation patterns, static vs dynamic chars)
- Terminal constraint adaptations

Base all implementation decisions on the research findings. Where the research identifies limitations or unknowns, make reasonable choices and document them.
</context>

<requirements>

**Functional Requirements:**
- Render falling character columns in terminal
- Implement bright "head" effect with trailing fade
- Support character mutation during column lifecycle (per research findings)
- Handle column spawn, movement, and lifecycle
- Respond to terminal resize events
- Clean exit on keyboard interrupt (Ctrl+C)

**Visual Requirements:**
- Use character set identified in research
- Implement color/brightness pattern from research (ANSI colors)
- Follow timing parameters from research (spawn rate, speed, mutation)
- Match static vs dynamic character behavior from research
- Achieve visual density similar to original (per research recommendations)

**Technical Requirements:**
- Modular architecture: separate concerns into focused modules
- Clean, readable code with type hints
- Efficient terminal rendering (avoid flicker)
- Cross-platform ANSI support
- Configurable parameters (allow tuning without code changes)

**Quality Requirements:**
- No external dependencies beyond Python standard library
- Robust error handling (terminal size, interrupt, etc.)
- Performance: smooth animation on typical terminal
- Documentation: docstrings for public interfaces
</requirements>

<implementation>

**Architecture:**

Thoroughly analyze the problem and consider multiple approaches before settling on structure. Deeply consider the separation of concerns needed for maintainability.

Recommended module breakdown:
1. `config.py` - Configuration constants and parameters from research
2. `characters.py` - Character set management, selection logic
3. `column.py` - Column class: state, movement, rendering logic
4. `renderer.py` - Terminal rendering, ANSI color handling, screen management
5. `main.py` - Application entry point, main loop, event handling
6. `__init__.py` - Package initialization (can be empty or expose main API)

**Key Design Patterns:**

Follow these patterns from research findings:
- Character selection: Use the specific character set from research
- Brightness implementation: Map research color/brightness to ANSI codes (bright white head → green fade)
- Mutation timing: Follow research findings on which characters change and when
- Column spawn: Implement spawn frequency from research

Avoid these pitfalls:
- Don't use `print()` for animation - it's too slow and causes flicker. Use ANSI cursor positioning instead.
- Don't clear entire screen each frame - update only changed positions
- Don't use `time.sleep()` for timing - it's imprecise. Use frame-based timing with proper delta calculations.
- Don't hardcode magic numbers - put research-based parameters in config

**ANSI Terminal Control:**

Essential codes for smooth rendering:
- `\033[?25l` - Hide cursor
- `\033[?25h` - Show cursor
- `\033[2J` - Clear screen
- `\033[H` - Move cursor to home
- `\033[{row};{col}H` - Move cursor to position
- `\033[38;5;{color}m` - Set 256-color foreground
- `\033[0m` - Reset formatting

Use appropriate green shades (ANSI 256-color palette) for fade effect based on research.

**Performance Considerations:**

For maximum efficiency, structure the main loop to:
1. Calculate delta time since last frame
2. Update all column states in parallel (conceptually)
3. Build render buffer with only changed positions
4. Write buffer to stdout in single operation
5. Target frame rate from research (or 30fps if not specified)
</implementation>

<output>

Create modular structure in current directory:

```
./matrix_rain/
├── __init__.py          - Package initialization
├── config.py            - Configuration and constants from research
├── characters.py        - Character set and selection logic
├── column.py            - Column state and behavior
├── renderer.py          - Terminal rendering and ANSI handling
└── main.py              - Application entry point and main loop

./run_matrix.py          - Simple launcher script
./README.md              - Usage instructions and attribution
```

**File Descriptions:**

- `matrix_rain/__init__.py`: Expose main entry point
- `matrix_rain/config.py`: All configurable parameters (speeds, colors, character sets, spawn rates) derived from research
- `matrix_rain/characters.py`: Character pool management, random selection, head vs trail differentiation
- `matrix_rain/column.py`: Column class with position, velocity, length, mutation logic, rendering state
- `matrix_rain/renderer.py`: TerminalRenderer class - screen buffer, ANSI color codes, cursor control, efficient updates
- `matrix_rain/main.py`: MatrixRain class - main loop, column management, input handling, graceful shutdown
- `run_matrix.py`: Simple `if __name__ == "__main__": from matrix_rain import main; main.run()` launcher
- `README.md`: How to run, what it does, attribution to 1999 Matrix film, research notes

</output>

<verification>

Before declaring complete:

1. **Code Quality:**
   - All modules have docstrings
   - Type hints on functions
   - No obvious performance issues
   - Clean separation of concerns

2. **Functional Testing:**
   - Run `python run_matrix.py` successfully
   - Verify columns appear and fall
   - Verify bright heads with fading trails
   - Verify character mutation (if research indicated it)
   - Verify clean exit on Ctrl+C
   - Test terminal resize handling

3. **Visual Verification:**
   - Check against research findings:
     - Correct character set displaying
     - Brightness/color pattern matches description
     - Motion speed feels authentic
     - Screen density looks appropriate

4. **Code Review:**
   - No magic numbers (all in config)
   - No hardcoded paths or assumptions
   - Robust error handling
   - Standard library only

5. **Documentation:**
   - README explains how to run
   - README credits original Matrix film
   - Code comments explain non-obvious logic
   - Research findings referenced where relevant

</verification>

<summary_requirements>
Create `.prompts/002-matrix-rain-implement/SUMMARY.md`

Use this structure:

```markdown
# Matrix Rain Implementation Summary

**{One substantive sentence - e.g., "Modular Python terminal implementation with 6 modules recreating Matrix rain effect"}**

## Version
v1

## Key Findings
- {What was implemented}
- {Key technical approaches used}
- {How research findings were applied}

## Files Created
- `matrix_rain/config.py` - Configuration from research parameters
- `matrix_rain/characters.py` - Character set management
- `matrix_rain/column.py` - Column behavior and state
- `matrix_rain/renderer.py` - Terminal rendering engine
- `matrix_rain/main.py` - Main application loop
- `matrix_rain/__init__.py` - Package initialization
- `run_matrix.py` - Launcher script
- `README.md` - Documentation

## Decisions Needed
{Any choices that need user approval, or "None - ready to run"}

## Blockers
{External impediments, or "None"}

## Next Step
Run `python run_matrix.py` to test the effect

---
*Confidence: {High|Medium|Low}*
*Iterations: {n}*
```

The one-liner must be substantive - describe what was built, not "Implementation finished".
</summary_requirements>

<success_criteria>
- All 6+ modules created with clear responsibilities
- Configuration derived from research findings
- Terminal rendering is smooth (no flicker)
- Visual effect matches research description within terminal constraints
- Clean keyboard interrupt handling
- README with clear usage instructions
- Code is modular and maintainable
- All verification steps pass
- SUMMARY.md created with file list and next step
- Application runs successfully in terminal
</success_criteria>
