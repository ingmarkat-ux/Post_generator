# LinkedIn Post Generator

A web application that helps you create, edit, and schedule LinkedIn posts optimized for engagement.

## Features

- **Topic-based generation** — Select from predefined topics or enter your own
- **AI-powered writing** — Generates personal, business-context posts optimized for LinkedIn (uses OpenAI API, with built-in template fallback)
- **Clean post editor** — Edit and refine generated posts in a distraction-free interface
- **LinkedIn preview** — See how your post will look before publishing
- **Optimal time slots** — Suggests the next 3 best times to post based on LinkedIn engagement data
- **Post scheduling** — Schedule posts to be published at your chosen time
- **Direct LinkedIn posting** — Connect your LinkedIn account via OAuth to post directly

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

**OpenAI API Key** (optional — the app has built-in templates as fallback):
- Get a key from https://platform.openai.com/api-keys

**LinkedIn OAuth** (required for direct posting):
- Create an app at https://www.linkedin.com/developers/
- Add `http://localhost:8000/auth/linkedin/callback` as an authorized redirect URL
- Enable the `Sign In with LinkedIn using OpenID Connect` and `Share on LinkedIn` products

### 3. Run the application

```bash
python run.py
```

Open http://localhost:8000 in your browser.

## Usage

1. **Select a topic** from the chips or type your own
2. **Add context** (optional) — personal experiences or specific angles
3. **Choose a tone** — Professional & Personal, Thought Leadership, or Storytelling
4. Click **Activate** to generate the post
5. **Edit** the generated post in the text editor
6. **Preview** how it will appear on LinkedIn
7. **Schedule** using an optimal time slot or pick a custom time
8. Or **Post Now** if your LinkedIn account is connected

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript (no framework)
- **Post Generation**: OpenAI GPT-4o-mini (with template fallback)
- **Scheduling**: APScheduler
- **LinkedIn Integration**: OAuth 2.0, UGC Posts API
