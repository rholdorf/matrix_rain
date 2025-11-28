# Matrix Rain Research Summary

**Half-width katakana characters (mirrored) cascade at variable speeds with bright white heads fading through green trails, mutating every 3 frames in synchronized waves to create the iconic shimmer effect over a fixed character grid.**

## Version
v1

## Key Findings
- Character set: Mirror-flipped half-width katakana (ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ) plus numerals 0-9, hand-drawn by designer Simon Whiteley from Japanese cookbook references
- Visual effect: Bright white head (\033[97m) fading through 3-4 discrete ANSI green shades to dark green, with 20% of columns featuring highlighted "runner" glyphs mid-trail
- Motion mechanics: Columns spawn randomly (2.5% probability/frame), fall at variable speeds (1-3 rows/frame at 20fps), trail lengths 7-20 characters, with 20-35% screen coverage
- Character mutation: Glyphs remain static in grid positions, mutating every 3 frames globally with 40% designated as mutating positions, creating shimmer while waves of illumination cascade down
- Grid-based architecture: Fixed 2D grid where characters don't physically descend - instead brightness waves move down columns, allowing multiple overlapping raindrops per column

## Decisions Needed
None - research provides sufficient detail for implementation. Optional choices: character mirroring (can omit), 256-color vs 16-color mode (support both), grid-based vs simplified column approach (recommend simplified first).

## Blockers
None - all required information gathered. Terminal must support ANSI colors and Unicode (half-width katakana), which are standard on modern systems.

## Next Step
Create matrix-rain-implement prompt using these findings to build Python terminal implementation with curses/ncurses, targeting 20fps refresh rate with configurable parameters.

---
*Confidence: High*
*Full output: matrix-rain-research.md*
