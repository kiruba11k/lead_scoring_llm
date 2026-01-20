import streamlit as st
import requests
import json
from datetime import datetime
import re

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Lead Intelligence Platform",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================
# UI THEME CSS (NEW PATTERN)
# =========================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

:root{
  --bg:#070B18;
  --bg2:#0B1224;
  --card: rgba(255,255,255,0.06);
  --card2: rgba(255,255,255,0.09);
  --border: rgba(255,255,255,0.12);
  --text:#E5E7EB;
  --muted: rgba(229,231,235,0.70);

  --primary:#22c55e;
  --primary2:#06b6d4;
  --danger:#ef4444;
  --warn:#f59e0b;
  --info:#60a5fa;
}

/* Background */
.stApp{
  font-family: "Inter", sans-serif;
  background:
    radial-gradient(800px 500px at 10% 10%, rgba(34,197,94,0.16), transparent 60%),
    radial-gradient(800px 500px at 90% 20%, rgba(6,182,212,0.14), transparent 60%),
    radial-gradient(800px 500px at 40% 90%, rgba(96,165,250,0.12), transparent 60%),
    linear-gradient(180deg, var(--bg) 0%, var(--bg2) 60%, var(--bg) 100%);
  color: var(--text);
}

/* Remove Streamlit default padding */
.block-container{
  padding-top: 1rem !important;
  padding-bottom: 2rem !important;
}

/* Hide Streamlit default top header + toolbar */
header[data-testid="stHeader"]{
  display:none !important;
}
div[data-testid="stToolbar"]{
  display:none !important;
}
#MainMenu{
  visibility:hidden !important;
}
footer{
  visibility:hidden !important;
}

/* Top Hero Header */
.hero{
  width:100%;
  padding: 22px 22px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(34,197,94,0.16), rgba(6,182,212,0.12));
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow: 0px 25px 70px rgba(0,0,0,0.45);
  position: relative;
  overflow:hidden;
  animation: fadeIn 0.6s ease;
}

.hero:before{
  content:"";
  position:absolute;
  inset:-80px;
  background: radial-gradient(circle at 30% 30%, rgba(34,197,94,0.20), transparent 60%);
  filter: blur(12px);
}

.hero-inner{
  position:relative;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:18px;
  flex-wrap:wrap;
}

.brand{
  display:flex;
  gap:14px;
  align-items:center;
}

.logo{
  width:48px;
  height:48px;
  border-radius:16px;
  background: rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.14);
  display:flex;
  align-items:center;
  justify-content:center;
  box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.06);
}

.brand h1{
  margin:0;
  font-size:20px;
  font-weight:900;
  letter-spacing:-0.02em;
}

.brand p{
  margin:2px 0 0 0;
  font-size:12.5px;
  color: var(--muted);
}

.pills{
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
  color: rgba(229,231,235,0.80);
  font-size: 12px;
}

/* Card */
.card{
  margin-top: 14px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 18px;
  box-shadow: 0px 22px 60px rgba(0,0,0,0.35);
  backdrop-filter: blur(10px);
  animation: fadeIn 0.55s ease;
}

.card-title{
  font-size: 14px;
  font-weight: 900;
  letter-spacing:-0.01em;
  margin:0 0 6px 0;
}

.card-sub{
  font-size: 12.5px;
  color: var(--muted);
  margin:0 0 12px 0;
}

/* Inputs */
.stTextInput input{
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  border-radius: 14px !important;
  color: var(--text) !important;
  padding: 12px !important;
}
.stTextInput input:focus{
  outline:none !important;
  border: 1px solid rgba(34,197,94,0.45) !important;
}

/* Buttons */
.stButton button{
  border-radius: 14px !important;
  padding: 12px 14px !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  background: linear-gradient(135deg, rgba(34,197,94,0.95), rgba(6,182,212,0.90)) !important;
  color: #06101c !important;
  font-weight: 900 !important;
  transition: transform 0.15s ease, filter 0.15s ease !important;
}
.stButton button:hover{
  transform: translateY(-2px);
  filter: brightness(1.05);
}

/* Output Blocks */
.kv{
  display:grid;
  grid-template-columns: 150px 1fr;
  gap: 10px;
  padding: 8px 0;
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

/* Score badge */
.badge{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.12);
  font-weight: 900;
  font-size: 12px;
}
.badge-cold{ background: rgba(100,116,139,0.20); color:#cbd5e1;}
.badge-cool{ background: rgba(59,130,246,0.18); color:#bfdbfe;}
.badge-warm{ background: rgba(245,158,11,0.18); color:#fde68a;}
.badge-hot { background: rgba(239,68,68,0.18); color:#fecaca;}

hr{
  border:none;
  border-top: 1px solid rgba(255,255,255,0.10);
  margin: 14px 0;
}

/* Animations */
@keyframes fadeIn{
  from{ opacity:0; transform: translateY(8px); }
  to{ opacity:1; transform: translateY(0px); }
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

if not APIFY_API_KEY or not GROQ_API_KEY:
    st.error("Missing API keys. Please add APIFY_API_KEY and GROQ_API_KEY in Streamlit secrets.")
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
    endpoint = "https://api.apify.com/v2/acts/apimaestro~linkedin-batch-profile-posts-scraper/run-sync-get-dataset-items"
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


def groq_score_lead(payload: dict):
    url = "https://api.groq.com/openai/v1/chat/completions"
    model = "llama-3.1-8b-instant"

    prompt = f"""
You are a Predictive Lead Scoring Engine for ANY sector.

Classify the prospect into one:
HOT, WARM, COOL, COLD

Return JSON only:
{{
  "priority": "HOT|WARM|COOL|COLD",
  "score": 0-100,
  "confidence": 0-100,
  "reasons": ["...", "...", "..."]
}}

Rules:
- Missing activity should be neutral, not negative.
- Senior role + strong company size/revenue should increase score.
- If company info is strong but activity missing, still can be WARM/HOT.

Prospect Payload:
{json.dumps(payload, indent=2)}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a lead scoring engine. Output JSON only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    resp = requests.post(url, headers=headers, json=body, timeout=60)

    if resp.status_code != 200:
        raise RuntimeError(f"Groq API error {resp.status_code}: {resp.text[:500]}")

    raw = resp.json()["choices"][0]["message"]["content"].strip()

    # ---- DEBUG SAFE PRINT (optional) ----
    # st.write("RAW RESPONSE:", raw)

    # 1) If response contains ```json ... ``` remove codeblock
    raw = raw.replace("```json", "").replace("```", "").strip()

    # 2) Extract first JSON object using regex
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"Groq did not return JSON. Raw output:\n{raw[:500]}")

    json_text = match.group(0).strip()

    # 3) Parse JSON safely
    data = json.loads(json_text)

    # 4) Validate required fields
    if "priority" not in data:
        raise ValueError(f"Invalid JSON format: {data}")

    return data


def badge(priority: str):
    p = (priority or "").upper().strip()
    cls = "badge-cold"
    icon = "fa-snowflake"
    if p == "HOT":
        cls, icon = "badge-hot", "fa-fire"
    elif p == "WARM":
        cls, icon = "badge-warm", "fa-sun"
    elif p == "COOL":
        cls, icon = "badge-cool", "fa-wind"

    return f"""<span class="badge {cls}"><i class="fa-solid {icon}"></i> {p}</span>"""


def get_basic(profile_data: dict):
    basic = profile_data.get("basic_info", {})
    name = basic.get("fullname", "N/A")
    headline = basic.get("headline", "N/A")
    location = basic.get("location", {}).get("full", "N/A")
    return name, headline, location


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
# HEADER (CUSTOM)
# =========================
st.markdown(
    """
<div class="hero">
  <div class="hero-inner">
    <div class="brand">
      <div class="logo"><i class="fa-solid fa-chart-network"></i></div>
      <div>
        <h1>Lead Intelligence Platform</h1>
        <p>Dynamic extraction · Sector-independent scoring · Transparent reasons</p>
      </div>
    </div>
    <div class="pills">
      <div class="pill"><i class="fa-solid fa-database"></i> Apify</div>
      <div class="pill"><i class="fa-solid fa-brain"></i> Groq</div>
      <div class="pill"><i class="fa-solid fa-lock"></i> Secrets</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================
# TOP INPUT PANEL (ALL INPUTS HERE)
# =========================
st.markdown(
    """
<div class="card">
  <div class="card-title"><i class="fa-solid fa-pen-to-square"></i> Input Panel</div>
  <div class="card-sub">Enter LinkedIn URL + company details. Extract and score in one place.</div>
</div>
""",
    unsafe_allow_html=True,
)

colA, colB, colC = st.columns([1.6, 1, 1], gap="large")

with colA:
    linkedin_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/username/")

with colB:
    company_name = st.text_input("Company Name", placeholder="Cadence Bank")
    company_size = st.text_input("Company Size", placeholder="5,001-10,000 employees")

with colC:
    annual_revenue = st.text_input("Annual Revenue", placeholder="$1.3 Billion")
    industry = st.text_input("Industry", placeholder="Banking")

# Reset when URL changes
if linkedin_url and linkedin_url.strip() != st.session_state.prev_url:
    st.session_state.prev_url = linkedin_url.strip()
    st.session_state.profile_data = None
    st.session_state.posts = []
    st.session_state.activity_days = None
    st.session_state.result = None
    st.session_state.debug_payload = None

btn1, btn2, btn3 = st.columns([1, 1, 1], gap="medium")

with btn1:
    extract_btn = st.button("Extract Profile")
with btn2:
    score_btn = st.button("Generate Score")
with btn3:
    debug_btn = st.button("Show Debug Payload")

if extract_btn:
    if not linkedin_url:
        st.warning("Please enter LinkedIn URL.")
    else:
        with st.spinner("Extracting profile..."):
            profile = fetch_linkedin_profile(linkedin_url)

        with st.spinner("Extracting recent posts..."):
            posts = fetch_recent_posts(linkedin_url, limit=2)
            activity_days = compute_activity_days(posts)

        st.session_state.profile_data = profile
        st.session_state.posts = posts
        st.session_state.activity_days = activity_days

        if profile:
            st.success("Extraction completed successfully.")
        else:
            st.error("Extraction failed. Check URL or Apify response.")

if score_btn:
    if not st.session_state.profile_data:
        st.warning("Extract profile first.")
    else:
        name, headline, location = get_basic(st.session_state.profile_data)

        payload = {
            "name": name,
            "headline": headline,
            "location": location,
            "company_name": company_name,
            "company_size": company_size,
            "annual_revenue": annual_revenue,
            "industry": industry,
            "activity_days": st.session_state.activity_days,
            "recent_posts_count": len(st.session_state.posts),
        }

        st.session_state.debug_payload = payload

        try:
            with st.spinner("Scoring lead..."):
                res = groq_score_lead(payload)
            st.session_state.result = res
            st.success("Scoring completed successfully.")
        except Exception as e:
            st.error(f"Scoring failed: {e}")

if debug_btn and st.session_state.debug_payload:
    with st.expander("Debug Payload Sent to Groq", expanded=True):
        st.json(st.session_state.debug_payload)


# =========================
# OUTPUT PANEL (SEPARATE AREA)
# =========================
st.markdown(
    """
<div class="card">
  <div class="card-title"><i class="fa-solid fa-display"></i> Output Panel</div>
  <div class="card-sub">Extracted data and scoring results appear below.</div>
</div>
""",
    unsafe_allow_html=True,
)

out1, out2 = st.columns([1.2, 0.8], gap="large")

with out1:
    st.markdown(
        """
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-user"></i> Extracted Prospect Info</div>
          <div class="card-sub">Profile details from LinkedIn extraction.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.profile_data:
        name, headline, location = get_basic(st.session_state.profile_data)

        st.markdown(
            f"""
            <div class="card">
              <div class="kv"><div class="k">Name</div><div class="v">{name}</div></div>
              <div class="kv"><div class="k">Headline</div><div class="v">{headline}</div></div>
              <div class="kv"><div class="k">Location</div><div class="v">{location}</div></div>
              <hr/>
              <div class="kv"><div class="k">Recent Activity Days</div><div class="v">{st.session_state.activity_days if st.session_state.activity_days is not None else "Not available"}</div></div>
              <div class="kv"><div class="k">Recent Posts Found</div><div class="v">{len(st.session_state.posts)}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No extracted data yet. Please extract a LinkedIn profile.")

with out2:
    st.markdown(
        """
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-ranking-star"></i> Scoring Results</div>
          <div class="card-sub">Priority, score, confidence and dynamic reasons.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.result:
        res = st.session_state.result
        priority = res.get("priority", "COLD")
        score = res.get("score", 0)
        confidence = res.get("confidence", 0)
        reasons = res.get("reasons", [])

        st.markdown(
            f"""
            <div class="card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <div class="card-title">Priority</div>
                  {badge(priority)}
                </div>
                <div style="text-align:right;">
                  <div class="card-title">Score</div>
                  <div style="font-size:30px; font-weight:900;">{score}/100</div>
                </div>
              </div>
              <hr/>
              <div class="kv"><div class="k">Confidence</div><div class="v">{confidence}%</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="card">
              <div class="card-title"><i class="fa-solid fa-circle-info"></i> Why this prediction?</div>
              <div class="card-sub">Generated dynamically by Groq based on extracted + manual inputs.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if reasons and isinstance(reasons, list):
            for r in reasons:
                st.markdown(
                    f"""
                    <div class="card" style="padding:14px; background: rgba(255,255,255,0.05);">
                      <div style="font-size:13px; font-weight:650;">{r}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No reasons returned.")
    else:
        st.info("No scoring result yet. Generate score after extraction.")
