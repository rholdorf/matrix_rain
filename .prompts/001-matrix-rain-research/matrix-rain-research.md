# Matrix Rain Effect - Technical Research

<research>
  <summary>
    The Matrix digital rain effect from the 1999 film uses mirror-flipped half-width katakana characters combined with Latin letters and numerals, rendered in a distinctive green-on-black color scheme inspired by old IBM CRT monitors. The effect was designed by Simon Whiteley, who drew character references from his wife's Japanese cookbooks and hand-drew each glyph before digitizing them. The animation was created in Softimage and rendered with Mental Ray at 24fps.

    The visual mechanics involve stationary glyphs in a fixed grid where the illusion of falling rain is created by waves of illumination cascading down columns. Most glyphs remain static in position while changing their displayed character every three frames at 50% opacity during transition. The iconic "bright white head fading to green trail" effect is achieved through brightness gradients where the leading character is fully opaque white, gradually dimming through shades of green down the trail.

    Implementation requires understanding three key behaviors: (1) columns spawn at random with variable speeds and lengths, (2) individual characters mutate periodically in synchronized frames creating a shimmer effect, and (3) approximately 1 in 5 columns features a highlighted "runner" glyph that appears brighter than surrounding characters. The effect balances density and sparseness through controlled spawn rates and variable column lifespans.
  </summary>

  <findings>
    <finding category="characters">
      <title>Character Set Composition</title>
      <detail>
        The Matrix digital rain uses a custom typeface designed by Simon Whiteley consisting of:
        - Half-width katakana characters (mirrored/reversed): ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ
        - Notable missing katakana: ｲｸﾁﾄﾉﾌﾍﾖﾙﾚﾛﾝ
        - Arabic numerals (0-9, also mirrored)
        - Limited Latin letters and symbols

        Whiteley chose katakana specifically because it has "very nice simple strokes" that were visually distinctive. All characters were hand-drawn by Whiteley and then scanned/digitized. The mirroring (lateral inversion) was intentional to "create an illusion of being trapped inside the code" and to obscure the characters' familiar shapes.

        Half-width katakana was selected over full-width because the narrower characters fit better in a grid-based display and are ideal for terminal implementations where each character occupies a single monospace cell.
      </detail>
      <source>
        Wikipedia Digital Rain article, Stack Exchange analysis of film screenshots, Science Fiction Stack Exchange character identification, interviews with Simon Whiteley on Snopes, FandomWire, and IMDb
      </source>
      <relevance>
        For terminal implementation, half-width katakana (Unicode range FF65-FF9F) are perfect since they occupy single character width in monospace fonts. The mirroring is optional for terminal recreation but could be achieved through character mapping. A reasonable implementation can use the documented katakana set plus numerals 0-9 for authentic appearance.
      </relevance>
    </finding>

    <finding category="characters">
      <title>Head vs Trail Character Differences</title>
      <detail>
        The original film does not differentiate character types between head and trail positions - the same character set is used throughout. The visual distinction comes entirely from brightness/color differences, not from different character selections. The "head" is simply the leading glyph rendered in bright white, while trail glyphs are rendered in progressively darker shades of green.

        All glyphs (head and trail) can mutate/change their displayed character according to the same mutation rules.
      </detail>
      <source>
        Visual analysis from carlnewton's digital-rain-analysis, implementation studies on GitHub
      </source>
      <relevance>
        Implementation can use the same character pool for all positions in a column. The visual hierarchy is achieved purely through color/brightness attributes applied during rendering, not through character selection logic.
      </relevance>
    </finding>

    <finding category="visual">
      <title>Brightness and Color Pattern</title>
      <detail>
        The iconic color scheme transitions from bright white at the column head through various shades of green down the trail:

        Head (position 0): Bright white (#FFFFFF or #f0fdf4)
        Positions 1-2: Light gray transitioning to light green
        Trail positions: Progressive shades of green from light (#4ade80, #22c55e) to medium (#16a34a) to dark (#15803d)

        The green color was specifically chosen to evoke old IBM CRT monitors. Implementation studies suggest using 3-5 discrete color levels for the gradient:
        - White for head
        - 1-2 gray/light green shades for immediate trail
        - 2-3 progressively darker green shades for the remaining trail

        Opacity/brightness decreases linearly or with a smoothstep function down the trail length. During character mutations, both old and new glyphs appear at 50% opacity in the same position for one frame during transition.
      </detail>
      <source>
        Multiple implementation studies (Flutter tutorial, GitHub C++ implementations, Maarten Hus blog), color value analysis from Tailwind CSS-based implementations, Simon Whiteley interviews mentioning IBM CRT monitor aesthetics
      </source>
      <relevance>
        Terminal ANSI colors provide limited gradients. Best approach: use ANSI bright white (\033[97m) for head, then transition through ANSI bright green (\033[92m) to normal green (\033[32m) to dark green (\033[2;32m dim). This provides 3-4 discrete levels which is sufficient to approximate the gradient effect. Some terminals support 256-color mode (green shades: 46, 40, 34, 28, 22) for smoother gradients.
      </relevance>
    </finding>

    <finding category="motion">
      <title>Column Spawn Frequency</title>
      <detail>
        Columns spawn randomly rather than on a fixed schedule. Analysis of implementations shows common spawn probabilities:
        - Per-column spawn check: ~2.5% chance per frame (Math.random() > 0.975)
        - Alternative approach: 50% probability when previous column completes
        - Columns can spawn at any vertical position, not just at the top of screen

        New columns appear at scattered intervals creating organic, non-uniform coverage. The spawn rate is calibrated to maintain visual interest without overwhelming the screen - typically keeping 20-40% of possible columns active at any given time.
      </detail>
      <source>
        JavaScript implementation analysis from DEV Community, Matrix rain CodeProject article, digital-rain-analysis observations about mid-screen spawning, Rosetta Code implementations
      </source>
      <relevance>
        For terminal implementation, check each potential column position each frame with ~2-5% spawn probability. This creates organic timing. Alternative: maintain a target active column count (e.g., 30% of terminal width) and spawn new columns when count drops below threshold.
      </relevance>
    </finding>

    <finding category="motion">
      <title>Column Velocity and Length</title>
      <detail>
        Speed: Columns fall at variable speeds. Common implementation parameters:
        - Minimum speed: 5 character cells per second
        - Maximum speed: 45 character cells per second (min + 40 range)
        - Some columns fall "quite quickly and difficult to follow" while others "fall slower and can be followed"

        Length: Trail lengths vary significantly:
        - Minimum length: 5 characters
        - Maximum length: Variable, often 15-25 characters
        - Randomized per column at spawn time

        At 20-24fps, speed translates to moving 0-2 rows per frame depending on column speed setting.
      </detail>
      <source>
        Digital rain analysis studies, C++ implementation with speed parameters (minimum 5.0f, range 40), Flutter tutorial specifications, frame rate analysis at 20-24fps
      </source>
      <relevance>
        For terminal at ~20fps refresh: move columns 1 row per frame (slow) to 2-3 rows per frame (fast). Assign random speed multiplier (0.5x to 2x) to each column at spawn. Trail length should be randomized between 7-20 characters to match film variability. Shorter trails create sparseness, longer trails create density.
      </relevance>
    </finding>

    <finding category="behavior">
      <title>Character Mutation Patterns</title>
      <detail>
        Character mutation follows specific rules:

        1. Timing: Glyphs remain static for exactly 3 frames, then change to a new random character
        2. Synchronization: "All changing glyphs change on the same frame" - there's global synchronization
        3. Transition effect: During the mutation frame, old and new glyphs both render at 50% opacity
        4. Not all positions mutate: Some strings consist entirely of changing glyphs while others have static characters
        5. The glyphs themselves don't descend - they remain in place and different glyphs appear beneath them (except for the changing glyphs which mutate in position)

        This creates the characteristic "shimmer" effect where characters flicker and change while the rain cascades down.
      </detail>
      <source>
        carlnewton's digital-rain-analysis (explicit 3-frame timing), visual behavior studies, implementation analysis showing synchronized mutations
      </source>
      <relevance>
        Implementation should maintain a frame counter and trigger mutations every 3 frames globally. For each position in active columns, randomly decide at spawn whether that position will be "static" or "mutating". If mutating, change character every 3 frames. Transition effect can be approximated in terminal by briefly using a dim/gray color during mutation frame.
      </relevance>
    </finding>

    <finding category="behavior">
      <title>Column Lifecycle and Highlighted Glyphs</title>
      <detail>
        Column birth: Columns can spawn at any vertical position, not just screen top. Invisible characters precede visible glyphs (suggesting columns exist "above" the screen before becoming visible).

        Column movement: The leading glyph advances down the screen, leaving a trail. Glyphs in the trail remain in place (except for character mutations).

        Column death: Columns disappear when their length exceeds approximately 2x screen height. The fade-out is gradual enough to be imperceptible. Some implementations show trails fading out as they reach terminal length rather than abruptly disappearing.

        Highlighted glyphs: Approximately 1 in 5 strings (20%) feature a "highlighted" or "runner" glyph - a single character within the trail that appears brighter than surrounding trail glyphs. Only the leading glyph of the string is highlighted at any time. These highlighted glyphs occasionally "stammer" causing the string to fall behind by one row temporarily.
      </detail>
      <source>
        carlnewton's digital-rain-analysis (1 in 5 ratio, leading glyph highlighting, stammering behavior), CodeProject implementation showing 2x screen height lifecycle, observations about mid-screen spawning
      </source>
      <relevance>
        Implementation state machine: SPAWNING -> ACTIVE -> FADING -> DEAD. Track column position, speed, length, age. Spawn 20% of columns with "highlighted runner" flag. For highlighted columns, render one mid-trail character (not head) with brighter color. Remove columns when head position exceeds screen height + trail length. Optional: implement "stammer" effect where highlighted columns randomly pause for 1 frame.
      </relevance>
    </finding>

    <finding category="technical">
      <title>Screen Coverage and Density</title>
      <detail>
        The original effect maintains a balance between density and sparseness:

        Column count: Screen is divided into columns based on character width. For terminal, this equals terminal width in characters.

        Active column percentage: Not all columns are active simultaneously. Typical coverage is 20-40% of available columns at any moment.

        Multiple raindrops per column: The analysis reveals that "multiple raindrops often occupy a column at the same time" with different speeds, though they cannot collide.

        Density control: Adjustable via spawn rate, column count, and average trail length. Denser effect uses higher spawn probability and longer trails.

        Performance: Modern implementations can animate thousands of characters at 60fps, but original was rendered at 24fps. Terminal implementations typically target 20-30fps for smooth appearance without excessive CPU usage.
      </detail>
      <source>
        Rezmason's matrix implementation documentation (density parameter, 80 columns default), digital-rain-analysis (multiple raindrops per column), performance studies showing 60fps capability, original 24fps film specification
      </source>
      <relevance>
        Terminal implementation should: (1) Create one potential column per character width of terminal, (2) Maintain 20-35% active at any time via spawn probability tuning, (3) Target 20fps refresh rate for balance of smoothness and CPU efficiency, (4) Use sleep/delay of ~50ms between frames (1000ms/20fps). For 80-column terminal, maintain ~16-28 active columns. Allow 2-3 raindrops to overlap in same column with different trail positions.
      </relevance>
    </finding>

    <finding category="technical">
      <title>Animation Software and Rendering</title>
      <detail>
        Original production technical stack:
        - Animation software: Softimage (3D animation package)
        - Rendering: Mental Ray (Mental Images' renderer)
        - Design: Custom typeface hand-drawn by Simon Whiteley, scanned and digitized
        - Frame rate: 24fps (standard film frame rate)
        - Post-processing: Justen Marshall (now R&D supervisor at Animal Logic) implemented the vertical cascading effect

        The rain effect was created by making the code "run vertically" which made it "look like rain" with "that feeling of sadness and a melancholic feel" according to Whiteley.

        Once built "in space dimensionally" (3D space), the cascading pattern naturally evoked rainfall.
      </detail>
      <source>
        Simon Whiteley interviews on Snopes, FandomWire, IMDb discussing Softimage and Mental Ray, technical process descriptions, Justen Marshall credit for vertical cascading implementation
      </source>
      <relevance>
        While the original used high-end 3D software, the effect translates well to 2D terminal implementation. The core mechanics (vertical cascading, brightness gradients, character mutation) can be achieved with simple 2D array manipulation and ANSI escape sequences for positioning and coloring. The "dimensionality" can be suggested through brightness variation alone.
      </relevance>
    </finding>

    <finding category="behavior">
      <title>Static vs Dynamic Grid Mechanics</title>
      <detail>
        A crucial understanding: "The glyphs themselves do not descend—except for changing glyphs, they remain in place, and different glyphs appear beneath them."

        This reveals the effect is not characters moving down the screen, but rather:
        1. A fixed grid of character positions
        2. Glyphs that remain static in position (with periodic mutations)
        3. "Waves of illumination" cascading down columns
        4. The rain effect created by changing which glyphs are bright/visible

        The 2D glyphs are in a fixed grid and don't move - the "raindrops" are waves of illumination of stationary symbols occupying a column. This is why multiple raindrops can occupy the same column simultaneously.
      </detail>
      <source>
        carlnewton's digital-rain-analysis (explicit statement about non-descending glyphs), Rezmason's technical documentation about waves of illumination, multiple implementation studies confirming grid-based approach
      </source>
      <relevance>
        Two implementation approaches:

        APPROACH A (Grid-based, closer to original): Maintain a 2D grid [row][col] of characters. Don't move characters. Instead, move a "brightness pointer" down each active column, illuminating characters as it passes. Characters mutate in-place every 3 frames.

        APPROACH B (Simpler, common in terminals): Track column state objects that move down screen, rendering trail behind them. Easier to implement but less authentic.

        Recommend Approach B for initial implementation (simpler), with option to refactor to Approach A for authenticity.
      </relevance>
    </finding>
  </findings>

  <recommendations>
    <recommendation priority="high">
      <action>Use half-width katakana character set for authentic appearance</action>
      <rationale>
        Implement character pool: ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ plus numerals 0-9. These are the documented characters from the original film. Half-width katakana (Unicode FF65-FF9F) fit perfectly in terminal monospace grids. Optional: add limited Latin letters (A-Z, a-z) and symbols (.,;:!?+-=*/) for variation. Character mirroring is optional - can be implemented via Unicode character mapping or omitted for simplicity.
      </rationale>
    </recommendation>

    <recommendation priority="high">
      <action>Implement 3-4 level ANSI color gradient from white to dark green</action>
      <rationale>
        Use ANSI escape sequences to create brightness gradient:
        - Head (position 0): \033[97m (bright white)
        - Position 1-2: \033[92m (bright green)
        - Position 3-6: \033[32m (normal green)
        - Position 7+: \033[2;32m (dim green)

        For terminals supporting 256-color mode, use green palette (colors 46→40→34→28→22) for smoother gradient. This approximates the white-to-dark-green fade within terminal constraints while maintaining the iconic Matrix aesthetic inspired by IBM CRT monitors.
      </rationale>
    </recommendation>

    <recommendation priority="high">
      <action>Target 20fps refresh rate with key timing parameters</action>
      <rationale>
        Frame timing: 50ms delay between frames (1000ms / 20fps)

        Column spawn: Check each inactive column position with 2.5% probability per frame (~2-3 new columns per second for 80-column terminal)

        Column speed: Randomize between 1 row/frame (slow) and 2-3 rows/frame (fast), with weighted preference toward slower speeds

        Column length: Randomize between 7-20 characters at spawn

        Character mutation: Global mutation every 3 frames (every 150ms at 20fps). Randomly designate 40-60% of character positions as "mutating" at column spawn.

        These parameters balance visual authenticity with terminal rendering performance and create the organic, flowing appearance of the original.
      </rationale>
    </recommendation>

    <recommendation priority="medium">
      <action>Implement mixed static and dynamic character mutation strategy</action>
      <rationale>
        At column spawn time, for each position in the trail, randomly decide if that position will be:
        - STATIC (60% probability): Character chosen once, never changes
        - MUTATING (40% probability): Character changes every 3 frames

        Maintain global frame counter. When frame_count % 3 == 0, iterate all MUTATING positions and select new random character from pool.

        This creates the authentic shimmer effect where some characters flicker while others remain stable, matching the observed behavior in the original film. The synchronized mutation (all changes on same frame) is more visually striking than individual random timing.
      </rationale>
    </recommendation>

    <recommendation priority="medium">
      <action>Implement highlighted "runner" glyphs for 20% of columns</action>
      <rationale>
        When spawning a column, generate random number. If < 0.2 (20% chance), mark column as "highlighted".

        For highlighted columns, select one position in the trail (not the head, typically middle third) to render with brighter color than surrounding trail glyphs. As column advances, the highlighted position moves with it.

        Optional enhancement: implement "stammer" effect where highlighted columns have 5% chance per frame to pause movement for 1 frame.

        This adds visual variety and matches the "1 in 5 strings" observation from film analysis, creating more dynamic and interesting rain patterns.
      </rationale>
    </recommendation>

    <recommendation priority="low">
      <action>Allow multiple overlapping raindrops per column</action>
      <rationale>
        Track 2-3 active raindrop objects per column position instead of limiting to one. Each raindrop has independent speed and length. When rendering, blend/overlay their brightness values, taking the maximum brightness at any given position.

        This matches the observation that "multiple raindrops often occupy a column at the same time" and creates richer density without increasing spawn rate. Implement only if performance allows, as it increases state management complexity.
      </rationale>
    </recommendation>
  </recommendations>

  <terminal_constraints>
    ## Limitations of Terminal Environment

    ### Color Depth
    **Original:** Smooth gradients with potentially hundreds of color values from white through pale green through dark green to black
    **Terminal:** Limited to discrete ANSI color codes
    - Basic 16-color mode: ~4 distinct levels (bright white, bright green, green, dim green)
    - 256-color mode: ~6-8 green shades available (colors 46, 40, 34, 28, 22, 16)
    - True color (24-bit): Some modern terminals support full RGB, allowing closer approximation

    **Adaptation:** Use 3-4 discrete brightness levels. This is sufficient to convey the effect as human eye tolerates quantization when characters are rapidly changing.

    ### Refresh Rate and Flicker
    **Original:** Rendered at 24fps, displayed at consistent frame rate without flicker
    **Terminal:**
    - Print-based rendering can cause flicker as screen clears/redraws
    - SSH/network terminals may have lag
    - Different terminal emulators have varying rendering performance

    **Adaptation:** Use ANSI escape sequences for cursor positioning to update only changed characters rather than full screen clear/redraw. Target 20fps (50ms delay) as compromise between smoothness and flicker. Alternative: use curses/ncurses library for double-buffered rendering.

    ### Character Grid Constraints
    **Original:** Rendered at arbitrary resolution, characters can be positioned at any pixel coordinate
    **Terminal:** Locked to fixed character grid (e.g., 80x24, 120x40)
    - No sub-character positioning
    - Movement is quantized to whole character cells

    **Adaptation:** Embrace the grid. The original also used a grid structure, so this is actually faithful. Smooth motion is achieved through timing rather than sub-pixel positioning.

    ### Opacity and Blending
    **Original:** Smooth opacity transitions, 50% opacity blending during character mutations
    **Terminal:** No alpha channel support in standard ANSI

    **Adaptation:** During mutation frames (every 3 frames), render the new character in a midpoint color (e.g., if position would be normal green, render in dim green during mutation frame) to suggest the 50% blend. This is an approximation but maintains the visual rhythm.

    ### Unicode Support
    **Original:** Custom glyphs drawn by hand, potentially unique shapes
    **Terminal:** Dependent on system font and Unicode support
    - Half-width katakana (FF65-FF9F) well-supported in modern terminals
    - Rendering depends on installed fonts
    - Some terminals may not display katakana correctly

    **Adaptation:** Provide fallback character sets. Default to half-width katakana, but allow configuration to use ASCII (A-Z, 0-9, symbols) for terminals with poor Unicode support. Include character set auto-detection if possible.

    ### Performance
    **Original:** Rendered offline, frames can take minutes each
    **Terminal:** Must render in real-time at 20+ fps
    - Large terminals (200x60) = 12,000 character positions
    - CPU-intensive if poorly optimized

    **Adaptation:** Optimize rendering by:
    1. Only update changed character positions, not entire screen
    2. Limit active column count (20-35% of terminal width)
    3. Use efficient data structures (arrays, not nested loops)
    4. Pre-calculate ANSI color codes
    5. Consider skip-frame strategy if CPU-bound (render at 15fps instead of 20fps)

    ### Terminal Size Variability
    **Original:** Fixed canvas size for film frame
    **Terminal:** Variable size (can be resized during execution)

    **Adaptation:** Detect terminal size at startup using ANSI sequences or system calls (e.g., stty size, tput cols/lines). Optionally handle SIGWINCH signal to detect resize events and adjust column count dynamically. Set minimum size requirements (e.g., 40x20) for usable effect.

    ## Practical Implementation Approach

    Given constraints, recommend:
    1. Use curses/ncurses library (or Python equivalent) for flicker-free rendering
    2. Implement 256-color mode with fallback to 16-color
    3. Target 20fps refresh rate
    4. Optimize by tracking dirty regions (only redraw changed characters)
    5. Provide configuration options for density, speed, character set
    6. Include "performance mode" that reduces active columns and uses 16-color mode for slower systems
  </terminal_constraints>

  <metadata>
    <confidence level="high">
      Character composition: HIGH - well-documented by creator interviews and film analysis with specific character lists

      Visual characteristics (colors, gradient): HIGH - consistent across multiple implementation studies and creator statements about IBM CRT aesthetic

      Motion patterns (spawn rate, speed): MEDIUM-HIGH - based on implementation studies and visual observation, but exact probabilities inferred rather than documented

      Character mutation timing: HIGH - explicit "3 frames" documented in digital-rain-analysis with visual confirmation

      Column lifecycle and highlighted glyphs: MEDIUM - "1 in 5" ratio documented, but exact behavior of highlighted glyphs partially inferred

      Overall confidence: HIGH for core characteristics needed for implementation. The combination of creator interviews, technical documentation, and detailed film analysis provides solid foundation. Areas of medium confidence involve exact numerical parameters (spawn probability percentages, speed ranges) which can be tuned during implementation.
    </confidence>

    <dependencies>
      **Essential:**
      - Terminal with ANSI color support (at minimum 16-color mode)
      - Unicode rendering capability (for half-width katakana characters)
      - Monospace font with Japanese character support
      - Terminal control capability (cursor positioning, screen clearing)
      - Programming language with:
        - Random number generation
        - String/character manipulation
        - Terminal I/O control
        - Millisecond-precision timing/sleep

      **Recommended:**
      - 256-color terminal support for smoother gradients
      - curses/ncurses library for flicker-free rendering
      - Terminal size detection (ANSI sequences or system calls)
      - Signal handling for graceful exit (Ctrl+C)

      **Optional:**
      - True color (24-bit) terminal support
      - Window resize detection (SIGWINCH signal handling)
      - Configuration file support for user customization
    </dependencies>

    <open_questions>
      1. **Exact randomization algorithm for character selection**: Is it uniform distribution across character pool, or weighted toward certain characters? Film analysis suggests uniform, but not confirmed.

      2. **Precise column spawn probability per frame**: Implementations vary from 2.5% to 50% depending on approach. Original film specification unknown. Requires tuning to aesthetic preference.

      3. **Character mirroring implementation**: Were characters individually mirrored, or was entire rendered output flipped? Does mirroring enhance terminal implementation or is it unnecessary complication?

      4. **Highlighted glyph "stammer" behavior**: Observation mentions it but mechanism unclear. Is it random pause? Does it affect adjacent characters? How frequent?

      5. **Deletion strings**: Analysis mentions "deletion strings can appear over the top of existing strings" but behavior not fully explained. Are these special column types that erase rather than illuminate?

      6. **Multiple raindrops collision behavior**: When multiple raindrops occupy same column, how do their brightness values combine? Maximum? Additive? Multiplicative?

      7. **Pre-spawn invisible characters**: Analysis suggests characters exist "above" screen before becoming visible. How many? Does this affect mutation timing?

      These questions don't block implementation but could refine authenticity. Recommend prototyping with reasonable assumptions and iterating based on visual comparison.
    </open_questions>

    <assumptions>
      1. **24fps timing estimates**: Assumed original film rendered at standard 24fps. Used for calculating character mutation frequency (3 frames = 125ms).

      2. **Terminal 20fps target**: Assumed 20fps is achievable and sufficient for modern terminals. Higher rates (30-60fps) possible but may cause flicker or excessive CPU usage.

      3. **Uniform character distribution**: Assumed random character selection uses uniform distribution across character pool unless evidence suggests otherwise.

      4. **Grid-based positioning**: Assumed terminal character grid is acceptable approximation of original effect, even though original was rendered at arbitrary pixel resolution.

      5. **ANSI color availability**: Assumed target terminals support at minimum 16-color ANSI codes. Extremely old terminals (monochrome) not supported.

      6. **Unicode font availability**: Assumed modern systems have fonts with half-width katakana support. Fallback to ASCII recommended but not core requirement.

      7. **Single-threaded implementation**: Assumed single-threaded, event-loop-based implementation is sufficient. Multi-threading not required for terminal rendering at 20fps.

      8. **Static terminal size**: Assumed terminal size remains constant during execution, though resize handling is recommended enhancement.

      9. **Vertical-only movement**: Assumed rain falls strictly vertically (no diagonal or horizontal movement) based on all observed implementations.

      10. **Left-to-right column independence**: Assumed each column operates independently with no horizontal interactions between adjacent columns.
    </assumptions>
  </metadata>
</research>
