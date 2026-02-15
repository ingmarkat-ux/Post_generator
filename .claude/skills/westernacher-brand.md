# Westernacher Brand Skill

## Purpose

Apply Westernacher Consulting's brand identity, color coding, and style guidelines to the LinkedIn Post Generator application. This skill ensures all UI elements, generated content, and visual design conform to the official Westernacher brand as defined at westernacher.com.

## Brand Reference

Full brand guidelines are documented in `brand_guidelines_westernacher.md` at the project root. Always consult that file for detailed specifications.

## Color Coding

### Primary Palette
- **Westernacher Blue** `#1596D1` — Primary interactive color (buttons, links, focus states, active elements)
- **Dark Navy** `#060F15` — Dark backgrounds, primary heading text
- **Charcoal** `#282E36` — Body text color

### Secondary Palette
- **Light Blue** `#9ECAE7` — Hover backgrounds, secondary highlights
- **Warm Tan** `#D8C6A8` — Accent hover states, decorative elements
- **White** `#FFFFFF` — Card backgrounds, text on dark surfaces

### Brand Gradient
```css
linear-gradient(90deg, #1595D0 0%, #3E276D 100%)
```
Used for featured elements, hero sections, avatar indicators, and overlay effects.

### Derived UI Colors
- Blue Light: `#E8F4FB` — Focus rings, selected backgrounds
- Blue Hover: `#1178A8` — Button/link hover states
- Surface BG: `#F5F6F8` — Page background
- Success: `#057642` — Positive feedback
- Error: `#CC1016` — Error/destructive actions

## Typography

Primary font: **Graphik** with system font fallbacks.
```
'Graphik', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif
```

Weight usage:
- 200 (Light): Decorative/subtle labels
- 400 (Regular): Body text
- 500 (Medium): Navigation, subheadings
- 600 (Semibold): Headings, buttons, emphasis

## Visual Design Rules

1. Clean minimalism with generous whitespace
2. Border radius: 10px for cards/panels, 6px for inputs/buttons
3. Transitions: 150ms ease for interactions, 300ms for toasts/overlays
4. Shadows: Subtle (`0 1px 3px rgba(0,0,0,0.06)`) with elevated hover (`0 4px 12px rgba(0,0,0,0.08)`)
5. Gradient overlays on imagery and avatar/profile indicators

## Brand Voice for Content Generation

When generating LinkedIn posts under the Westernacher brand:

- **Tone:** Innovative, partnership-driven, confident, forward-looking
- **Perspective:** Expert authority in SAP consulting and digital transformation
- **Language:** Clear, purposeful — avoid generic corporate jargon
- **Structure:** Hook opening, short paragraphs, line breaks for mobile readability
- **Closing:** End with engagement question or call-to-action
- **Required hashtags:** Always include `#WesternacherConsulting` and `#NonstopInnovation`
- **Key phrases to weave in:** "Nonstop Innovation", "believe in partnership", "operational excellence", "digital transformation", "technology-driven innovation"

## Topic Alignment

Prioritize these Westernacher-aligned topics:
- Innovation & Digital Transformation
- SAP & Enterprise Technology (S/4HANA, EWM, TM, Analytics)
- Supply Chain & Logistics Optimization
- Sustainability & Carbon Neutrality
- Leadership & Organizational Excellence
- Partnership & Collaboration

## When to Apply This Skill

- When modifying UI styles or CSS — use Westernacher color palette and design rules
- When editing the post generation system prompt — apply Westernacher brand voice
- When adding new UI components — follow the visual design rules above
- When creating or modifying content templates — align with brand voice and topics
- When the user references "Westernacher brand", "brand guidelines", or "brand style"
