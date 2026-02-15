"""Post generation logic using OpenAI API with fallback templates."""

from openai import OpenAI
from app.config import OPENAI_API_KEY

SYSTEM_PROMPT = """You are a LinkedIn post writing assistant. You write engaging,
personal posts related to business topics. Your writing style is:

- First-person perspective, sharing personal experiences or insights
- Professional but approachable tone
- Structured with short paragraphs and line breaks for readability
- Includes a hook in the first line to grab attention
- Ends with a question or call-to-action to drive engagement
- Uses relevant hashtags (3-5 max) at the end
- Avoids corporate jargon; feels authentic and human
- Optimal length: 150-300 words (LinkedIn sweet spot for engagement)
- Uses line breaks between paragraphs for mobile readability
"""

FALLBACK_TEMPLATES = {
    "leadership": """I've been reflecting on what leadership really means in today's fast-paced world.

It's not about having all the answers. It's about asking the right questions and creating space for your team to find solutions.

Last week, I stepped back during a critical project decision. Instead of directing, I listened. The result? My team came up with an approach I never would have considered — and it worked brilliantly.

Three things I've learned about modern leadership:

→ Vulnerability is strength, not weakness
→ The best ideas often come from unexpected places
→ Your job isn't to be the smartest person in the room

What's the most important leadership lesson you've learned this year?

#Leadership #Management #BusinessGrowth #PersonalDevelopment #TeamWork""",
    "innovation": """Innovation doesn't always look like a breakthrough moment.

Sometimes it's a small process change. A different way of looking at an old problem. A question nobody thought to ask.

I recently challenged my team to find one thing we do "because we've always done it that way." We found seven. We changed five of them.

The result? 30% faster delivery time and a team that feels more empowered than ever.

Real innovation starts with:

→ Questioning assumptions
→ Embracing discomfort
→ Celebrating small wins

What's one process in your work that could use a fresh perspective?

#Innovation #BusinessStrategy #GrowthMindset #Entrepreneurship #Change""",
    "career": """5 years ago, I made a career decision that everyone told me was a mistake.

I left a comfortable position to pursue something that scared me. There were sleepless nights. Moments of doubt. Times I questioned everything.

But here's what I learned:

→ Growth never happens in comfort zones
→ The "risky" path often has the biggest rewards
→ Your network becomes your net worth during transitions

Looking back, that "mistake" was the best decision I ever made. Not because it was easy — but because it forced me to grow in ways I never expected.

If you're standing at a career crossroads right now, trust yourself. The path less traveled has a way of becoming the right one.

What career leap are you considering?

#CareerGrowth #ProfessionalDevelopment #CareerAdvice #Motivation #Success""",
    "technology": """The technology landscape is shifting faster than ever.

But here's what most people get wrong: it's not about adopting every new tool. It's about understanding which ones solve real problems.

I recently audited the tech stack at my organization. We were using 15 different tools. We needed 6.

The simplification led to:

→ Better team collaboration
→ Reduced costs by 40%
→ Clearer workflows and less context-switching

Technology should amplify human capability, not complicate it.

Before you adopt the next shiny tool, ask yourself: "Does this solve a problem we actually have?"

What's your approach to evaluating new technology?

#Technology #DigitalTransformation #Productivity #TechStrategy #BusinessTools""",
    "default": """Something happened recently that completely changed my perspective on {topic}.

We often get caught up in the day-to-day that we forget to step back and look at the bigger picture. When I did exactly that last week, I realized something important.

The most successful people I know share three traits when it comes to {topic}:

→ They stay curious and never stop learning
→ They're not afraid to challenge the status quo
→ They focus on impact, not just activity

This isn't just theory — it's what I've seen work time and again in my own experience.

What's your take on {topic}? I'd love to hear different perspectives.

#Business #ProfessionalGrowth #LinkedIn #Insights #Learning""",
}


def generate_post(topic: str, context: str = "", tone: str = "professional-personal") -> str:
    """Generate a LinkedIn post using OpenAI API, with fallback to templates."""
    if OPENAI_API_KEY:
        try:
            return _generate_with_openai(topic, context, tone)
        except Exception:
            pass

    return _generate_from_template(topic)


def _generate_with_openai(topic: str, context: str, tone: str) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    user_message = f"Write a LinkedIn post about: {topic}"
    if context:
        user_message += f"\n\nAdditional context: {context}"
    user_message += f"\n\nTone: {tone}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        max_tokens=1000,
        temperature=0.8,
    )
    return response.choices[0].message.content


def _generate_from_template(topic: str) -> str:
    topic_lower = topic.lower()
    for key, template in FALLBACK_TEMPLATES.items():
        if key in topic_lower:
            return template
    return FALLBACK_TEMPLATES["default"].replace("{topic}", topic)
