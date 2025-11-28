# Research: Matrix Rain Effect Analysis

<research_objective>
Research the "Matrix rain" digital rain effect from the original 1999 film "The Matrix" to inform Python terminal implementation.

Purpose: Understand the technical and visual characteristics needed to recreate the effect in a terminal environment
Scope: Original 1999 film effect only - visual behavior, character sets, timing, and motion patterns
Output: matrix-rain-research.md with structured findings
</research_objective>

<research_scope>
<include>
**Visual Characteristics:**
- Character composition: What characters appear (Japanese katakana, Latin, numbers, symbols)
- Character differentiation: Do different types of characters appear in different parts (head vs trail)?
- Color and brightness: The "bright head" effect and how it fades down the trail
- Opacity/fade pattern: How characters dim as they move down in the trail

**Motion and Timing:**
- Column spawn frequency: How often new columns appear on screen
- Column velocity: Speed of descent (constant or variable?)
- Column length: Maximum and minimum heights observed
- Column lifespan: Do columns disappear/fade or reach bottom?

**Dynamic Behavior:**
- Character mutation: Do characters change while in the trail, or only at creation?
- Static vs dynamic characters: Which positions have changing characters
- Head behavior: Special characteristics of the leading/brightest character
- Randomness patterns: What aspects are randomized

**Technical Implementation Clues:**
- Frame rate observations
- Screen coverage patterns (sparse vs dense)
- Any visible algorithmic patterns
</include>

<exclude>
- Sequels and later Matrix films (focus only on 1999 original)
- Behind-the-scenes production details (unless technically relevant)
- Philosophical meaning or narrative context
- Commercial implementations or existing code (we want pure analysis first)
</exclude>

<sources>
Priority sources:
- Film analysis and frame studies
- Technical VFX documentation from 1999 production
- Digital rain creator interviews (if available)
- High-quality screenshots/clips for direct observation
- Prefer primary sources over interpretations
</sources>
</research_scope>

<research_approach>
Deeply consider the visual mechanics of this effect. Thoroughly analyze multiple sources to build an accurate technical model. Consider both what is explicitly documented and what can be inferred from visual observation.

For maximum efficiency, invoke all independent tool operations simultaneously:
- Search for technical documentation
- Fetch creator interviews
- Analyze visual references
- Research character sets used
</research_approach>

<output_structure>
Save to: `.prompts/001-matrix-rain-research/matrix-rain-research.md`

Structure findings using this XML format:

```xml
<research>
  <summary>
    {2-3 paragraph executive summary covering the essential visual and technical characteristics of the Matrix rain effect}
  </summary>

  <findings>
    <finding category="characters">
      <title>Character Set Composition</title>
      <detail>{What characters are used, their origins (katakana, etc.)}</detail>
      <source>{Where this information came from}</source>
      <relevance>{Why this matters for terminal implementation}</relevance>
    </finding>

    <finding category="characters">
      <title>Head vs Trail Character Differences</title>
      <detail>{Do different characters appear in the bright head vs the trail}</detail>
      <source>{Evidence source}</source>
      <relevance>{Implementation implications}</relevance>
    </finding>

    <finding category="visual">
      <title>Brightness and Color Pattern</title>
      <detail>{How the bright head effect works, color values, fade pattern}</detail>
      <source>{Source}</source>
      <relevance>{How to simulate in terminal with ANSI colors}</relevance>
    </finding>

    <finding category="motion">
      <title>Column Spawn Frequency</title>
      <detail>{How often columns appear, any patterns or randomness}</detail>
      <source>{Source}</source>
      <relevance>{Frame timing for implementation}</relevance>
    </finding>

    <finding category="motion">
      <title>Column Velocity and Length</title>
      <detail>{Speed of descent, min/max heights observed}</detail>
      <source>{Source}</source>
      <relevance>{Animation parameters}</relevance>
    </finding>

    <finding category="behavior">
      <title>Character Mutation Patterns</title>
      <detail>{Which characters change, when they change, which remain static}</detail>
      <source>{Source}</source>
      <relevance>{Dynamic vs static character logic}</relevance>
    </finding>

    <finding category="behavior">
      <title>Column Lifecycle</title>
      <detail>{Birth, movement, death/fade of columns}</detail>
      <source>{Source}</source>
      <relevance>{State management in implementation}</relevance>
    </finding>

    <finding category="technical">
      <title>Screen Coverage and Density</title>
      <detail>{How many columns active, spacing patterns, density}</detail>
      <source>{Source}</source>
      <relevance>{Performance and visual fidelity balance}</relevance>
    </finding>

    <!-- Additional findings as discovered -->
  </findings>

  <recommendations>
    <recommendation priority="high">
      <action>Character set to use for terminal implementation</action>
      <rationale>{Why these characters based on research}</rationale>
    </recommendation>

    <recommendation priority="high">
      <action>Color/brightness approach for terminal ANSI support</action>
      <rationale>{How to approximate the effect within terminal constraints}</rationale>
    </recommendation>

    <recommendation priority="high">
      <action>Key timing parameters (spawn rate, speed, mutation frequency)</action>
      <rationale>{Based on observed patterns}</rationale>
    </recommendation>

    <recommendation priority="medium">
      <action>Static vs dynamic character strategy</action>
      <rationale>{Based on visual analysis}</rationale>
    </recommendation>
  </recommendations>

  <terminal_constraints>
    {Analysis of how terminal limitations (ANSI colors, character grid, refresh rate) affect implementation}

    {Specific adaptations needed: e.g., "Original uses smooth gradients; terminal limited to discrete ANSI green shades"}
  </terminal_constraints>

  <metadata>
    <confidence level="{high|medium|low}">
      {Why this confidence level - e.g., "High for character composition (well-documented), Medium for exact timing (requires visual estimation)"}
    </confidence>
    <dependencies>
      {What's needed to implement - e.g., "Terminal with ANSI color support, Unicode character rendering, reasonable refresh rate"}
    </dependencies>
    <open_questions>
      {What couldn't be determined - e.g., "Exact randomization algorithm for character selection", "Precise column spawn probability per frame"}
    </open_questions>
    <assumptions>
      {What was assumed - e.g., "Assuming 24fps for timing estimates", "Assuming terminal can handle 60Hz refresh"}
    </assumptions>
  </metadata>
</research>
```
</output_structure>

<summary_requirements>
Create `.prompts/001-matrix-rain-research/SUMMARY.md`

Use this structure:

```markdown
# Matrix Rain Research Summary

**{One substantive sentence describing the key finding - e.g., "Katakana characters with bright white heads fading through green trail with character mutation"}**

## Version
v1

## Key Findings
- {Most important characteristic discovered}
- {Second key characteristic}
- {Third key characteristic}

## Decisions Needed
{Any choices that need user input, or "None"}

## Blockers
{External impediments, or "None"}

## Next Step
Create matrix-rain-implement prompt using these findings

---
*Confidence: {High|Medium|Low}*
*Full output: matrix-rain-research.md*
```

The one-liner must be substantive - describe actual findings, not "Research completed".
</summary_requirements>

<verification>
Before declaring complete:
1. All scope questions from <include> section have been addressed
2. Findings include specific, actionable details (not vague descriptions)
3. Sources are cited for each finding
4. Recommendations are concrete and implementation-ready
5. Terminal constraints section addresses practical limitations
6. Metadata captures uncertainties and assumptions
7. SUMMARY.md created with substantive one-liner
</verification>

<success_criteria>
- Character set composition identified with sources
- Visual characteristics (brightness, fade, colors) documented
- Motion patterns (spawn rate, velocity, lengths) quantified
- Dynamic behavior (mutation, static chars, head properties) explained
- Terminal adaptation strategy recommended
- All metadata fields completed honestly
- SUMMARY.md created with concrete findings
- Ready for implementation prompt to consume this research
</success_criteria>
