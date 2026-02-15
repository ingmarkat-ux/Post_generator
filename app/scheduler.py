"""Post scheduling system using APScheduler."""

import uuid
from datetime import datetime, timezone
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore

from app.linkedin import post_to_linkedin

scheduler = BackgroundScheduler(
    jobstores={"default": MemoryJobStore()},
    job_defaults={"coalesce": True, "max_instances": 1},
)

# In-memory store for scheduled posts
scheduled_posts: dict[str, dict] = {}


def start_scheduler():
    if not scheduler.running:
        scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)


def get_optimal_slots() -> list[dict]:
    """Return the next 3 optimal LinkedIn posting time slots.

    Based on LinkedIn engagement data:
    - Tuesday-Thursday: highest engagement
    - 7-8 AM, 12 PM, 5-6 PM: peak hours
    """
    now = datetime.now(timezone.utc)
    slots = []

    # Peak posting windows (hour, label)
    peak_windows = [
        (7, "Early Morning — Catches commuters & early risers"),
        (12, "Lunch Break — High scroll-time engagement"),
        (17, "End of Workday — Professionals winding down"),
    ]

    # Best days: Tuesday(1), Wednesday(2), Thursday(3)
    best_days = {1, 2, 3}

    candidate = now.replace(minute=0, second=0, microsecond=0)

    while len(slots) < 3:
        for hour, label in peak_windows:
            slot = candidate.replace(hour=hour)
            if slot > now and (slot.weekday() in best_days or len(slots) < 3):
                slots.append({
                    "datetime": slot.isoformat(),
                    "label": label,
                    "day": slot.strftime("%A"),
                    "time": slot.strftime("%I:%M %p"),
                    "date": slot.strftime("%B %d, %Y"),
                })
                if len(slots) >= 3:
                    break
        candidate = candidate.replace(hour=0)
        candidate = datetime.fromtimestamp(
            candidate.timestamp() + 86400, tz=timezone.utc
        )

    return slots


def schedule_post(
    content: str,
    scheduled_time: str,
    access_token: Optional[str] = None,
) -> dict:
    """Schedule a post for future publishing."""
    post_id = str(uuid.uuid4())[:8]
    run_date = datetime.fromisoformat(scheduled_time)

    if access_token:
        scheduler.add_job(
            post_to_linkedin,
            trigger="date",
            run_date=run_date,
            args=[access_token, content],
            id=post_id,
        )

    scheduled_posts[post_id] = {
        "id": post_id,
        "content": content,
        "scheduled_time": scheduled_time,
        "status": "scheduled" if access_token else "draft",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    return scheduled_posts[post_id]


def get_scheduled_posts() -> list[dict]:
    return list(scheduled_posts.values())


def cancel_scheduled_post(post_id: str) -> bool:
    if post_id in scheduled_posts:
        try:
            scheduler.remove_job(post_id)
        except Exception:
            pass
        scheduled_posts[post_id]["status"] = "cancelled"
        return True
    return False
