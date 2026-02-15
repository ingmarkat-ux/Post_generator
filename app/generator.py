"""Post generation logic using OpenAI API with fallback templates."""

from openai import OpenAI
from app.config import OPENAI_API_KEY

SYSTEM_PROMPT = """You are a LinkedIn post writing assistant for Westernacher Consulting,
a global SAP and business consulting firm with 55+ years of innovation. Their tagline
is "Nonstop Innovation" and they believe in partnership. Your writing style reflects
the Westernacher brand voice:

- First-person perspective from a consulting professional sharing insights and expertise
- Innovative, partnership-driven, confident, and forward-looking tone
- Expert authority in SAP consulting, digital transformation, and operational excellence
- Structured with short paragraphs and line breaks for readability
- Includes a hook in the first line to grab attention
- Ends with a question or call-to-action to drive engagement
- Uses clear, purposeful language — avoids generic corporate jargon
- Weaves in themes of innovation, partnership, sustainability, and technology-driven transformation
- Optimal length: 150-300 words (LinkedIn sweet spot for engagement)
- Uses line breaks between paragraphs for mobile readability
- Always includes #WesternacherConsulting and #NonstopInnovation among the hashtags (3-5 total)
"""

FALLBACK_TEMPLATES = {
    "innovation": """Nonstop Innovation isn't just a tagline — it's a mindset.

At Westernacher, we've spent 55+ years proving that innovation isn't a single breakthrough moment. It's the discipline of questioning assumptions every single day.

I recently worked with a client who had been running the same warehouse processes for a decade. We didn't overhaul everything at once. We started small — one process, one question: "Why do we do it this way?"

The results spoke for themselves:

→ 30% faster order fulfillment
→ Real-time visibility across the entire supply chain
→ A team that now sees change as opportunity, not disruption

Innovation is not about the newest technology. It's about solving real problems with the right approach.

What's one assumption in your business you've never questioned?

#WesternacherConsulting #NonstopInnovation #DigitalTransformation #SAP #Innovation""",
    "digital transformation": """Digital transformation fails when it starts with technology.

It succeeds when it starts with people and processes. After 30+ years as an SAP partner, this is the most important lesson I've learned at Westernacher.

We recently helped a global enterprise migrate to S/4HANA. The technology was the easy part. The real challenge? Aligning 12 country teams around a shared vision for operational excellence.

Here's what made the difference:

→ Starting with the business outcome, not the tool
→ Building partnerships across every level of the organization
→ Treating change management as a first-class priority

Technology-driven innovation works when people believe in the journey — not just the destination.

Where does your organization stand on its transformation roadmap?

#WesternacherConsulting #NonstopInnovation #DigitalTransformation #S4HANA #SAP""",
    "leadership": """The best leaders I've met in consulting don't have all the answers.

They have the courage to ask better questions. At Westernacher, we believe in partnership — and that starts with how we lead.

During a recent SAP implementation, our project lead did something unexpected. Instead of presenting the solution, she facilitated a workshop where the client's team designed it themselves. Our role? Guiding, challenging, and enabling.

The outcome was remarkable:

→ 95% user adoption in the first quarter
→ A client team that owns their system, not just uses it
→ A partnership that continues to grow

Leadership in consulting isn't about being the expert in the room. It's about unlocking the expertise that's already there.

What does partnership mean in your leadership style?

#WesternacherConsulting #NonstopInnovation #Leadership #Partnership #Consulting""",
    "supply chain": """Supply chains don't break overnight. They erode slowly — through disconnected systems, siloed data, and outdated processes.

At Westernacher, we've been pioneering supply chain solutions for decades. From SAP EWM to TM to Yard Logistics, we've seen what separates resilient supply chains from fragile ones.

A recent client transformation revealed a familiar pattern:

→ 4 disconnected warehouse systems generating conflicting data
→ Manual handoffs creating 48-hour blind spots
→ No real-time visibility from dock to delivery

After implementing an integrated SAP logistics platform:

→ End-to-end visibility in real time
→ 40% reduction in logistics costs
→ Faster response to demand shifts

The future of supply chain is connected, intelligent, and sustainable.

Where are the blind spots in your supply chain?

#WesternacherConsulting #NonstopInnovation #SupplyChain #Logistics #SAP""",
    "sustainability": """Carbon neutral since 2021. That's not just a milestone — it's a commitment.

At Westernacher, sustainability isn't a side project. It's woven into how we operate, how we advise our clients, and how we think about technology's role in building a better future.

But here's what I've learned: sustainability in business isn't only about reducing emissions. It's about:

→ Building processes that are efficient by design, not by accident
→ Using technology to measure, track, and improve impact
→ Making sustainability a competitive advantage, not a compliance checkbox

The enterprises that will thrive in the next decade are the ones embedding sustainability into their digital transformation strategy today.

How is your organization connecting sustainability with technology?

#WesternacherConsulting #NonstopInnovation #Sustainability #GreenBusiness #DigitalTransformation""",
    "technology": """The technology landscape is shifting faster than ever. But adopting every new tool isn't innovation — it's noise.

At Westernacher, with 30+ years as an SAP partner, we've learned that the right technology solves real problems. The wrong technology creates new ones.

A recent enterprise audit revealed a familiar story: 15 disconnected tools doing the work of 6 integrated ones.

After simplification and SAP consolidation:

→ Unified data across the organization
→ 40% reduction in operational costs
→ Teams collaborating instead of context-switching

Technology should amplify human capability and drive operational excellence — not complicate it.

Before you adopt the next platform, ask: "Does this solve a problem we actually have?"

What's your approach to technology simplification?

#WesternacherConsulting #NonstopInnovation #SAP #Technology #OperationalExcellence""",
    "default": """Something happened recently that shifted my perspective on {topic}.

At Westernacher, we believe in partnership and nonstop innovation. These aren't just words — they shape how we approach every challenge, including {topic}.

Working across 26 countries with enterprises navigating digital transformation, I've noticed the most successful organizations share three traits:

→ They stay curious and question established approaches
→ They invest in partnerships, not just vendor relationships
→ They focus on sustainable impact, not short-term fixes

After 55+ years of consulting, this isn't theory. It's what we see work, project after project, transformation after transformation.

What's your perspective on {topic}? I'd welcome the conversation.

#WesternacherConsulting #NonstopInnovation #Consulting #DigitalTransformation #Partnership""",
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
        if key != "default" and key in topic_lower:
            return template
    # Check for partial keyword matches
    keyword_map = {
        "sap": "technology",
        "s/4hana": "technology",
        "ewm": "supply chain",
        "warehouse": "supply chain",
        "logistics": "supply chain",
        "yard": "supply chain",
        "transform": "digital transformation",
        "carbon": "sustainability",
        "green": "sustainability",
        "partner": "leadership",
        "collaborat": "leadership",
        "operational": "innovation",
        "excellence": "innovation",
    }
    for keyword, template_key in keyword_map.items():
        if keyword in topic_lower and template_key in FALLBACK_TEMPLATES:
            return FALLBACK_TEMPLATES[template_key]
    return FALLBACK_TEMPLATES["default"].replace("{topic}", topic)
