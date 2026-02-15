# CLAUDE.md

## Project Overview

LinkedIn Post Generator — a web application for creating, editing, and scheduling LinkedIn posts optimized for engagement. Single-user app with in-memory session/state (no database).

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Frontend**: Vanilla HTML/CSS/JS (Jinja2 templates), no framework
- **Post Generation**: OpenAI GPT-4o-mini (with built-in template fallback when no API key)
- **Scheduling**: APScheduler (BackgroundScheduler, in-memory job store)
- **LinkedIn Integration**: OAuth 2.0, UGC Posts API via httpx
- **Deployment**: Docker, Render (see `render.yaml`, `Procfile`)

## Project Structure

```
app/
  main.py        — FastAPI app, routes, lifespan (scheduler start/stop)
  config.py      — Environment variable loading via python-dotenv
  generator.py   — OpenAI post generation + fallback templates
  linkedin.py    — OAuth flow, token exchange, profile fetch, UGC post creation
  scheduler.py   — APScheduler setup, optimal time slots, schedule/cancel posts
  models.py      — Pydantic request models (TopicRequest, PostContent, ScheduleRequest)
templates/
  index.html     — Single-page UI
static/
  css/style.css  — Styles
  js/app.js      — Client-side logic
run.py           — Entry point (uvicorn with reload)
```

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app (default port 8000, with hot reload)
python run.py

# Lint (matches CI)
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run tests
pytest
```

## Environment Variables

Configured via `.env` file (see `.env.example`):

- `OPENAI_API_KEY` — Optional; enables AI generation (falls back to templates without it)
- `LINKEDIN_CLIENT_ID` — Required for LinkedIn OAuth
- `LINKEDIN_CLIENT_SECRET` — Required for LinkedIn OAuth
- `LINKEDIN_REDIRECT_URI` — Defaults to `http://localhost:8000/auth/linkedin/callback`
- `PORT` — Server port (defaults to 8000)

## CI/CD

GitHub Actions workflow (`.github/workflows/python-app.yml`):
- Python 3.10, flake8 lint, pytest
- Triggers on push/PR to `claude/linkedin-post-generator-xZDmX` branch

## Key Architecture Notes

- **No database** — all state (session, scheduled posts) is in-memory and resets on restart
- **Single-user** — session is a module-level dict in `main.py`, not per-request
- **OpenAI fallback** — if `OPENAI_API_KEY` is missing or API call fails, `generator.py` uses hardcoded template posts keyed by topic
- **Scheduling** — posts are scheduled via APScheduler; if a LinkedIn token is available the job calls `post_to_linkedin` at the scheduled time, otherwise the post is saved as a "draft"
- **OAuth callback** — `/auth/linkedin/callback` exchanges the code for a token and stores it in the in-memory session
