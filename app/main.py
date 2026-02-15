"""LinkedIn Post Generator — FastAPI Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import LINKEDIN_CLIENT_ID
from app.generator import generate_post
from app.linkedin import exchange_code_for_token, get_auth_url, get_user_profile
from app.models import PostContent, ScheduleRequest, TopicRequest
from app.scheduler import (
    cancel_scheduled_post,
    get_optimal_slots,
    get_scheduled_posts,
    schedule_post,
    start_scheduler,
    stop_scheduler,
)

# In-memory session store (single-user app)
session: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="LinkedIn Post Generator", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ── Pages ──────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "linkedin_connected": "access_token" in session,
        "user_name": session.get("user_name", ""),
    })


# ── Post Generation API ───────────────────────────────────────────────

@app.post("/api/generate")
async def api_generate(req: TopicRequest):
    content = generate_post(req.topic, req.context, req.tone)
    return {"content": content, "topic": req.topic}


@app.post("/api/regenerate")
async def api_regenerate(req: TopicRequest):
    content = generate_post(req.topic, req.context, req.tone)
    return {"content": content, "topic": req.topic}


# ── Scheduling API ────────────────────────────────────────────────────

@app.get("/api/optimal-slots")
async def api_optimal_slots():
    return {"slots": get_optimal_slots()}


@app.post("/api/schedule")
async def api_schedule(req: ScheduleRequest):
    token = session.get("access_token")
    result = schedule_post(req.post_content, req.scheduled_time, token)
    return result


@app.get("/api/scheduled-posts")
async def api_scheduled_posts():
    return {"posts": get_scheduled_posts()}


@app.delete("/api/scheduled-posts/{post_id}")
async def api_cancel_post(post_id: str):
    success = cancel_scheduled_post(post_id)
    return {"success": success}


# ── LinkedIn Post Now ─────────────────────────────────────────────────

@app.post("/api/post-now")
async def api_post_now(req: PostContent):
    from app.linkedin import post_to_linkedin

    token = session.get("access_token")
    if not token:
        return {"error": "Not connected to LinkedIn"}
    try:
        result = post_to_linkedin(token, req.content)
        return {"success": True, "result": result}
    except Exception as e:
        return {"error": str(e)}


# ── LinkedIn OAuth ────────────────────────────────────────────────────

@app.get("/auth/linkedin")
async def auth_linkedin():
    if not LINKEDIN_CLIENT_ID:
        return {"error": "LinkedIn credentials not configured. Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in .env"}
    return RedirectResponse(get_auth_url())


@app.get("/auth/linkedin/callback")
async def auth_callback(code: str, request: Request):
    try:
        token_data = await exchange_code_for_token(code)
        session["access_token"] = token_data["access_token"]
        profile = await get_user_profile(token_data["access_token"])
        session["user_name"] = profile.get("name", "LinkedIn User")
        session["user_sub"] = profile.get("sub", "")
    except Exception:
        pass
    return RedirectResponse("/")


@app.get("/auth/linkedin/status")
async def auth_status():
    return {
        "connected": "access_token" in session,
        "user_name": session.get("user_name", ""),
    }


@app.post("/auth/linkedin/disconnect")
async def auth_disconnect():
    session.clear()
    return {"success": True}
