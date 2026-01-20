import streamlit as st
import requests
import json
from datetime import datetime, timedelta


# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Dynamic Lead Intelligence (Groq)", layout="wide")


# =========================
# SECRETS
# =========================
APIFY_API_KEY = st.secrets.get("APIFY", "")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not APIFY_API_KEY:
    st.error("Missing APIFY_API_KEY in Streamlit secrets.")
    st.stop()

if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY in Streamlit secrets.")
    st.stop()


# =========================
# APIFY HELPERS
# =========================
def extract_username(linkedin_url: str):
    if not linkedin_url:
        return None
    url = linkedin_url.strip().lower()

    url = url.replace("https://", "").replace("http://", "")
    url = url.replace("www.", "")

    if "linkedin.com/in/" not in url:
        return None

    username = url.split("linkedin.com/in/")[1].split("/")[0].split("?")[0]
    return username.strip() if username else None


def fetch_linkedin_profile(linkedin_url: str):
    """
    Extract LinkedIn profile info using Apify actor: apimaestro~linkedin-profile-detail
    Returns dict with basic_info + experience
    """
    username = extract_username(linkedin_url)
    if not username:
        return None

    endpoint = "https://api.apify.com/v2/acts/apimaestro~linkedin-profile-detail/run-sync-get-dataset-items"
    params = {"token": APIFY_API_KEY}

    payload = {"username": username, "includeEmail": False}

    try:
        resp = requests.post(endpoint, params=params, json=payload, timeout=90)
        if resp.status_code not in (200, 201):
            st.error(f"Apify profile actor failed: {resp.status_code}")
            return None

        data = resp.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]

        if isinstance(data, dict):
            return data

        return None

    except Exception as e:
        st.error(f"Profile extraction error: {e}")
        return None


def fetch_recent_posts(linkedin_url: str, limit: int = 2):
    """
    Extract recent posts using Apify actor: apimaestro~linkedin-batch-profile-posts-scraper
    Returns list of latest posts (sorted desc by timestamp)
    """
    endpoint = (
        "https://api.apify.com/v2/acts/"
        "apimaestro~linkedin-batch-profile-posts-scraper/"
        "run-sync-get-dataset-items"
    )

    params = {"token": APIFY_API_KEY}

    payload = {
        "includeEmail": False,
        "usernames": [linkedin_url.strip()],
    }

    try:
        resp = requests.post(endpoint, params=params, json=payload, timeout=90)
        if resp.status_code not in (200, 201):
            return []

        data = resp.json()
        if not isinstance(data, list):
            return []

        def get_ts(post):
            try:
                return int(post.get("posted_at", {}).get("timestamp", 0))
            except Exception:
                return 0

        data = sorted(data, key=get_ts, reverse=True)
        return data[:limit]

    except Exception:
        return []


def compute_activity_days(posts: list):
    """
    Compute activity days from most recent post timestamp.
    If no posts -> return None (neutral, not punished)
    """
    if not posts:
        return None

    ts = posts[0].get("posted_at", {}).get("timestamp")
    if not ts:
        return None

    try:
        post_dt = datetime.fromtimestamp(int(ts) / 1000)
        return max(0, (datetime.now() - post_dt).days)
    except Exception:
        return None


# =========================
# GROQ SCORER
# =========================
def groq_score_lead(prospect: dict):
    """
    Calls Groq LLM and returns JSON:
    {
      "priority": "HOT|WARM|COOL|COLD",
      "confidence": 0-100,
      "score": 0-100,
      "reasons": [...]
    }
    """

    url = "https://api.groq.com/openai/v1/chat/completions"
    model = "llama-3.1-8b-instant"

    prompt = f"""
You are a Lead Intelligence & Scoring Engine.

Your task:
Classify the prospect into ONE category: HOT, WARM, COOL, or COLD.

Also provide:
- score: 0 to 100
- confidence: 0 to 100
- reasons: 3 to 6 bullet reasons based on given data

Rules (dynamic):
- HOT: strong decision-maker + strong fit + strong company signals + recent activity
- WARM: good fit and decent seniority or company strength
- COOL: mixed signals (good seniority but weak fit OR no clear company strength)
- COLD: weak fit or junior role or missing important buying signals

IMPORTANT:
- If activity data is missing, do NOT automatically mark as COLD.
- Use missing fields as neutral signals.

Prospect data:
{json.dumps(prospect, indent=2)}

Return ONLY valid JSON:
{{
  "priority": "HOT|WARM|COOL|COLD",
  "score": 0-100,
  "confidence": 0-100,
  "reasons": ["...", "...", "..."]
}}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a B2B sales intelligence analyst."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=60)

    if resp.status_code != 200:
        raise RuntimeError(f"Groq API Error: {resp.text}")

    text = resp.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(text)
    except Exception:
        raise RuntimeError(f"Groq returned invalid JSON:\n{text}")


# =========================
# UI
# =========================
st.title("Dynamic Lead Intelligence Platform (Groq)")
st.caption(
    "LinkedIn data is extracted via Apify. Lead scoring is done by Groq LLM with dynamic reasons."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 1: Data Extraction")
    linkedin_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/username/")

with col2:
    st.subheader("Manual Company Info (Only 4 Fields)")
    company_name = st.text_input("Company Name")
    company_size = st.text_input("Company Size", placeholder="201-500 employees")
    annual_revenue = st.text_input("Annual Revenue", placeholder="$128.9 Million or $1.3 Billion")
    industry = st.text_input("Industry", placeholder="Banking / Financial Services / Fintech etc.")


# Session storage (to avoid old data mixing)
if "extracted" not in st.session_state:
    st.session_state.extracted = None

if "posts" not in st.session_state:
    st.session_state.posts = []

if "activity_days" not in st.session_state:
    st.session_state.activity_days = None

if "scoring_result" not in st.session_state:
    st.session_state.scoring_result = None


# Detect URL change and reset extraction only
if "prev_url" not in st.session_state:
    st.session_state.prev_url = ""

if linkedin_url and linkedin_url.strip() != st.session_state.prev_url:
    st.session_state.prev_url = linkedin_url.strip()
    st.session_state.extracted = None
    st.session_state.posts = []
    st.session_state.activity_days = None
    st.session_state.scoring_result = None


# Extract button
if st.button(" Extract LinkedIn Data"):
    if not linkedin_url:
        st.warning("Please enter LinkedIn URL.")
    else:
        with st.spinner("Extracting LinkedIn profile..."):
            profile_data = fetch_linkedin_profile(linkedin_url)

        with st.spinner("Extracting recent posts..."):
            posts = fetch_recent_posts(linkedin_url, limit=2)
            activity_days = compute_activity_days(posts)

        st.session_state.extracted = profile_data
        st.session_state.posts = posts
        st.session_state.activity_days = activity_days

        st.success("LinkedIn data extracted successfully ")


# Show extracted preview
st.divider()
st.subheader("Extracted Data Preview")

profile_data = st.session_state.extracted

if profile_data:
    basic = profile_data.get("basic_info", {})
    name = basic.get("fullname", "N/A")
    headline = basic.get("headline", "N/A")
    location = basic.get("location", {}).get("full", "N/A")

    # Current role extraction
    current_role = headline
    current_company = basic.get("current_company", "")

    exp = profile_data.get("experience", [])
    if isinstance(exp, list):
        for e in exp:
            if e.get("is_current") and e.get("title"):
                current_role = e.get("title")
                current_company = e.get("company", current_company)
                break

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Personal Information")
        st.write("**Name:**", name)
        st.write("**Headline:**", headline)
        st.write("**Location:**", location)

    with c2:
        st.markdown("### Professional Information")
        st.write("**Current Role:**", current_role)
        st.write("**Current Company:**", current_company)

    st.markdown("### Activity")
    if st.session_state.activity_days is None:
        st.write("**Recent Activity Days:** Not available (no posts found)")
    else:
        st.write("**Recent Activity Days:**", st.session_state.activity_days)

    if st.session_state.posts:
        last_post = st.session_state.posts[0]
        rel = last_post.get("posted_at", {}).get("relative", "")
        st.write("**Last Post:**", rel if rel else "Available")
else:
    st.info("No LinkedIn data extracted yet. Click **Extract LinkedIn Data**.")


# =========================
# SCORE BUTTON
# =========================
st.divider()
st.subheader("Step 2: Generate Score (Groq)")

if st.button(" Generate Score"):
    if not st.session_state.extracted:
        st.warning("Please extract LinkedIn data first.")
    else:
        # Build prospect context for Groq
        basic = st.session_state.extracted.get("basic_info", {})
        exp = st.session_state.extracted.get("experience", [])

        title = basic.get("headline", "")
        if isinstance(exp, list):
            for e in exp:
                if e.get("is_current") and e.get("title"):
                    title = e.get("title")
                    break

        prospect_context = {
            "name": basic.get("fullname"),
            "title": title,
            "location": basic.get("location", {}).get("full"),
            "company_name": company_name,
            "company_size": company_size,
            "annual_revenue": annual_revenue,
            "industry": industry,
            "activity_days": st.session_state.activity_days,  # None allowed
            "recent_posts_count": len(st.session_state.posts),
        }

        st.markdown("### Debug (Values sent to Groq)")
        st.json(prospect_context)

        try:
            with st.spinner("Scoring with Groq..."):
                result = groq_score_lead(prospect_context)

            st.session_state.scoring_result = result
            st.success("Scoring completed ")

        except Exception as e:
            st.error(f"Scoring failed: {e}")


# =========================
# DISPLAY SCORE RESULT
# =========================
result = st.session_state.scoring_result
if result:
    st.divider()
    st.subheader("Scoring Results")

    priority = result.get("priority", "N/A")
    confidence = result.get("confidence", 0)
    score = result.get("score", 0)
    reasons = result.get("reasons", [])

    c1, c2, c3 = st.columns(3)
    c1.metric("Priority", priority)
    c2.metric("Confidence", f"{confidence}%")
    c3.metric("Score", f"{score}/100")

    st.markdown("### Why this score?")
    if isinstance(reasons, list) and reasons:
        for r in reasons:
            st.write("->", r)
    else:
        st.write("No reasons returned.")
