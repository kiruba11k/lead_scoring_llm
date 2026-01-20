import streamlit as st
import requests
import json
from datetime import datetime


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Dynamic Lead Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# MODERN UI CSS (FIXED LAYOUT)
# =========================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

:root{
  --bg1:#050814;
  --bg2:#0b1220;
  --panel: rgba(255,255,255,0.06);
  --panel2: rgba(255,255,255,0.08);
  --border: rgba(255,255,255,0.12);
  --text: #e5e7eb;
  --muted: rgba(229,231,235,0.72);
  --accent: #60a5fa;
  --accent2:#a78bfa;
  --good:#22c55e;
  --warn:#f59e0b;
  --bad:#ef4444;
}

/* Full background */
.stApp{
  font-family: "Inter", sans-serif;
  background:
    radial-gradient(900px 500px at 10% 10%, rgba(96,165,250,0.25), transparent 55%),
    radial-gradient(900px 500px at 90% 20%, rgba(167,139,250,0.18), transparent 55%),
    radial-gradient(900px 600px at 40% 95%, rgba(34,197,94,0.10), transparent 60%),
    linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 65%, var(--bg1) 100%);
  color: var(--text);
}

/* Remove top blank padding */
.block-container{
  padding-top: 0.8rem !important;
  padding-bottom: 2.2rem !important;
}

/* Change Streamlit header bar */
header[data-testid="stHeader"]{
  background: rgba(5,8,20,0.72) !important;
  backdrop-filter: blur(10px) !important;
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
}

/* Make toolbar icons visible */
header[data-testid="stHeader"] *{
  color: rgba(229,231,235,0.85) !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
  background: rgba(255,255,255,0.03) !important;
  border-right: 1px solid rgba(255,255,255,0.08) !important;
}

/* NAVBAR */
.navbar{
  width: 100%;
  padding: 14px 16px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  background: linear-gradient(135deg, rgba(96,165,250,0.14), rgba(167,139,250,0.10));
  box-shadow: 0px 18px 55px rgba(0,0,0,0.35);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  position: sticky;
  top: 0.6rem;
  z-index: 50;
}

.brand{
  display:flex;
  align-items:center;
  gap:10px;
}

.brand-icon{
  width: 42px;
  height: 42px;
  border-radius: 14px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  display:flex;
  align-items:center;
  justify-content:center;
  box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.06);
}

.brand-title{
  font-size: 18px;
  font-weight: 900;
  letter-spacing: -0.02em;
  margin:0;
}

.brand-sub{
  font-size: 12px;
  color: var(--muted);
  margin-top:2px;
}

.nav-pills{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  justify-content:flex-end;
}

.pill{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  color: var(--muted);
  font-size: 12px;
}

/* Cards */
.card{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0px 18px 55px rgba(0,0,0,0.28);
  backdrop-filter: blur(10px);
}

.card:hover{
  border-color: rgba(96,165,250,0.30);
}

/* Section title */
.h2{
  font-size: 15px;
  font-weight: 900;
  letter-spacing: -0.01em;
  margin: 0 0 8px 0;
}
.desc{
  font-size: 12.5px;
  color: var(--muted);
  margin: 0 0 12px 0;
}

/* Input style */
.stTextInput input{
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 14px !important;
  color: var(--text) !important;
  padding: 12px !important;
}
.stTextInput input::placeholder{
  color: rgba(229,231,235,0.40) !important;
}

/* Buttons */
.stButton button{
  border-radius: 14px !important;
  padding: 12px 14px !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  background: linear-gradient(135deg, rgba(96,165,250,0.95), rgba(167,139,250,0.92)) !important;
  color: #050814 !important;
  font-weight: 900 !important;
  transition: transform 0.15s ease, filter 0.15s ease !important;
}
.stButton button:hover{
  transform: translateY(-2px);
  filter: brightness(1.05);
}

/* Secondary button (we wrap in div) */
.secondary button{
  background: rgba(255,255,255,0.08) !important;
  color: var(--text) !important;
}

/* Key-Value */
.kv{
  display:grid;
  grid-template-columns: 140px 1fr;
  gap: 10px;
  margin: 8px 0;
}
.k{
  color: var(--muted);
  font-size: 12px;
}
.v{
  color: var(--text);
  font-size: 13px;
  font-weight: 650;
}

/* Badge */
.badge{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.12);
  font-weight: 900;
  font-size: 12px;
  letter-spacing: 0.02em;
}
.badge-cold{ background: rgba(100,116,139,0.22); color:#cbd5e1;}
.badge-cool{ background: rgba(59,130,246,0.22); color:#bfdbfe;}
.badge-warm{ background: rgba(245,158,11,0.22); color:#fde68a;}
.badge-hot { background: rgba(239,68,68,0.22); color:#fecaca;}

/* Metric tiles */
.metrics{
  display:grid;
  grid-template-columns: repeat(3, minmax(0,1fr));
  gap: 12px;
  margin-top: 12px;
}
.tile{
  padding: 14px;
  border-radius: 16px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
}
.tile .label{
  font-size: 12px;
  color: var(--muted);
}
.tile .value{
  margin-top: 6px;
  font-size: 20px;
  font-weight: 900;
}

/* Reason card */
.reason{
  padding: 12px;
  border-radius: 16px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.10);
  margin-top: 10px;
  display:flex;
  gap:10px;
  align-items:flex-start;
}
.reason-icon{
  width: 28px;
  height: 28px;
  border-radius: 10px;
  display:flex;
  align-items:center;
  justify-content:center;
  background: rgba(96,165,250,0.16);
  border: 1px solid rgba(255,255,255,0.12);
}

hr{
  border:none;
  border-top: 1px solid rgba(255,255,255,0.10);
  margin: 14px 0;
}

</style>
""",
    unsafe_allow_html=True,
)


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
# HELPERS
# =========================
def extract_username(linkedin_url: str):
    if not linkedin_url:
        return None
    url = linkedin_url.strip().lower()
    url = url.replace("https://", "").replace("http://", "").replace("www.", "")
    if "linkedin.com/in/" not in url:
        return None
    username = url.split("linkedin.com/in/")[1].split("/")[0].split("?")[0]
    return username.strip() if username else None


def fetch_linkedin_profile(linkedin_url: str):
    username = extract_username(linkedin_url)
    if not username:
        return None

    endpoint = "https://api.apify.com/v2/acts/apimaestro~linkedin-profile-detail/run-sync-get-dataset-items"
    params = {"token": APIFY_API_KEY}
    payload = {"username": username, "includeEmail": False}

    resp = requests.post(endpoint, params=params, json=payload, timeout=90)
    if resp.status_code not in (200, 201):
        return None

    data = resp.json()
    if isinstance(data, list) and len(data) > 0:
        return data[0]
    if isinstance(data, dict):
        return data
    return None


def fetch_recent_posts(linkedin_url: str, limit: int = 2):
    endpoint = (
        "https://api.apify.com/v2/acts/"
        "apimaestro~linkedin-batch-profile-posts-scraper/"
        "run-sync-get-dataset-items"
    )
    params = {"token": APIFY_API_KEY}
    payload = {"includeEmail": False, "usernames": [linkedin_url.strip()]}

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


def groq_score_lead(prospect: dict):
    url = "https://api.groq.com/openai/v1/chat/completions"
    model = "llama-3.1-8b-instant"

    prompt = f"""
You are a Lead Intelligence & Scoring Engine.

Classify the prospect into ONE category:
HOT, WARM, COOL, or COLD.

Return:
- priority
- score (0 to 100)
- confidence (0 to 100)
- reasons (3 to 6)

Rules:
- HOT: strong decision-maker + strong fit + strong company signals + recent activity
- WARM: good fit and decent seniority or company strength
- COOL: mixed signals
- COLD: weak fit or junior role or weak company signals

IMPORTANT:
If activity is missing, treat it as neutral. Do NOT force COLD.

Prospect:
{json.dumps(prospect, indent=2)}

Return ONLY JSON:
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
        raise RuntimeError(resp.text)

    content = resp.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def get_current_role_and_company(profile_data: dict):
    basic = profile_data.get("basic_info", {})
    headline = basic.get("headline", "") or ""
    company = basic.get("current_company", "") or ""

    title = headline
    exp = profile_data.get("experience", [])
    if isinstance(exp, list):
        for e in exp:
            if e.get("is_current") and e.get("title"):
                title = e.get("title", title)
                company = e.get("company", company)
                break

    return title, company


def priority_badge(priority: str):
    p = (priority or "").upper().strip()
    cls = "badge-cold"
    icon = "fa-snowflake"
    if p == "HOT":
        cls, icon = "badge-hot", "fa-fire"
    elif p == "WARM":
        cls, icon = "badge-warm", "fa-sun"
    elif p == "COOL":
        cls, icon = "badge-cool", "fa-wind"

    return f"""
    <span class="badge {cls}">
        <i class="fa-solid {icon}"></i> {p}
    </span>
    """


# =========================
# SESSION STATE
# =========================
if "prev_url" not in st.session_state:
    st.session_state.prev_url = ""

if "profile_data" not in st.session_state:
    st.session_state.profile_data = None

if "posts" not in st.session_state:
    st.session_state.posts = []

if "activity_days" not in st.session_state:
    st.session_state.activity_days = None

if "result" not in st.session_state:
    st.session_state.result = None

if "debug_payload" not in st.session_state:
    st.session_state.debug_payload = None


# =========================
# NAVBAR
# =========================
st.markdown(
    """
<div class="navbar">
  <div class="brand">
    <div class="brand-icon"><i class="fa-solid fa-layer-group"></i></div>
    <div>
      <div class="brand-title">Dynamic Lead Intelligence</div>
      <div class="brand-sub">Extraction via Apify · Scoring via Groq · Dynamic reasons</div>
    </div>
  </div>
  <div class="nav-pills">
    <div class="pill"><i class="fa-solid fa-database"></i> Live Extraction</div>
    <div class="pill"><i class="fa-solid fa-brain"></i> LLM Scoring</div>
    <div class="pill"><i class="fa-solid fa-shield-halved"></i> Secrets Protected</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)


# =========================
# SIDEBAR CONTROLS
# =========================
with st.sidebar:
    st.markdown("### Controls")
    st.caption("Reset the current prospect without refreshing the app.")

    st.markdown("<div class='secondary'>", unsafe_allow_html=True)
    if st.button("Reset Prospect"):
        st.session_state.profile_data = None
        st.session_state.posts = []
        st.session_state.activity_days = None
        st.session_state.result = None
        st.session_state.debug_payload = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# MAIN LAYOUT
# =========================
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown(
        """
        <div class="card">
            <div class="h2"><i class="fa-solid fa-link"></i> Prospect Extraction</div>
            <div class="desc">Enter LinkedIn URL to extract profile + recent posts activity.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    linkedin_url = st.text_input(
        "LinkedIn Profile URL",
        placeholder="https://www.linkedin.com/in/username/",
        key="linkedin_url_input",
    )

    # Reset when URL changes
    if linkedin_url and linkedin_url.strip() != st.session_state.prev_url:
        st.session_state.prev_url = linkedin_url.strip()
        st.session_state.profile_data = None
        st.session_state.posts = []
        st.session_state.activity_days = None
        st.session_state.result = None
        st.session_state.debug_payload = None

    btn1, btn2 = st.columns([1, 1], gap="medium")
    with btn1:
        extract_btn = st.button("Extract Profile + Activity")
    with btn2:
        st.markdown("<div class='secondary'>", unsafe_allow_html=True)
        show_debug = st.button("Show Debug Payload")
        st.markdown("</div>", unsafe_allow_html=True)

    if extract_btn:
        if not linkedin_url:
            st.warning("Please enter a LinkedIn URL.")
        else:
            with st.spinner("Extracting LinkedIn profile..."):
                profile_data = fetch_linkedin_profile(linkedin_url)

            with st.spinner("Extracting recent posts..."):
                posts = fetch_recent_posts(linkedin_url, limit=2)
                activity_days = compute_activity_days(posts)

            st.session_state.profile_data = profile_data
            st.session_state.posts = posts
            st.session_state.activity_days = activity_days

            if profile_data:
                st.success("Extraction completed successfully.")
            else:
                st.error("Extraction failed. Check LinkedIn URL or Apify response.")

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="h2"><i class="fa-solid fa-building"></i> Manual Company Details</div>
            <div class="desc">Only these 4 fields are needed for scoring.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    company_name = st.text_input("Company Name", placeholder="MidCap Financial")
    company_size = st.text_input("Company Size", placeholder="201-500 employees")
    annual_revenue = st.text_input("Annual Revenue", placeholder="$128.9 Million or $1.3 Billion")
    industry = st.text_input("Industry", placeholder="Banking / Financial Services / Fintech")


with right:
    st.markdown(
        """
        <div class="card">
            <div class="h2"><i class="fa-solid fa-user"></i> Extracted Preview</div>
            <div class="desc">Profile information and activity signal.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.profile_data:
        basic = st.session_state.profile_data.get("basic_info", {})
        name = basic.get("fullname", "N/A")
        headline = basic.get("headline", "N/A")
        location = basic.get("location", {}).get("full", "N/A")

        title, current_company = get_current_role_and_company(st.session_state.profile_data)

        st.markdown(
            f"""
            <div class="card" style="margin-top: 12px;">
                <div class="kv"><div class="k">Name</div><div class="v">{name}</div></div>
                <div class="kv"><div class="k">Headline</div><div class="v">{headline}</div></div>
                <div class="kv"><div class="k">Location</div><div class="v">{location}</div></div>
                <hr/>
                <div class="kv"><div class="k">Current Role</div><div class="v">{title}</div></div>
                <div class="kv"><div class="k">Current Company</div><div class="v">{current_company}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        activity_days = st.session_state.activity_days
        posts = st.session_state.posts

        activity_text = "Not available"
        last_post_text = "Not available"

        if activity_days is not None:
            activity_text = str(activity_days)

        if posts:
            last_post_text = posts[0].get("posted_at", {}).get("relative", "Available")

        st.markdown(
            f"""
            <div class="card" style="margin-top: 12px;">
                <div class="h2"><i class="fa-solid fa-chart-line"></i> Activity</div>
                <div class="kv"><div class="k">Recent Activity Days</div><div class="v">{activity_text}</div></div>
                <div class="kv"><div class="k">Last Post</div><div class="v">{last_post_text}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Enter a LinkedIn URL and extract profile first.")

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="h2"><i class="fa-solid fa-wand-magic-sparkles"></i> Lead Scoring</div>
            <div class="desc">Groq predicts priority with reasons dynamically.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_btn = st.button("Generate Score")

    if score_btn:
        if not st.session_state.profile_data:
            st.warning("Extract LinkedIn profile first.")
        else:
            title, current_company = get_current_role_and_company(st.session_state.profile_data)
            basic = st.session_state.profile_data.get("basic_info", {})

            payload = {
                "name": basic.get("fullname"),
                "title": title,
                "location": basic.get("location", {}).get("full"),
                "current_company": current_company,
                "company_name": company_name,
                "company_size": company_size,
                "annual_revenue": annual_revenue,
                "industry": industry,
                "activity_days": st.session_state.activity_days,
                "recent_posts_count": len(st.session_state.posts),
            }

            st.session_state.debug_payload = payload

            try:
                with st.spinner("Scoring with Groq..."):
                    result = groq_score_lead(payload)
                st.session_state.result = result
                st.success("Scoring completed successfully.")
            except Exception as e:
                st.error(f"Scoring failed: {e}")

    if st.session_state.result:
        res = st.session_state.result
        priority = (res.get("priority") or "").upper()
        score = res.get("score", 0)
        confidence = res.get("confidence", 0)
        reasons = res.get("reasons", [])

        st.markdown(
            f"""
            <div class="card" style="margin-top: 12px;">
                <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
                    <div>
                        <div class="h2">Scoring Results</div>
                        <div style="margin-top:8px;">{priority_badge(priority)}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="pill"><i class="fa-solid fa-gauge-high"></i> Score</div>
                        <div style="font-size:28px; font-weight:900; margin-top:6px;">{score}/100</div>
                    </div>
                </div>

                <div class="metrics">
                    <div class="tile">
                        <div class="label">Confidence</div>
                        <div class="value">{confidence}%</div>
                    </div>
                    <div class="tile">
                        <div class="label">Recent Posts</div>
                        <div class="value">{len(st.session_state.posts)}</div>
                    </div>
                    <div class="tile">
                        <div class="label">Activity Days</div>
                        <div class="value">{st.session_state.activity_days if st.session_state.activity_days is not None else "N/A"}</div>
                    </div>
                </div>

                <hr/>
                <div class="h2">Why this prediction?</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if isinstance(reasons, list) and reasons:
            for r in reasons:
                st.markdown(
                    f"""
                    <div class="reason">
                        <div class="reason-icon"><i class="fa-solid fa-check"></i></div>
                        <div style="font-size:13px; font-weight:650; color: rgba(229,231,235,0.92);">
                            {r}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No reasons returned by the model.")

    if show_debug and st.session_state.debug_payload:
        with st.expander("Debug Payload Sent to Groq", expanded=True):
            st.json(st.session_state.debug_payload)
