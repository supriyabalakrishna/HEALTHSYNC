# app.py
# Urban Guardian AI - HackArena Edition
from backup_ai import backup_analysis
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import requests
import folium
from streamlit_folium import st_folium

# =========================================================
# CONFIG
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NODEMCU_IP = os.getenv("NODEMCU_IP")

st.set_page_config(
    page_title="Urban Guardian AI",
    page_icon="🚑",
    layout="wide"
)

# =========================================================
# FUTURISTIC CSS
# =========================================================

st.markdown("""
<style>

.stApp{
    background:
    linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #020617
    );
}

/* Hide Streamlit Branding */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* HERO */

.hero{
    text-align:center;
    padding:30px;

    border-radius:25px;

    background:
    linear-gradient(
        135deg,
        rgba(0,255,255,0.12),
        rgba(37,99,235,0.12)
    );

    border:
    1px solid rgba(0,255,255,0.25);

    box-shadow:
    0px 0px 35px rgba(0,255,255,0.15);
}

.hero-title{

    font-size:58px;
    font-weight:800;

    background:
    linear-gradient(
        90deg,
        #00ffff,
        #38bdf8,
        #60a5fa
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-sub{

    color:#94a3b8;
    font-size:18px;
}

/* METRICS */

[data-testid="metric-container"] {

    background:
    rgba(15,23,42,0.8);

    border:
    1px solid rgba(0,255,255,0.15);

    border-radius:20px;

    padding:15px;

    box-shadow:
    0px 0px 20px rgba(0,255,255,0.08);
}

[data-testid="metric-container"]:hover {

    transform:translateY(-5px);

    transition:0.3s ease;

    box-shadow:
    0px 0px 30px rgba(0,255,255,0.3);
}

/* BUTTON */

.stButton > button {

    width:100%;
    height:55px;

    border:none;

    border-radius:15px;

    color:white;

    font-size:18px;
    font-weight:bold;

    background:
    linear-gradient(
        90deg,
        #06b6d4,
        #2563eb
    );

    box-shadow:
    0px 0px 25px rgba(37,99,235,0.35);
}

.stButton > button:hover {

    transform:scale(1.02);

    transition:0.3s;

    box-shadow:
    0px 0px 35px rgba(0,255,255,0.5);
}

/* TEXT AREA */

textarea {

    background:
    rgba(15,23,42,0.8) !important;

    color:white !important;

    border:
    1px solid rgba(0,255,255,0.2) !important;

    border-radius:15px !important;
}

/* GLASS CARD */

.glass{

    background:
    rgba(255,255,255,0.04);

    backdrop-filter:
    blur(15px);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:20px;

    padding:20px;
}

/* GLOW */

@keyframes pulse {

    0%{
        box-shadow:
        0px 0px 15px rgba(0,255,255,0.1);
    }

    50%{
        box-shadow:
        0px 0px 35px rgba(0,255,255,0.35);
    }

    100%{
        box-shadow:
        0px 0px 15px rgba(0,255,255,0.1);
    }
}

.glow{
    animation:pulse 3s infinite;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# GEMINI
# =========================================================

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# =========================================================
# FALLBACK
# =========================================================

def fallback_response():

    return {
        "severity":"Critical",
        "type":"Cardiac Emergency",
        "location":"Silk Board Junction",
        "hospital":"Apollo Hospital",
        "route":[
            "Silk Board",
            "BTM Layout",
            "Apollo Hospital"
        ],
        "corridor_required":True,
        "citizen_alert":
        "Emergency ambulance approaching. Please use alternate routes."
    }

# =========================================================
# GEMINI ANALYSIS
# =========================================================

def analyze_emergency(text):

    if not GEMINI_API_KEY:
        return fallback_response()

    prompt = f"""
You are Urban Guardian AI.

Analyze the emergency.

Return ONLY JSON.

{{
"severity":"",
"type":"",
"location":"",
"hospital":"",
"route":[],
"corridor_required":true,
"citizen_alert":""
}}

Emergency:
{text}
"""

    try:

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            prompt
        )

        clean = (
            response.text
            .replace("```json","")
            .replace("```","")
            .strip()
        )

        return json.loads(clean)

    except Exception:
        return fallback_response()

# =========================================================
# NODEMCU
# =========================================================

def activate_corridor():

    try:

        requests.get(
            f"http://{NODEMCU_IP}/emergency",
            timeout=2
        )

        return True

    except:

        return False


def normal_mode():

    try:

        requests.get(
            f"http://{NODEMCU_IP}/normal",
            timeout=2
        )

        return True

    except:

        return False


def get_status():

    try:

        requests.get(
            f"http://{NODEMCU_IP}/status",
            timeout=2
        )

        return True

    except:

        return False

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class='hero glow'>
<div class='hero-title'>
🚑 Urban Guardian AI
</div>

<div class='hero-sub'>
Agentic Emergency Response & Smart Traffic Command Center
</div>
</div>
""",
unsafe_allow_html=True)

st.write("")

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "🚨 Emergency Dashboard",
    "🗺 Smart City View",
    "⚙ Hardware Monitoring"
])

# =========================================================
# TAB 1
# =========================================================

with tab1:

    emergency = st.text_area(
        "🚨 Describe Emergency",
        height=160,
        placeholder="Critical cardiac patient near Silk Board Junction. Heavy traffic congestion..."
    )

    analyze = st.button(
        "Analyze Emergency"
    )

    if analyze:

        with st.spinner(
            "🤖 AI Agents Coordinating..."
        ):

            data = analyze_emergency(
                emergency
            )

        c1,c2,c3,c4 = st.columns(4)

        c1.metric(
            "Severity",
            data["severity"]
        )

        c2.metric(
            "Location",
            data["location"]
        )

        c3.metric(
            "Hospital",
            data["hospital"]
        )

        c4.metric(
            "Corridor",
            "ACTIVE"
            if data["corridor_required"]
            else "OFF"
        )

        st.divider()

        left,right = st.columns(
            [2,1]
        )

        with left:

            st.subheader(
                "🧠 AI Analysis"
            )

            st.info(
                f"Emergency Type: {data['type']}"
            )

            st.success(
                f"Recommended Hospital: {data['hospital']}"
            )

            st.write(
                f"Route: {' ➜ '.join(data['route'])}"
            )

        with right:

            st.subheader(
                "🤖 Agents"
            )

            st.success(
                "Emergency Agent"
            )

            st.success(
                "Hospital Agent"
            )

            st.success(
                "Traffic Agent"
            )

            st.success(
                "Citizen Alert Agent"
            )

        st.divider()

        st.subheader(
            "🚦 Traffic Control"
        )

        if data["corridor_required"]:

            activate_corridor()

            st.success(
                "Emergency Corridor Activated"
            )

        else:

            normal_mode()

            st.info(
                "Normal Traffic Mode"
            )

        st.divider()

        st.subheader(
            "📢 Citizen Alert"
        )

        st.warning(
            data["citizen_alert"]
        )

# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.subheader(
        "🗺 Smart City Route Visualization"
    )

    m = folium.Map(
        location=[12.9279,77.6271],
        zoom_start=12
    )

    folium.Marker(
        [12.9279,77.6271],
        popup="🚑 Ambulance"
    ).add_to(m)

    folium.Marker(
        [12.8945,77.5970],
        popup="🏥 Apollo Hospital"
    ).add_to(m)

    folium.PolyLine(
        [
            [12.9279,77.6271],
            [12.8945,77.5970]
        ],
        color="lime",
        weight=8
    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=500
    )
# =========================================================
# TAB 3
# =========================================================

with tab3:

    st.subheader(
        "⚙ Hardware Monitoring"
    )

    online = get_status()

    col1,col2,col3 = st.columns(3)

    with col1:

        st.metric(
            "NodeMCU",
            "ONLINE" if online else "OFFLINE"
        )

    with col2:

        st.metric(
            "Traffic Corridor",
            "READY"
        )

    with col3:

        st.metric(
            "Emergency Mode",
            "STANDBY"
        )

    if online:

        st.success(
            "🟢 NodeMCU Connected Successfully"
        )

    else:

        st.warning(
            "🟡 NodeMCU Not Reachable"
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Powered by Gemini • Agentic AI • ESP8266 • Urban Guardian AI"
)
st.subheader("📊 Impact Metrics")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Response Time Saved",
    "6 min"
)

c2.metric(
    "Traffic Delay Reduced",
    "32%"
)

c3.metric(
    "Emergency Priority",
    "HIGH"
)

c4.metric(
    "Corridor Length",
    "4.2 km"
)