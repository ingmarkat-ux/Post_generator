/* ── State ──────────────────────────────────────────────────────────── */
let selectedTopic = "";
let selectedSlot = null;
let currentPost = "";

/* ── Init ──────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
    initTopicChips();
    initToneCards();
    loadOptimalSlots();
    loadScheduledPosts();
    setupEditorSync();
});

/* ── Topic Selection ───────────────────────────────────────────────── */
function initTopicChips() {
    document.querySelectorAll(".topic-chip").forEach((chip) => {
        chip.addEventListener("click", () => {
            document.querySelectorAll(".topic-chip").forEach((c) => c.classList.remove("active"));
            chip.classList.add("active");
            selectedTopic = chip.dataset.topic;
            document.getElementById("custom-topic").value = "";
        });
    });

    document.getElementById("custom-topic").addEventListener("input", (e) => {
        if (e.target.value.trim()) {
            document.querySelectorAll(".topic-chip").forEach((c) => c.classList.remove("active"));
            selectedTopic = e.target.value.trim();
        }
    });
}

/* ── Tone Selection ────────────────────────────────────────────────── */
function initToneCards() {
    document.querySelectorAll(".radio-card").forEach((card) => {
        card.addEventListener("click", () => {
            document.querySelectorAll(".radio-card").forEach((c) => c.classList.remove("active"));
            card.classList.add("active");
        });
    });
}

/* ── Editor Sync ───────────────────────────────────────────────────── */
function setupEditorSync() {
    const editor = document.getElementById("post-editor");
    editor.addEventListener("input", () => {
        currentPost = editor.value;
        updateCharCount();
        updatePreview();
    });
}

function updateCharCount() {
    const count = currentPost.length;
    document.getElementById("char-count").textContent = `${count} characters`;
}

function updatePreview() {
    const previewBody = document.getElementById("preview-body");
    if (previewBody) {
        previewBody.textContent = currentPost;
    }
}

/* ── Generate Post ─────────────────────────────────────────────────── */
async function generatePost() {
    const topic = selectedTopic || document.getElementById("custom-topic").value.trim();
    if (!topic) {
        showToast("Please select or enter a topic", "error");
        return;
    }

    const context = document.getElementById("context").value.trim();
    const tone = document.querySelector('input[name="tone"]:checked').value;

    const btn = document.getElementById("btn-activate");
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Generating...';

    try {
        const res = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, context, tone }),
        });
        const data = await res.json();

        currentPost = data.content;
        showEditor(data.content);
        showToast("Post generated successfully", "success");
    } catch (err) {
        showToast("Failed to generate post", "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
            Activate`;
    }
}

async function regeneratePost() {
    const topic = selectedTopic || document.getElementById("custom-topic").value.trim();
    if (!topic) return;

    const context = document.getElementById("context").value.trim();
    const tone = document.querySelector('input[name="tone"]:checked').value;

    try {
        const res = await fetch("/api/regenerate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, context, tone }),
        });
        const data = await res.json();

        currentPost = data.content;
        showEditor(data.content);
        showToast("Post regenerated", "info");
    } catch (err) {
        showToast("Failed to regenerate", "error");
    }
}

function showEditor(content) {
    document.getElementById("empty-state").style.display = "none";
    document.getElementById("editor-area").style.display = "block";
    document.getElementById("post-actions").style.display = "flex";

    const editor = document.getElementById("post-editor");
    editor.value = content;
    currentPost = content;
    updateCharCount();
    updatePreview();
}

/* ── Preview Toggle ────────────────────────────────────────────────── */
function togglePreview() {
    const container = document.getElementById("preview-container");
    const isHidden = container.style.display === "none";
    container.style.display = isHidden ? "block" : "none";
    if (isHidden) updatePreview();
}

/* ── Optimal Time Slots ────────────────────────────────────────────── */
async function loadOptimalSlots() {
    try {
        const res = await fetch("/api/optimal-slots");
        const data = await res.json();
        renderSlots(data.slots);
    } catch (err) {
        console.error("Failed to load slots:", err);
    }
}

function renderSlots(slots) {
    const container = document.getElementById("time-slots");
    container.innerHTML = slots
        .map(
            (slot, i) => `
        <div class="time-slot" data-datetime="${slot.datetime}" onclick="selectSlot(this, '${slot.datetime}')">
            <div class="slot-indicator"></div>
            <div class="slot-info">
                <div class="slot-datetime">${slot.day}, ${slot.date} at ${slot.time}</div>
                <div class="slot-label">${slot.label}</div>
            </div>
        </div>
    `
        )
        .join("");
}

function selectSlot(el, datetime) {
    document.querySelectorAll(".time-slot").forEach((s) => s.classList.remove("active"));
    el.classList.add("active");
    selectedSlot = datetime;
    document.getElementById("custom-datetime").value = "";
}

/* ── Schedule Post ─────────────────────────────────────────────────── */
async function schedulePost() {
    const content = document.getElementById("post-editor").value.trim();
    if (!content) {
        showToast("No post content to schedule", "error");
        return;
    }

    const customDatetime = document.getElementById("custom-datetime").value;
    const scheduledTime = customDatetime ? new Date(customDatetime).toISOString() : selectedSlot;

    if (!scheduledTime) {
        showToast("Please select a time slot or enter a custom time", "error");
        return;
    }

    try {
        const res = await fetch("/api/schedule", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                post_content: content,
                scheduled_time: scheduledTime,
            }),
        });
        const data = await res.json();
        showToast("Post scheduled successfully", "success");
        loadScheduledPosts();
    } catch (err) {
        showToast("Failed to schedule post", "error");
    }
}

/* ── Post Now ──────────────────────────────────────────────────────── */
async function postNow() {
    const content = document.getElementById("post-editor").value.trim();
    if (!content) {
        showToast("No post content to publish", "error");
        return;
    }

    try {
        const res = await fetch("/api/post-now", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content, topic: selectedTopic }),
        });
        const data = await res.json();

        if (data.error) {
            showToast(data.error, "error");
        } else {
            showToast("Post published to LinkedIn!", "success");
        }
    } catch (err) {
        showToast("Failed to publish post", "error");
    }
}

/* ── Scheduled Posts List ──────────────────────────────────────────── */
async function loadScheduledPosts() {
    try {
        const res = await fetch("/api/scheduled-posts");
        const data = await res.json();
        renderScheduledPosts(data.posts);
    } catch (err) {
        console.error("Failed to load scheduled posts:", err);
    }
}

function refreshScheduled() {
    loadScheduledPosts();
}

function renderScheduledPosts(posts) {
    const container = document.getElementById("scheduled-list");

    if (!posts || posts.length === 0) {
        container.innerHTML = '<p class="empty-text">No scheduled posts yet</p>';
        return;
    }

    container.innerHTML = posts
        .map((post) => {
            const time = new Date(post.scheduled_time).toLocaleString();
            const preview = post.content.substring(0, 120) + (post.content.length > 120 ? "..." : "");
            return `
            <div class="scheduled-item">
                <div class="scheduled-item-content">
                    <p>${escapeHtml(preview)}</p>
                    <div class="scheduled-item-meta">
                        <span class="scheduled-item-time">${time}</span>
                        <span class="status-badge ${post.status}">${post.status}</span>
                    </div>
                </div>
                ${post.status === "scheduled" || post.status === "draft" ? `<button class="btn-cancel" onclick="cancelPost('${post.id}')">Cancel</button>` : ""}
            </div>
        `;
        })
        .join("");
}

async function cancelPost(postId) {
    try {
        await fetch(`/api/scheduled-posts/${postId}`, { method: "DELETE" });
        showToast("Post cancelled", "info");
        loadScheduledPosts();
    } catch (err) {
        showToast("Failed to cancel post", "error");
    }
}

/* ── LinkedIn ──────────────────────────────────────────────────────── */
async function disconnectLinkedIn() {
    try {
        await fetch("/auth/linkedin/disconnect", { method: "POST" });
        location.reload();
    } catch (err) {
        showToast("Failed to disconnect", "error");
    }
}

/* ── Toast Notifications ───────────────────────────────────────────── */
function showToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(100%)";
        toast.style.transition = "all 300ms ease";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/* ── Utilities ─────────────────────────────────────────────────────── */
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
