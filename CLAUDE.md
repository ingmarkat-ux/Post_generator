# Westernacher Post Generator — Project Instructions

## Brand Identity

This project follows **Westernacher Consulting** brand guidelines. All UI, content, and design decisions must conform to the official Westernacher brand identity as documented in `brand_guidelines_westernacher.md`.

**Tagline:** "Nonstop Innovation"
**Website:** westernacher.com

## Color Coding (Quick Reference)

| Role             | Color                | Hex       |
|------------------|----------------------|-----------|
| Primary          | Westernacher Blue    | `#1596D1` |
| Primary Hover    | Blue Hover           | `#1178A8` |
| Primary Light    | Blue Light           | `#E8F4FB` |
| Text             | Charcoal             | `#282E36` |
| Dark Background  | Dark Navy            | `#060F15` |
| Background       | Surface BG           | `#F5F6F8` |
| Accent           | Light Blue           | `#9ECAE7` |
| Warm Accent      | Warm Tan             | `#D8C6A8` |
| Success          | Green                | `#057642` |
| Error            | Red                  | `#CC1016` |
| Brand Gradient   | Blue → Purple        | `linear-gradient(90deg, #1595D0 0%, #3E276D 100%)` |

## Typography

Font: `'Graphik', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif`

Weights: Light (200), Regular (400), Medium (500), Semibold (600)

## Brand Voice

When writing or generating content for this application:

- **Tone:** Innovative, partnership-driven, confident, forward-looking
- **Perspective:** Expert authority in SAP consulting and digital transformation
- **Language:** Clear, purposeful — no generic corporate jargon
- **Required hashtags:** `#WesternacherConsulting` `#NonstopInnovation`
- **Key phrases:** "Nonstop Innovation", "believe in partnership", "operational excellence", "digital transformation", "technology-driven innovation"

## Skills

- **Westernacher Brand Skill** (`.claude/skills/westernacher-brand.md`): Full brand application guide covering colors, typography, visual design rules, brand voice for content generation, and topic alignment. Consult this skill whenever modifying UI, styles, templates, or generated content.

## Project Structure

- `app/` — Python backend (FastAPI): generator, LinkedIn integration, scheduler, models, config
- `static/css/style.css` — Westernacher-branded CSS (uses CSS custom properties for all brand colors)
- `static/js/app.js` — Frontend logic
- `templates/index.html` — Jinja2 template with Westernacher-aligned topics
- `brand_guidelines_westernacher.md` — Complete brand reference document

## Development Guidelines

- Always use CSS custom properties (`var(--primary)`, `var(--gradient)`, etc.) rather than hardcoded color values
- Maintain the Westernacher brand gradient for featured/hero elements
- All generated LinkedIn posts must include `#WesternacherConsulting` and `#NonstopInnovation`
- Topic chips should align with Westernacher's consulting domains: Innovation, Digital Transformation, SAP & Technology, Supply Chain & Logistics, Leadership, Sustainability, Partnership, Operational Excellence
